class Player:

    # Stats base por clase
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
        # Fallback por si acaso
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

        # Stats visibles
        self.stats = {
            "fuerza":      base["fuerza"],
            "mente":       base["mente"],
            "resistencia": base["resistencia"]
        }

        # Vida y energía
        self.vida_max     = base["vida_max"]
        self.vida         = base["vida_max"]
        self.energia_max  = base["energia_max"]
        self.energia      = base["energia_max"]
        self.energia_nombre = base["energia_nombre"]

        # Sistema oculto (el núcleo del juego)
        self.psique = {
            "violencia":  0,
            "miedo":      0,
            "culpa":      0,
            "lucidez":    0,
            "corrupcion": 0
        }

        self.alive = True
        self.level = 1

    # ─────────────────────────────────────────
    # MODIFICAR PSIQUE
    # ─────────────────────────────────────────
    def modificar_psique(self, cambios):
        for clave, valor in cambios.items():
            if clave in self.psique:
                self.psique[clave] = max(0, self.psique[clave] + valor)

    # ─────────────────────────────────────────
    # MODIFICAR STATS
    # ─────────────────────────────────────────
    def modificar_stats(self, cambios):
        for clave, valor in cambios.items():
            if clave in self.stats:
                self.stats[clave] += valor

    # ─────────────────────────────────────────
    # RECIBIR DAÑO
    # ─────────────────────────────────────────
    def recibir_daño(self, cantidad):
        # La resistencia mitiga el daño (cada punto reduce 2%)
        reduccion = self.stats["resistencia"] * 0.02
        daño_real = int(cantidad * (1 - reduccion))
        daño_real = max(1, daño_real)           # mínimo 1 de daño siempre
        self.vida = max(0, self.vida - daño_real)
        if self.vida <= 0:
            self.alive = False
        return daño_real

    # ─────────────────────────────────────────
    # GASTAR ENERGÍA
    # ─────────────────────────────────────────
    def gastar_energia(self, cantidad):
        self.energia = max(0, self.energia - cantidad)

    # ─────────────────────────────────────────
    # RECUPERAR (parcial, entre niveles)
    # ─────────────────────────────────────────
    def recuperar(self, vida=0, energia=0):
        self.vida    = min(self.vida_max,    self.vida    + vida)
        self.energia = min(self.energia_max, self.energia + energia)

    # ─────────────────────────────────────────
    # MORIR
    # ─────────────────────────────────────────
    def morir(self, razon=""):
        self.alive = False

    # ─────────────────────────────────────────
    # RESUMEN (debug)
    # ─────────────────────────────────────────
    def mostrar_estado(self):
        print(f"\n=== {self.name} ({self.clase}) ===")
        print(f"Vida: {self.vida}/{self.vida_max}")
        print(f"{self.energia_nombre}: {self.energia}/{self.energia_max}")
        print("Stats:", self.stats)
        print("Psique:", self.psique)
