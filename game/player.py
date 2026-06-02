import random

# IDs y nombres display de todos los ítems
NOMBRES_ITEMS = {
    "antorcha":   "Antorcha",
    "sal":        "Sal Consagrada",
    "vendas":     "Vendas Viejas",
    "espejo":     "Fragmento de Espejo",
    "tinta":      "Tinta del Abismo",
    "sangre":     "Sangre Seca",
    "eco_piedra": "Piedra de Eco",
    "mapa":       "Mapa Roto",
    "elixir":     "Elixir del Olvido",
}

# Ítems que pueden usarse entre combates (no en combate)
ITEMS_ENTRE_COMBATES = {"antorcha", "sal", "vendas", "espejo", "sangre", "mapa", "elixir"}
# Ítems de un solo uso
ITEMS_CONSUMIBLES = {"sal", "vendas", "espejo", "tinta", "eco_piedra", "mapa", "elixir"}
# Ítems que solo aplican dentro del combate
ITEMS_DE_COMBATE = {"tinta", "eco_piedra"}

# Tier de cada ítem (para cofres)
TIER_BASICO  = ["vendas", "antorcha", "sangre"]
TIER_MEDIO   = ["espejo", "mapa"]
TIER_ALTO    = ["tinta", "eco_piedra"]


class Player:

    CLASES = {
        "Guerrero": {
            "fuerza": 8,
            "mente":  3,
            "resistencia": 7,
            "vida_max": 120,
            "energia_max": 40,
            "energia_nombre": "Stamina"
        },
        "Hechicero": {
            "fuerza": 3,
            "mente":  9,
            "resistencia": 4,
            "vida_max": 70,
            "energia_max": 100,
            "energia_nombre": "Magia"
        },
        "Ladrón": {
            "fuerza": 6,
            "mente":  6,
            "resistencia": 5,
            "vida_max": 90,
            "energia_max": 70,
            "energia_nombre": "Ingenio"
        },
        "Errante": {
            "fuerza": 5,
            "mente":  5,
            "resistencia": 5,
            "vida_max": 80,
            "energia_max": 60,
            "energia_nombre": "Energía"
        }
    }

    def __init__(self, name, clase):
        self.name  = name
        self.clase = clase

        base = self.CLASES.get(clase, self.CLASES["Errante"])

        self.stats = {
            "fuerza":      base["fuerza"],
            "mente":       base["mente"],
            "resistencia": base["resistencia"]
        }

        self.vida_max     = base["vida_max"]
        self.vida         = base["vida_max"]
        self.energia_max  = base["energia_max"]
        self.energia      = base["energia_max"]
        self.energia_nombre = base["energia_nombre"]

        self.psique = {
            "violencia":  0,
            "miedo":      0,
            "culpa":      0,
            "lucidez":    0,
            "corrupcion": 0
        }

        self.alive = True
        self.level = 1
        self.historial = []
        self.stats_combate = {
            "daño_infligido":  0,
            "daño_recibido":   0,
            "rondas_ganadas":  0,
            "rondas_perdidas": 0,
            "criticos":        0,
            "acciones":        {},
        }

        # ── Nuevo: Aliento del Umbral ──────────────────────────
        self.aliento = 0

        # ── Nuevo: Inventario (max 3) ──────────────────────────
        self.inventario = []

        # ── Nuevo: Llave de Piedra (para cofres) ───────────────
        self.llave_piedra = False

        # ── Nuevo: Aliado (solo uno por run) ───────────────────
        self.aliado_tipo      = None   # "viajero" | "voz"
        self.viajero_activo   = False  # Viajero listo para el próximo combate
        self.viajero_usado    = False  # Viajero ya acompañó en un combate

        # ── Nuevo: Ending secreto ──────────────────────────────
        self.fusionado_con_otro = False

        # ── Nuevo: Memorias como moneda ───────────────────────
        self.memorias_gastadas = 0

        # ── Nuevo: Estado de último combate ───────────────────
        self.ultimo_combate_perfecto = False  # 3/3 rondas ganadas

        # ── Nuevo: Cofre del Umbral (1 por run) ───────────────
        self.cofre_umbral_disponible = True

    # ─────────────────────────────────────────
    # PSIQUE
    # ─────────────────────────────────────────
    def modificar_psique(self, cambios):
        for clave, valor in cambios.items():
            if clave in self.psique:
                self.psique[clave] = max(0, min(100, self.psique[clave] + valor))

    def psique_equilibrada(self):
        """True si todos los valores de psique están dentro de un rango de 10 puntos."""
        valores = list(self.psique.values())
        return max(valores) - min(valores) <= 10

    # ─────────────────────────────────────────
    # STATS
    # ─────────────────────────────────────────
    def modificar_stats(self, cambios):
        for clave, valor in cambios.items():
            if clave in self.stats:
                self.stats[clave] += valor

    # ─────────────────────────────────────────
    # VIDA Y ENERGÍA
    # ─────────────────────────────────────────
    def recibir_daño(self, cantidad):
        reduccion = self.stats["resistencia"] * 0.02
        daño_real = int(cantidad * (1 - reduccion))
        daño_real = max(1, daño_real)
        self.vida = max(0, self.vida - daño_real)
        if self.vida <= 0:
            self.alive = False
        return daño_real

    def gastar_energia(self, cantidad):
        self.energia = max(0, self.energia - cantidad)

    def recuperar(self, vida=0, energia=0):
        self.vida    = min(self.vida_max,    self.vida    + vida)
        self.energia = min(self.energia_max, self.energia + energia)

    # ─────────────────────────────────────────
    # ALIENTO DEL UMBRAL
    # ─────────────────────────────────────────
    def ganar_aliento(self, cantidad=1):
        self.aliento = min(10, self.aliento + cantidad)

    def gastar_aliento(self, cantidad):
        if self.aliento >= cantidad:
            self.aliento -= cantidad
            return True
        return False

    # ─────────────────────────────────────────
    # INVENTARIO
    # ─────────────────────────────────────────
    def agregar_item(self, id_item):
        if len(self.inventario) >= 3:
            return False
        self.inventario.append(id_item)
        return True

    def tiene_item(self, id_item):
        return id_item in self.inventario

    def quitar_item(self, id_item):
        if id_item in self.inventario:
            self.inventario.remove(id_item)

    # ─────────────────────────────────────────
    # MEMORIAS COMO MONEDA
    # ─────────────────────────────────────────
    def gastar_memoria(self, indice):
        if 0 <= indice < len(self.historial):
            self.historial.pop(indice)
            self.memorias_gastadas += 1
            return True
        return False

    # ─────────────────────────────────────────
    # ESTADÍSTICAS DE COMBATE
    # ─────────────────────────────────────────
    def contar_usos_accion(self, id_accion):
        return self.stats_combate["acciones"].get(id_accion, 0)

    # ─────────────────────────────────────────
    # HISTORIAL
    # ─────────────────────────────────────────
    def registrar_decision(self, descripcion):
        self.historial.append(descripcion)

    def morir(self, razon=""):
        self.alive = False

    # ─────────────────────────────────────────
    # DEBUG
    # ─────────────────────────────────────────
    def mostrar_estado(self):
        print(f"\n=== {self.name} ({self.clase}) ===")
        print(f"Vida: {self.vida}/{self.vida_max}")
        print(f"{self.energia_nombre}: {self.energia}/{self.energia_max}")
        print(f"Aliento del Umbral: {self.aliento}/10")
        print("Stats:", self.stats)
        print("Psique:", self.psique)
        print("Inventario:", self.inventario)
