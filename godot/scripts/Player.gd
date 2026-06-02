class_name Player
extends Resource
## Player — datos del jugador.
## Port directo de game/player.py.
## Es un Resource (datos puros, sin nodo visual).
##
## IMPORTANTE: el comportamiento debe ser idéntico al Python.
## Referencia: game/player.py | Contrato: test_game.py (96 tests)

# ─────────────────────────────────────────
# CONSTANTES DE CLASE
# ─────────────────────────────────────────
const CLASES := {
	"Guerrero": {
		"fuerza": 8, "mente": 3, "resistencia": 7,
		"vida_max": 120, "energia_max": 40, "energia_nombre": "Stamina"
	},
	"Hechicero": {
		"fuerza": 3, "mente": 9, "resistencia": 4,
		"vida_max": 70, "energia_max": 100, "energia_nombre": "Magia"
	},
	"Ladrón": {
		"fuerza": 6, "mente": 6, "resistencia": 5,
		"vida_max": 90, "energia_max": 70, "energia_nombre": "Ingenio"
	},
	"Errante": {
		"fuerza": 5, "mente": 5, "resistencia": 5,
		"vida_max": 80, "energia_max": 60, "energia_nombre": "Energía"
	},
}

const NOMBRES_ITEMS := {
	"antorcha": "Antorcha", "sal": "Sal Consagrada", "vendas": "Vendas Viejas",
	"espejo": "Fragmento de Espejo", "tinta": "Tinta del Abismo",
	"sangre": "Sangre Seca", "eco_piedra": "Piedra de Eco",
	"mapa": "Mapa Roto", "elixir": "Elixir del Olvido",
}

# ─────────────────────────────────────────
# PROPIEDADES
# ─────────────────────────────────────────
@export var name_jugador: String = ""
@export var clase: String = ""

@export var stats: Dictionary = {}
@export var vida_max: int = 0
@export var vida: int = 0
@export var energia_max: int = 0
@export var energia: int = 0
@export var energia_nombre: String = ""

@export var psique: Dictionary = {
	"violencia": 0, "miedo": 0, "culpa": 0,
	"lucidez": 0, "corrupcion": 0
}

@export var alive: bool = true
@export var level: int = 1
@export var historial: Array = []
@export var stats_combate: Dictionary = {
	"daño_infligido": 0, "daño_recibido": 0,
	"rondas_ganadas": 0, "rondas_perdidas": 0,
	"criticos": 0, "acciones": {},
}

# Aliento del Umbral y nuevas mecánicas
@export var aliento: int = 0
@export var inventario: Array = []
@export var llave_piedra: bool = false
@export var aliado_tipo: String = ""
@export var viajero_activo: bool = false
@export var viajero_usado: bool = false
@export var fusionado_con_otro: bool = false
@export var memorias_gastadas: int = 0
@export var ultimo_combate_perfecto: bool = false
@export var cofre_umbral_disponible: bool = true


# ─────────────────────────────────────────
# INICIALIZACIÓN
# ─────────────────────────────────────────
func inicializar(p_name: String, p_clase: String) -> void:
	name_jugador = p_name
	clase = p_clase
	var base: Dictionary = CLASES.get(p_clase, CLASES["Errante"])
	stats = {
		"fuerza": base["fuerza"],
		"mente": base["mente"],
		"resistencia": base["resistencia"],
	}
	vida_max    = base["vida_max"]
	vida        = base["vida_max"]
	energia_max = base["energia_max"]
	energia     = base["energia_max"]
	energia_nombre = base["energia_nombre"]


# ─────────────────────────────────────────
# PSIQUE
# ─────────────────────────────────────────
func modificar_psique(cambios: Dictionary) -> void:
	for clave in cambios:
		if clave in psique:
			psique[clave] = clamp(psique[clave] + cambios[clave], 0, 100)


func psique_equilibrada() -> bool:
	var valores := psique.values()
	return valores.max() - valores.min() <= 10


# ─────────────────────────────────────────
# VIDA Y ENERGÍA
# ─────────────────────────────────────────
func recibir_daño(cantidad: int) -> int:
	var reduccion: float = stats["resistencia"] * 0.02
	var daño_real: int = max(1, int(cantidad * (1.0 - reduccion)))
	vida = max(0, vida - daño_real)
	if vida <= 0:
		alive = false
	return daño_real


func gastar_energia(cantidad: int) -> void:
	energia = max(0, energia - cantidad)


func recuperar(p_vida: int = 0, p_energia: int = 0) -> void:
	vida    = min(vida_max,    vida    + p_vida)
	energia = min(energia_max, energia + p_energia)


# ─────────────────────────────────────────
# ALIENTO
# ─────────────────────────────────────────
func ganar_aliento(cantidad: int = 1) -> void:
	aliento = min(10, aliento + cantidad)


func gastar_aliento(cantidad: int) -> bool:
	if aliento >= cantidad:
		aliento -= cantidad
		return true
	return false


# ─────────────────────────────────────────
# INVENTARIO
# ─────────────────────────────────────────
func agregar_item(id_item: String) -> bool:
	if inventario.size() >= 3:
		return false
	inventario.append(id_item)
	return true


func tiene_item(id_item: String) -> bool:
	return id_item in inventario


func quitar_item(id_item: String) -> void:
	inventario.erase(id_item)


# ─────────────────────────────────────────
# HISTORIAL Y MEMORIAS
# ─────────────────────────────────────────
func registrar_decision(descripcion: String) -> void:
	historial.append(descripcion)


func gastar_memoria(indice: int) -> bool:
	if indice >= 0 and indice < historial.size():
		historial.remove_at(indice)
		memorias_gastadas += 1
		return true
	return false


func contar_usos_accion(id_accion: String) -> int:
	return stats_combate["acciones"].get(id_accion, 0)


func morir(razon: String = "") -> void:
	alive = false
