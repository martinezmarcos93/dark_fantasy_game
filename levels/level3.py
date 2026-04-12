from enemies import crear_sacerdote

class Level3:

    def __init__(self):
        self.nombre = "El Ritual de la Entrega"

    # ─────────────────────────────────────────
    # FASE 1 — COMBATE (diferenciado por clase)
    # Enemigo: El Sacerdote Sin Rostro
    # ─────────────────────────────────────────
    def fase_combate(self, player, engine):
        from enemies import crear_sacerdote
        enemy = crear_sacerdote()
        return engine.combate_narrativo(enemy)

    def fase_psicologica(self, player, engine):

        player.recuperar(vida=6, energia=12)

        texto = """
La cueva se abre en una sala amplia.
El aire es pesado.
Antiguo.
En el centro hay un altar de piedra.
Encima… un libro.
Sus páginas están en blanco.
Pero algo se escribe lentamente.
No con tinta.
Con algo más denso.

La voz susurra:
"Para comprender… tenés que entregar."

¿Qué hacés?
"""

        eleccion = engine.mostrar_nivel(
            "assets/lvl3.jpg",
            texto,
            opciones=True,
            opciones_lista=[
                "Leer el libro",
                "Ofrecer tu sangre",
                "Ignorar el altar y seguir"
            ]
        )

        if eleccion == "1":
            player.psique["lucidez"] += 15
            player.psique["corrupcion"] += 5
            engine.mostrar_nivel(
                "assets/lvl3.jpg",
                """
Leés.
Las palabras no están escritas.
Se forman mientras las mirás.
Y hablan de vos.
De cosas que no recordabas…
pero que son ciertas.
Cada línea te revela.
Pero también te cambia.
""",
                opciones=False
            )

        elif eleccion == "2":
            player.psique["corrupcion"] += 20
            engine.mostrar_nivel(
                "assets/lvl3.jpg",
                """
Apoyás tu mano.
La piedra está tibia.
La sangre fluye.
El libro responde.
Las páginas se llenan.
Pero no con conocimiento.
Con aceptación.
Algo en vos… ya eligió.
""",
                opciones=False
            )

        elif eleccion == "3":
            player.psique["miedo"] += 10
            engine.mostrar_nivel(
                "assets/lvl3.jpg",
                """
Te alejás.
Pero el altar no desaparece.
Lo sentís.
Como una decisión no tomada.
Como algo pendiente.
Y sabés…
que lo vas a volver a ver.
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
