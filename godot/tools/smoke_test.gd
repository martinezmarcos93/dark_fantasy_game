extends Node
## Piloto automático headless — recorre una partida entera sin intervención.
##
## Existe porque los ~4000 renglones portados (10 niveles, combate, finales)
## nunca se habían ejecutado juntos: `--quit-after` solo probaba el arranque.
## No es un test de comportamiento (ese contrato es test_game.py): es un
## detector de crashes en runtime — nulls, índices fuera de rango, awaits
## colgados, rutas de assets rotas.
##
## Uso:
##   godot --headless --path . tools/smoke_test.tscn -- --semilla 7
##   godot --headless --path . tools/smoke_test.tscn -- --semilla 7 --lectura
##
## Cada semilla toma un camino distinto por el árbol de decisiones, así que
## varias corridas cubren ramas distintas de los niveles. Con `--lectura`
## corre en Modo Lectura (sin combate): el jugador no muere, así que la
## corrida atraviesa los 10 niveles y llega al final — la única forma barata
## de ejercitar los niveles profundos, que al azar casi nunca se alcanzan.

const GameScreenScene := preload("res://scenes/GameScreen.tscn")

## Tope de pantallas antes de declarar bucle infinito.
const MAX_PANTALLAS := 4000
## Frames seguidos sin que la pantalla pida input antes de declarar cuelgue.
const MAX_FRAMES_QUIETO := 6000

var _gs: Control
var _rng := RandomNumberGenerator.new()
var _pantallas := 0
var _frames_quieto := 0
var _terminado := false
var _semilla := 1
var _lectura := false


func _ready() -> void:
	_semilla = _leer_semilla()
	_rng.seed = _semilla
	seed(_semilla)  # el juego usa randi_range/pick_random globales

	# El tiempo acelerado hace que los fundidos y el typewriter no dominen
	# la duración de la corrida. Los Tween respetan time_scale.
	Engine.time_scale = 50.0

	_lectura = "--lectura" in OS.get_cmdline_user_args()
	print("── smoke_test | semilla=%d | modo=%s ──"
		% [_semilla, "lectura" if _lectura else "normal"])

	_gs = GameScreenScene.instantiate()
	add_child(_gs)
	GameEngine.pantalla = _gs
	await get_tree().process_frame

	# Rama "nueva partida" del flujo real, sin el menú (que ya se verifica con
	# --quit-after y cuya opción "Salir" cortaría la corrida).
	GameEngine.save_slot = 0
	GameEngine.current_level_index = 0
	GameEngine.modo_lectura = _lectura
	SaveSystem.borrar_partida(0)

	await GameEngine.mostrar_intro()
	print("   intro OK")
	await GameEngine.crear_personaje()
	print("   personaje OK: %s — %s" % [GameEngine.player.name_jugador, GameEngine.player.clase])
	GameEngine.cargar_niveles()
	await GameEngine.jugar()

	_terminado = true
	print("── FIN | pantallas=%d | nivel alcanzado=%d | vivo=%s ──"
		% [_pantallas, GameEngine.current_level_index, str(GameEngine.player.alive)])
	get_tree().quit(0)


func _process(_delta: float) -> void:
	if _terminado or _gs == null:
		return

	# Campo de nombre (crear_personaje): responder y salir.
	for c in _gs.get_children():
		if c is LineEdit:
			c.text = "Piloto"
			c.text_submitted.emit("Piloto")
			return

	if not _gs._esperando:
		_frames_quieto += 1
		if _frames_quieto > MAX_FRAMES_QUIETO:
			push_error("smoke_test: la pantalla no pidió input en %d frames — flujo colgado tras %d pantallas (nivel %d)"
				% [MAX_FRAMES_QUIETO, _pantallas, GameEngine.current_level_index])
			get_tree().quit(1)
		return

	_frames_quieto = 0

	if _gs._typing:
		_gs._skip_typing()
		return

	_pantallas += 1
	if _pantallas > MAX_PANTALLAS:
		push_error("smoke_test: %d pantallas sin terminar — bucle infinito (nivel %d)"
			% [MAX_PANTALLAS, GameEngine.current_level_index])
		get_tree().quit(1)
		return

	var n: int = _gs._opciones_actuales.size()
	_gs._on_boton_pressed(_rng.randi_range(0, n - 1) if n > 0 else -1)


## Lee `-- --semilla N` de la línea de comandos. Sin argumento: 1.
func _leer_semilla() -> int:
	var args := OS.get_cmdline_user_args()
	for i in range(args.size() - 1):
		if args[i] == "--semilla":
			return int(args[i + 1])
	return 1
