class_name Enemy
extends Resource
## Enemy — datos de un enemigo.
## Port directo de la clase Enemy en combat_system.py.
## Las instancias las crea EnemyFactory.gd.

@export var nombre: String = ""
@export var id_enemigo: String = ""
@export var imagen: String = ""
@export var vida: int = 0
@export var vida_max: int = 0
@export var dificultad: int = 0

@export var texto_intro: String = ""
@export var textos_ataque: Dictionary = {}    # situacion → String o {clase → String}
@export var textos_derrota: String = ""
@export var textos_victoria: String = ""
@export var texto_empate: String = ""

@export var psique_victoria_jugador: Dictionary = {}
@export var psique_derrota_jugador: Dictionary = {}
@export var inmunidades: Array = []
@export var rondas_max: int = 3


func inicializar(
	p_nombre: String, p_id: String, p_imagen: String,
	p_vida: int, p_dificultad: int,
	p_intro: String, p_ataques: Dictionary,
	p_derrota: String, p_victoria: String, p_empate: String,
	p_psique_victoria: Dictionary, p_psique_derrota: Dictionary,
	p_inmunidades: Array = [], p_rondas: int = 3
) -> void:
	nombre    = p_nombre
	id_enemigo = p_id
	imagen    = p_imagen
	vida      = p_vida
	vida_max  = p_vida
	dificultad = p_dificultad
	texto_intro     = p_intro
	textos_ataque   = p_ataques
	textos_derrota  = p_derrota
	textos_victoria = p_victoria
	texto_empate    = p_empate
	psique_victoria_jugador = p_psique_victoria
	psique_derrota_jugador  = p_psique_derrota
	inmunidades = p_inmunidades
	rondas_max  = p_rondas


func esta_debilitado() -> bool:
	return vida < vida_max * 0.4


## Resuelve el texto de ataque según situación y clase del jugador.
## Si el valor es un Dict (por clase), busca la clase o cae a "_".
## Si es String, lo devuelve directamente.
func texto_para_ataque(situacion: String, clase: String) -> String:
	var entry = textos_ataque.get(situacion, textos_ataque.get("default", "Ataca."))
	if entry is Dictionary:
		return entry.get(clase, entry.get("_", "Ataca."))
	return str(entry)


## Elige la acción del enemigo según el contexto del combate.
## Port directo de Enemy.elegir_accion() en combat_system.py.
func elegir_accion(state: Resource, clase_jugador: String) -> String:
	if state.enemigo_paralizado:
		return "paralizado"

	if clase_jugador == "Ladrón" and state.en_posicion:
		if "detectar_sigilo" in textos_ataque:
			return "detectar_sigilo"

	if esta_debilitado():
		if "desesperado" in textos_ataque:
			return "desesperado"

	var historial: Array = state.acciones_jugador
	if historial.size() >= 2 and historial[-1] == historial[-2]:
		var repetida: String = historial[-1]
		if repetida in ["defender", "velo", "observar", "respirar"]:
			if "presencia_psiquica" in textos_ataque:
				return "presencia_psiquica"
		if repetida in ["golpe_directo", "fuego", "ataque_rapido"]:
			if "ataque_pesado" in textos_ataque:
				return "ataque_pesado"

	var excluir := ["detectar_sigilo", "desesperado", "paralizado"]
	var patrones := textos_ataque.keys().filter(func(k): return k not in excluir)
	if patrones.is_empty():
		return "default"
	return patrones[(state.ronda_actual - 1) % patrones.size()]
