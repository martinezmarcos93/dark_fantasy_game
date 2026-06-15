class_name CombatState
extends Resource
## CombatState — estado mutable de un combate.
## Port directo de CombatState en combat_system.py.
## Se crea al inicio de cada pelea y se descarta al terminar.

## Port fiel de combat_system.HECHIZOS. Las claves coinciden con el Python
## (costo_energia, descripcion) porque acciones_disponibles() las usa.
const HECHIZOS := [
	{"id": "fuego",      "nombre": "Palabra de Fuego",     "descripcion": "Daño directo alto",          "efecto": "daño_alto", "costo_energia": 15, "inmune": []},
	{"id": "velo",       "nombre": "Velo de Sombra",       "descripcion": "Reduce daño esta ronda",     "efecto": "defensa",   "costo_energia": 10, "inmune": []},
	{"id": "resonancia", "nombre": "Resonancia Mental",    "descripcion": "Ventaja en siguiente tirada","efecto": "ventaja",   "costo_energia": 10, "inmune": []},
	{"id": "nombre",     "nombre": "Nombre Verdadero",     "descripcion": "Paraliza al enemigo una ronda","efecto": "paralizar","costo_energia": 20, "inmune": ["sacerdote"]},
	{"id": "abismo",     "nombre": "Fragmento del Abismo", "descripcion": "Daño masivo — te daña también","efecto": "nuclear", "costo_energia": 40, "inmune": []},
]

var ronda_actual: int = 1
var rondas_max: int = 3

var rondas_jugador: int = 0
var rondas_enemigo: int = 0

var en_posicion: bool = false       # Ladrón en posición tras Observar

var hechizos_disponibles: Array = []
var _hechizos_originales: Array = []

var golpe_cargado_disponible: bool = true
var furia_disponible: bool = true
var defensas_consecutivas: int = 0
var contraataque_disponible: bool = false

var defensa_activa: bool = false
var ventaja_activa: bool = false
var enemigo_paralizado: bool = false
var _paralizado_siguiente: bool = false
var proximo_defender_exito: bool = false  # Piedra de Eco

var daño_jugador_total: int = 0
var daño_enemigo_total: int = 0

var acciones_jugador: Array = []

var uso_especiales: bool = false
var huyo: bool = false


func inicializar(player: Resource, p_rondas_max: int = 3) -> void:
	rondas_max = p_rondas_max
	var nivel: int = player.level

	var desbloqueados := ["fuego", "velo", "resonancia"]
	if nivel >= 3:
		desbloqueados.append("nombre")
	if nivel >= 4:
		desbloqueados.append("abismo")

	hechizos_disponibles = desbloqueados.duplicate()
	_hechizos_originales = desbloqueados.duplicate()


func hechizo_por_id(id: String) -> Dictionary:
	for h in HECHIZOS:
		if h["id"] == id:
			return h
	return {}
