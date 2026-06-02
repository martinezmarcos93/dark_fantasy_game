import json
import os

SAVE_DIR    = "saves"
NUM_SLOTS   = 3
NG_PLUS_FILE = "saves/ng_plus.json"

def _ruta(slot):
    os.makedirs(SAVE_DIR, exist_ok=True)
    return os.path.join(SAVE_DIR, f"slot{slot}.json")

def guardar_partida(player, nivel_index, slot=0):
    data = {
        "nombre":     player.name,
        "clase":      player.clase,
        "nivel_actual": nivel_index,
        "alive":      player.alive,
        "stats":      player.stats,
        "psique":     player.psique,
        "vida":       player.vida,
        "vida_max":   player.vida_max,
        "energia":    player.energia,
        "energia_max": player.energia_max,
        "historial":      player.historial,
        "stats_combate":  player.stats_combate,
        # Nuevos campos
        "aliento":                   player.aliento,
        "inventario":                player.inventario,
        "llave_piedra":              player.llave_piedra,
        "aliado_tipo":               player.aliado_tipo,
        "viajero_activo":            player.viajero_activo,
        "viajero_usado":             player.viajero_usado,
        "fusionado_con_otro":        player.fusionado_con_otro,
        "memorias_gastadas":         player.memorias_gastadas,
        "ultimo_combate_perfecto":   player.ultimo_combate_perfecto,
        "cofre_umbral_disponible":   player.cofre_umbral_disponible,
    }
    with open(_ruta(slot), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def cargar_partida(slot=0):
    ruta = _ruta(slot)
    if not os.path.exists(ruta):
        return None
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return None

def listar_slots():
    slots = []
    for i in range(NUM_SLOTS):
        data = cargar_partida(i)
        if data:
            slots.append({
                "slot":   i,
                "nombre": data.get("nombre", "???"),
                "clase":  data.get("clase",  "???"),
                "nivel":  data.get("nivel_actual", 0),
                "vacio":  False,
            })
        else:
            slots.append({"slot": i, "vacio": True})
    return slots

def existe_partida(slot=0):
    return os.path.exists(_ruta(slot))

def borrar_partida(slot=0):
    ruta = _ruta(slot)
    if os.path.exists(ruta):
        os.remove(ruta)

def guardar_ng_plus(psique):
    os.makedirs(SAVE_DIR, exist_ok=True)
    with open(NG_PLUS_FILE, "w", encoding="utf-8") as f:
        json.dump({"psique_heredada": psique}, f, ensure_ascii=False, indent=2)

def cargar_ng_plus():
    if not os.path.exists(NG_PLUS_FILE):
        return None
    try:
        with open(NG_PLUS_FILE, "r", encoding="utf-8") as f:
            return json.load(f).get("psique_heredada")
    except (json.JSONDecodeError, OSError):
        return None

def existe_ng_plus():
    return os.path.exists(NG_PLUS_FILE)
