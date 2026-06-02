extends Node
## AudioManager — música por nivel con crossfade real.
## Equivale al sistema de reproducir_musica() en ui.py.
## Usa dos AudioStreamPlayer para crossfade: uno activo, uno fade-in.

var _jugador_a: AudioStreamPlayer
var _jugador_b: AudioStreamPlayer
var _activo: AudioStreamPlayer
var _tween: Tween

const MUSIC_DIR: String = "res://assets/music/"
const FADE_DURATION: float = 1.5


func _ready() -> void:
	_jugador_a = AudioStreamPlayer.new()
	_jugador_b = AudioStreamPlayer.new()
	add_child(_jugador_a)
	add_child(_jugador_b)
	_activo = _jugador_a


# Reproduce música por nombre ("menu", "boss", "ambiente") o por nivel (int)
func reproducir(nombre: String = "", nivel: int = -1) -> void:
	var archivo := ""
	if nombre != "":
		archivo = MUSIC_DIR + nombre + ".mp3"
	elif nivel >= 0:
		archivo = MUSIC_DIR + "nivel_%d.mp3" % nivel

	if archivo == "" or not ResourceLoader.exists(archivo):
		return

	var stream := load(archivo) as AudioStream
	if stream == null:
		return

	# Crossfade al jugador inactivo
	var entrante := _jugador_b if _activo == _jugador_a else _jugador_a
	entrante.stream = stream
	entrante.volume_db = -80.0
	entrante.play()

	if _tween:
		_tween.kill()
	_tween = create_tween().set_parallel(true)
	_tween.tween_property(_activo,  "volume_db", -80.0, FADE_DURATION)
	_tween.tween_property(entrante, "volume_db",   0.0, FADE_DURATION)
	await _tween.finished

	_activo.stop()
	_activo = entrante


func detener() -> void:
	_jugador_a.stop()
	_jugador_b.stop()
