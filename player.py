class Player:
    def __init__(self, name, clase):
        self.name = name
        self.clase = clase

        # Stats visibles (jugador cree que esto importa)
        self.stats = {
            "fuerza": 5,
            "mente": 5,
            "resistencia": 5
        }

        # Sistema oculto (LO REALMENTE IMPORTANTE)
        self.psique = {
            "violencia": 0,
            "miedo": 0,
            "culpa": 0,
            "lucidez": 0,
            "corrupcion": 0
        }

        # Estado del personaje
        self.alive = True
        self.level = 1

    # -------------------------
    # MODIFICADORES DE PSIQUE
    # -------------------------
    def modificar_psique(self, cambios):
        for clave, valor in cambios.items():
            if clave in self.psique:
                self.psique[clave] += valor

    # -------------------------
    # MODIFICADORES DE STATS
    # -------------------------
    def modificar_stats(self, cambios):
        for clave, valor in cambios.items():
            if clave in self.stats:
                self.stats[clave] += valor

    # -------------------------
    # MORIR
    # -------------------------
    def morir(self, razon=""):
        self.alive = False
        print(f"\n{self.name} ha muerto.")
        if razon:
            print(f"Causa: {razon}")

    # -------------------------
    # RESUMEN
    # -------------------------
    def mostrar_estado(self):
        print(f"\n=== {self.name} ===")
        print(f"Clase: {self.clase}")
        print("Stats:", self.stats)
        print("Psique:", self.psique)