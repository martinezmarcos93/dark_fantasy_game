import json
import os

SAVE_DIR  = "saves"
NUM_SLOTS = 3

def _ruta(slot):
    os.makedirs(SAVE_DIR, exist_ok=True)
    return os.path.join(SAVE_DIR, f"slot{slot}.json")

# ─────────────────────────────────────────
# GUARDAR PARTIDA
# ─────────────────────────────────────────
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
        "historial":  player.historial,
    }
    with open(_ruta(slot), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ─────────────────────────────────────────
# CARGAR PARTIDA
# ─────────────────────────────────────────
def cargar_partida(slot=0):
    ruta = _ruta(slot)
    if not os.path.exists(ruta):
        return None
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return None

# ─────────────────────────────────────────
# RESUMEN DE TODOS LOS SLOTS
# Devuelve lista de dicts con info rápida para el menú de carga
# ─────────────────────────────────────────
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

# ─────────────────────────────────────────
# EXISTE PARTIDA EN SLOT?
# ─────────────────────────────────────────
def existe_partida(slot=0):
    return os.path.exists(_ruta(slot))

# ─────────────────────────────────────────
# BORRAR PARTIDA
# ─────────────────────────────────────────
def borrar_partida(slot=0):
    ruta = _ruta(slot)
    if os.path.exists(ruta):
        os.remove(ruta)
