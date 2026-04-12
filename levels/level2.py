from enemies import crear_reflejo

class Level2:

    def __init__(self):
        self.nombre = "El Espejo de las Formas"

    # ─────────────────────────────────────────
    # FASE 1 — COMBATE (diferenciado por clase)
    # Enemigo: El Reflejo Armado
    # ─────────────────────────────────────────
    def fase_combate(self, player, engine):
        from enemies import crear_reflejo
        enemy = crear_reflejo()
        return engine.combate_narrativo(enemy)

    def fase_psicologica(self, player, engine):

        player.recuperar(vida=8, energia=15)

        texto = """
Avanzás más profundo en la cueva.
El aire cambia. Es más denso.
Llegás a una cámara circular.
En el centro… hay un espejo.
Pero no refleja tu cuerpo.
Refleja… algo más.
La voz regresa:
"No sos lo que creés. Mirá."

¿Qué hacés?
"""

        eleccion = engine.mostrar_nivel(
            "assets/lvl2.jpg",
            texto,
            opciones=True,
            opciones_lista=[
                "Mirar fijamente el espejo",
                "Romper el espejo",
                "Dar la espalda y seguir"
            ]
        )

        if eleccion == "1":
            player.psique["lucidez"] += 15
            engine.mostrar_nivel(
                "assets/lvl2.jpg",
                """
Te acercás.
Tu reflejo no te copia.
Se adelanta.
Sonríe antes que vos.
Y entonces entendés…
No estás mirando.
Estás siendo observado.
""",
                opciones=False
            )

        elif eleccion == "2":
            player.psique["violencia"] += 15
            engine.mostrar_nivel(
                "assets/lvl2.jpg",
                """
Golpeás el espejo.
Se rompe.
Pero no desaparece.
Cada fragmento sigue reflejando.
Versiones tuyas.
Peores.
Más sinceras.

La voz:
"Romper no elimina."
""",
                opciones=False
            )

        elif eleccion == "3":
            player.psique["miedo"] += 10
            engine.mostrar_nivel(
                "assets/lvl2.jpg",
                """
Das la espalda.
Pero sentís la mirada.
El reflejo no depende del espejo.
Ahora está en vos.
Y no podés dejar de sentirlo.
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
