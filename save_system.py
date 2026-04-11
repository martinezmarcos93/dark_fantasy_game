import json
import os

SAVE_FILE = "savegame.json"

# ─────────────────────────────────────────
# GUARDAR PARTIDA
# ─────────────────────────────────────────
def guardar_partida(player, nivel_index):
    data = {
        "nombre": player.name,
        "clase": player.clase,
        "nivel_actual": nivel_index,
        "alive": player.alive,
        "stats": player.stats,
        "psique": player.psique
    }
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ─────────────────────────────────────────
# CARGAR PARTIDA
# ─────────────────────────────────────────
def cargar_partida():
    if not os.path.exists(SAVE_FILE):
        return None
    with open(SAVE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# ─────────────────────────────────────────
# EXISTE PARTIDA GUARDADA?
# ─────────────────────────────────────────
def existe_partida():
    return os.path.exists(SAVE_FILE)

# ─────────────────────────────────────────
# BORRAR PARTIDA (al iniciar nueva)
# ─────────────────────────────────────────
def borrar_partida():
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)
