extends Node
## GameEngine — director global del juego.
## Equivale a game_engine.py en la versión Pygame.
## Registrado como Autoload: siempre disponible como GameEngine.singleton.

# Nivel actual (0-based, igual que Python)
var current_level_index: int = 0
var player: Resource       # instancia de Player (Resource)
var modo_lectura: bool = false
var dificultad_global: float = 1.0
var huyo_este_nivel: bool = false

# Referencia a la pantalla de juego activa
var pantalla_activa = null

func _ready() -> void:
	# El GameEngine no carga nada hasta que el Menu lo indica
	pass


# ─────────────────────────────────────────
# CAMBIAR DE ESCENA
# ─────────────────────────────────────────
func ir_a_escena(ruta: String) -> void:
	get_tree().change_scene_to_file(ruta)


func ir_a_nivel(indice: int) -> void:
	current_level_index = indice
	var ruta = "res://scenes/levels/Level%d.tscn" % (indice + 1)
	ir_a_escena(ruta)


# ─────────────────────────────────────────
# FINALES (port de determinar_final())
# Se porta completo en Fase 1 — por ahora stub
# ─────────────────────────────────────────
func determinar_final() -> String:
	# TODO Fase 1: portar desde game_engine.py → determinar_final()
	return "[ Final pendiente de implementar ]"
