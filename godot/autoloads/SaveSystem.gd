extends Node
## SaveSystem — 3 slots de guardado + New Game+.
## Equivale a save_system.py en la versión Pygame.
## Usa FileAccess de Godot 4 (no File — esa es API de Godot 3).

const NUM_SLOTS: int = 3
const SAVE_DIR: String = "user://saves/"
const NG_PLUS_FILE: String = "user://saves/ng_plus.json"


func _ruta(slot: int) -> String:
	return SAVE_DIR + "slot%d.json" % slot


func guardar_partida(player: Resource, nivel_index: int, slot: int = 0) -> void:
	DirAccess.make_dir_recursive_absolute(SAVE_DIR.trim_suffix("/"))
	# TODO Fase 1: serializar player a dict y guardarlo con FileAccess
	pass


func cargar_partida(slot: int = 0) -> Dictionary:
	var ruta := _ruta(slot)
	if not FileAccess.file_exists(ruta):
		return {}
	var f := FileAccess.open(ruta, FileAccess.READ)
	if f == null:
		return {}
	var data = JSON.parse_string(f.get_as_text())
	f.close()
	if data is Dictionary:
		return data
	return {}


func borrar_partida(slot: int = 0) -> void:
	var ruta := _ruta(slot)
	if FileAccess.file_exists(ruta):
		DirAccess.remove_absolute(ruta)


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


func guardar_ng_plus(psique: Dictionary) -> void:
	DirAccess.make_dir_recursive_absolute(SAVE_DIR.trim_suffix("/"))
	var f := FileAccess.open(NG_PLUS_FILE, FileAccess.WRITE)
	if f:
		f.store_string(JSON.stringify({"psique_heredada": psique}))
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
