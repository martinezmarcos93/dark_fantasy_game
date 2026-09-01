extends Node
## AudioManager — música por contexto con crossfade real.
##
## Port de UI.reproducir_musica() (ui.py:595). El contrato del original:
##   nombre=X → X.mp3         (menu, boss, ambiente, credits)
##   nivel=N  → nivel_N.mp3
##   si la pista pedida no existe → una aleatoria del pool
##   al terminar una pista, arranca la del nivel actual  (ui.py:452-453)
##
## Lo único que cambia respecto de Pygame es el empalme: allá el corte era
## seco (mixer.music.play()), acá hay crossfade de 1.5 s entre dos players.

const MUSIC_DIR: String = "res://assets/music/"
const FADE_DURATION: float = 1.5

## Pool de pistas. Lista fija en vez de listar el directorio: al exportar,
## los .mp3 viven como .mp3str dentro de .godot/imported/ y un DirAccess
## sobre res://assets/music/ devolvería vacío.
const PISTAS: Array[String] = [
	"ambiente", "boss", "credits", "menu",
	"nivel_0", "nivel_1", "nivel_2", "nivel_3", "nivel_4",
	"nivel_5", "nivel_6", "nivel_7", "nivel_8", "nivel_9",
]

## Nivel cuya música corresponde ahora (-1 = fuera de los niveles: menú, intro).
## Cambiarlo NO corta la pista en curso: igual que en el original, el relevo
## ocurre recién cuando la pista actual termina.
var nivel_actual: int = -1

var _jugador_a: AudioStreamPlayer
var _jugador_b: AudioStreamPlayer
var _activo: AudioStreamPlayer
var _tween: Tween


func _ready() -> void:
	_jugador_a = AudioStreamPlayer.new()
	_jugador_b = AudioStreamPlayer.new()
	add_child(_jugador_a)
	add_child(_jugador_b)
	_activo = _jugador_a
	# Los .mp3 se importan con loop=false, así que `finished` sí se emite.
	_jugador_a.finished.connect(_on_pista_terminada.bind(_jugador_a))
	_jugador_b.finished.connect(_on_pista_terminada.bind(_jugador_b))


# ═══════════════════════════════════════════════════════════════
# API PÚBLICA
# ═══════════════════════════════════════════════════════════════
## Reproduce por nombre ("menu", "boss", "ambiente") o por nivel (int >= 0).
## Sin argumentos válidos, o si el archivo no existe: pista aleatoria.
func reproducir(nombre: String = "", nivel: int = -1) -> void:
	var pista := ""
	if nombre != "":
		pista = nombre
	elif nivel >= 0:
		pista = "nivel_%d" % nivel

	if pista == "" or not _existe(pista):
		pista = _pista_aleatoria()
	if pista == "":
		return

	_reproducir_pista(pista)


## Declara en qué nivel estamos. Si no suena nada, arranca ya; si algo suena,
## espera a que termine (fidelidad con ui.py: la música no se corta al bajar
## de nivel, se releva al terminar la pista).
func ambientar_nivel(n: int) -> void:
	nivel_actual = n
	if not _sonando():
		reproducir("", n)


func detener() -> void:
	if _tween:
		_tween.kill()
	_jugador_a.stop()
	_jugador_b.stop()


# ═══════════════════════════════════════════════════════════════
# INTERNO
# ═══════════════════════════════════════════════════════════════
func _reproducir_pista(pista: String) -> void:
	var stream := load(MUSIC_DIR + pista + ".mp3") as AudioStream
	if stream == null:
		return

	var saliente := _activo
	var entrante := _jugador_b if _activo == _jugador_a else _jugador_a
	entrante.stream = stream
	entrante.volume_db = -80.0
	entrante.play()
	# El activo cambia ya, no al final del fade: así una llamada durante el
	# crossfade encadena correctamente en vez de pisarse con la anterior.
	_activo = entrante

	if _tween:
		_tween.kill()
	_tween = create_tween().set_parallel(true)
	_tween.tween_property(saliente, "volume_db", -80.0, FADE_DURATION)
	_tween.tween_property(entrante, "volume_db",   0.0, FADE_DURATION)
	_tween.finished.connect(saliente.stop, CONNECT_ONE_SHOT)


func _on_pista_terminada(quien: AudioStreamPlayer) -> void:
	# Solo releva el que estaba al frente: el saliente de un crossfade que
	# termine solo no debe disparar una pista nueva.
	if quien != _activo:
		return
	reproducir("", nivel_actual)


func _existe(pista: String) -> bool:
	return pista in PISTAS and ResourceLoader.exists(MUSIC_DIR + pista + ".mp3")


func _pista_aleatoria() -> String:
	var disponibles: Array[String] = []
	for p in PISTAS:
		if ResourceLoader.exists(MUSIC_DIR + p + ".mp3"):
			disponibles.append(p)
	return disponibles.pick_random() if not disponibles.is_empty() else ""


func _sonando() -> bool:
	return _jugador_a.playing or _jugador_b.playing
