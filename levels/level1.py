from enemies import crear_guardian

class Level1:

    def __init__(self):
        self.nombre = "La Cueva del Origen"

    # ─────────────────────────────────────────
    # FASE 1 — COMBATE
    # ─────────────────────────────────────────
    def fase_combate(self, player, engine):
        enemy = crear_guardian()
        return engine.combate_narrativo(enemy)

    # ─────────────────────────────────────────
    # FASE 2 — DECISIÓN PSICOLÓGICA
    # ─────────────────────────────────────────
    def fase_psicologica(self, player, engine):

        player.recuperar(vida=8, energia=15)

        texto = """
Te adentras en la cueva.
No hay antorchas. No hay sonido.
Solo oscuridad.
Algo… respira en la profundidad.
No lo ves, pero lo sentís.
Una voz, o tal vez un pensamiento que no es tuyo, susurra:
"Antes de la luz… ya estabas aquí."

¿Qué hacés?
"""

        eleccion = engine.mostrar_nivel(
            "assets/lvl1.jpg",
            texto,
            opciones=True,
            opciones_lista=[
                "Avanzar hacia la oscuridad",
                "Encender una antorcha",
                "Llamar para saber quién está ahí"
            ]
        )

        if eleccion == "1":
            player.psique["corrupcion"] += 10
            engine.mostrar_nivel(
                "assets/lvl1.jpg",
                """
Caminás sin ver.
Cada paso se siente… correcto.
Como si ya hubieras estado ahí antes.
La oscuridad no te rechaza.
Te envuelve.

La voz vuelve:
"Recordar es descender."
""",
                opciones=False
            )

        elif eleccion == "2":
            player.psique["lucidez"] += 10
            engine.mostrar_nivel(
                "assets/lvl1.jpg",
                """
La antorcha enciende.
La luz revela paredes húmedas…
y marcas.
No son naturales.
Son manos.
Cientos de ellas.
Marcadas desde adentro.

La voz susurra:
"La luz no revela. Delata."
""",
                opciones=False
            )

        elif eleccion == "3":
            player.psique["miedo"] += 15
            engine.mostrar_nivel(
                "assets/lvl1.jpg",
                """
Tu voz se pierde.
Pero algo responde.
No con sonido.
Con presencia.
Ahora sabés que no estás solo.
Y nunca lo estuviste.
""",
                opciones=False
            )

    # ─────────────────────────────────────────
    # ENTRY POINT
    # ─────────────────────────────────────────
    def jugar(self, player, engine):
        resultado = self.fase_combate(player, engine)
        if resultado == "muerte":
            return "muerte"

        self.fase_psicologica(player, engine)
        return "continuar"
