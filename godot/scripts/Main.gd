extends Node
## Main — punto de entrada del juego.
## DEMO de Fase 4: arranca Level1 punta a punta conduciendo la GameScreen.
## En fases siguientes se antepone el flujo Menu → Intro → creación de personaje.

const GameScreenScene := preload("res://scenes/GameScreen.tscn")
const Level1Script := preload("res://scripts/levels/level1.gd")

var _gs: Control


func _ready() -> void:
	print("Descenso al Umbral — Godot 4.6 | Fase 4: Level1")
	_gs = GameScreenScene.instantiate()
	add_child(_gs)
	_demo()


func _demo() -> void:
	# Player de prueba
	var p := Player.new()
	p.inicializar("Marcos", "Hechicero")
	p.aliento = 4
	p.level = 1

	# Cablear el director: GameEngine conduce la GameScreen (ADR-007)
	GameEngine.player = p
	GameEngine.pantalla = _gs
	GameEngine.current_level_index = 0
	_gs.actualizar_hud(p)

	# Pantalla de apertura
	var texto := "[center]Descenso al Umbral[/center]\n\n" \
		+ "El mundo se consume en silencio.\n" \
		+ "Los que descienden no regresan.\n" \
		+ "Los que regresan… ya no son los mismos.\n\n" \
		+ "¿Quién sos para intentarlo?"
	await _gs.mostrar_pantalla("res://assets/images/lvl1.jpg", texto, ["Descender al Umbral"])

	# ── Level 1 punta a punta (combate → fase psicológica → cofre → llave) ──
	var level1: BaseLevel = Level1Script.new()
	var resultado: String = await level1.jugar(p, GameEngine)
	print("[demo] Resultado de %s: %s" % [level1.nombre, resultado])
	print("[demo] Fin del demo.")
