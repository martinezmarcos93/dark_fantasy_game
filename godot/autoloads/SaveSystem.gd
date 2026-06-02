extends Node
## SaveSystem — 3 slots de guardado + New Game+.
## Port completo de save_system.py usando FileAccess (API de Godot 4).
## NUNCA usar File — esa es API de Godot 3.

const NUM_SLOTS: int = 3
const SAVE_DIR: String = "user://saves/"
const NG_PLUS_FILE: String = "user://saves/ng_plus.json"


func _ruta(slot: int) -> String:
	return SAVE_DIR + "slot%d.json" % slot


# ─────────────────────────────────────────
# GUARDAR
# ─────────────────────────────────────────
func guardar_partida(player: Resource, nivel_index: int, slot: int = 0) -> void:
	DirAccess.make_dir_recursive_absolute(
		ProjectSettings.globalize_path(SAVE_DIR)
	)
	var data := {
		"nombre":       player.name_jugador,
		"clase":        player.clase,
		"nivel_actual": nivel_index,
		"alive":        player.alive,
		"stats":        player.stats,
		"psique":       player.psique,
		"vida":         player.vida,
		"vida_max":     player.vida_max,
		"energia":      player.energia,
		"energia_max":  player.energia_max,
		"historial":    player.historial,
		"stats_combate": player.stats_combate,
		# Nuevas mecánicas
		"aliento":                  player.aliento,
		"inventario":               player.inventario,
		"llave_piedra":             player.llave_piedra,
		"aliado_tipo":              player.aliado_tipo,
		"viajero_activo":           player.viajero_activo,
		"viajero_usado":            player.viajero_usado,
		"fusionado_con_otro":       player.fusionado_con_otro,
		"memorias_gastadas":        player.memorias_gastadas,
		"ultimo_combate_perfecto":  player.ultimo_combate_perfecto,
		"cofre_umbral_disponible":  player.cofre_umbral_disponible,
	}
	var f := FileAccess.open(_ruta(slot), FileAccess.WRITE)
	if f:
		f.store_string(JSON.stringify(data, "\t"))
		f.close()


# ─────────────────────────────────────────
# CARGAR
# ─────────────────────────────────────────
func cargar_partida(slot: int = 0) -> Dictionary:
	var ruta := _ruta(slot)
	if not FileAccess.file_exists(ruta):
		return {}
	var f := FileAccess.open(ruta, FileAccess.READ)
	if f == null:
		return {}
	var data = JSON.parse_string(f.get_as_text())
	f.close()
	return data if data is Dictionary else {}


func cargar_en_player(player: Resource, slot: int = 0) -> bool:
	var data := cargar_partida(slot)
	if data.is_empty():
		return false
	var req := ["nombre", "clase", "stats", "psique", "alive", "nivel_actual"]
	for k in req:
		if not k in data:
			return false

	player.inicializar(data["nombre"], data["clase"])
	player.stats  = data["stats"]
	player.psique = data["psique"]
	player.alive  = data["alive"]
	player.vida   = data.get("vida", player.vida_max)
	player.energia = data.get("energia", player.energia_max)
	player.historial      = data.get("historial", [])
	player.stats_combate  = data.get("stats_combate", player.stats_combate)
	player.aliento                 = data.get("aliento", 0)
	player.inventario              = data.get("inventario", [])
	player.llave_piedra            = data.get("llave_piedra", false)
	player.aliado_tipo             = data.get("aliado_tipo", "")
	player.viajero_activo          = data.get("viajero_activo", false)
	player.viajero_usado           = data.get("viajero_usado", false)
	player.fusionado_con_otro      = data.get("fusionado_con_otro", false)
	player.memorias_gastadas       = data.get("memorias_gastadas", 0)
	player.ultimo_combate_perfecto = data.get("ultimo_combate_perfecto", false)
	player.cofre_umbral_disponible = data.get("cofre_umbral_disponible", true)
	return true


# ─────────────────────────────────────────
# SLOTS
# ─────────────────────────────────────────
func listar_slots() -> Array:
	var result := []
	for i in range(NUM_SLOTS):
		var data := cargar_partida(i)
		if data.is_empty():
			result.append({"slot": i, "vacio": true})
		else:
			result.append({
				"slot":   i,
				"vacio":  false,
				"nombre": data.get("nombre", "???"),
				"clase":  data.get("clase",  "???"),
				"nivel":  data.get("nivel_actual", 0),
			})
	return result


func existe_partida(slot: int = 0) -> bool:
	return FileAccess.file_exists(_ruta(slot))


func borrar_partida(slot: int = 0) -> void:
	var ruta := _ruta(slot)
	if FileAccess.file_exists(ruta):
		DirAccess.remove_absolute(ProjectSettings.globalize_path(ruta))


# ─────────────────────────────────────────
# NEW GAME+
# ─────────────────────────────────────────
func guardar_ng_plus(psique: Dictionary) -> void:
	DirAccess.make_dir_recursive_absolute(
		ProjectSettings.globalize_path(SAVE_DIR)
	)
	var f := FileAccess.open(NG_PLUS_FILE, FileAccess.WRITE)
	if f:
		f.store_string(JSON.stringify({"psique_heredada": psique}, "\t"))
		f.close()


func cargar_ng_plus() -> Dictionary:
	if not FileAccess.file_exists(NG_PLUS_FILE):
		return {}
	var f := FileAccess.open(NG_PLUS_FILE, FileAccess.READ)
	if f == null:
		return {}
	var data = JSON.parse_string(f.get_as_text())
	f.close()
	if data is Dictionary:
		return data.get("psique_heredada", {})
	return {}


func existe_ng_plus() -> bool:
	return FileAccess.file_exists(NG_PLUS_FILE)
