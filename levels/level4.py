from enemies import crear_sombra

class Level4:

    def __init__(self):
        self.nombre = "El Rey de las Sombras"

    # ─────────────────────────────────────────
    # FASE 1 — COMBATE (diferenciado por clase)
    # Enemigo: La Sombra Soberana
    # El más difícil de los 4 — dificultad 6
    # ─────────────────────────────────────────
    def fase_combate(self, player, engine):
        from enemies import crear_sombra
        enemy = crear_sombra()
        return engine.combate_narrativo(enemy)

    def fase_psicologica(self, player, engine):

        player.recuperar(vida=5, energia=10)

        texto = f"""
El camino se estrecha.
Las paredes ya no son piedra.
Son… carne.
Respiran.
Late algo dentro.
Avanzás igual.
Llegás a una grieta.
Y ahí… los ves.
Versiones tuyas.
Distintas.
Una llora.
Otra sonríe.
Otra te observa con desprecio.

La voz dice:
"{player.name}. No sos uno. Elegí."

¿Qué hacés?
"""

        eleccion = engine.mostrar_nivel(
            "assets/lvl4.jpg",
            texto,
            opciones=True,
            opciones_lista=[
                "Aceptar todas las versiones",
                "Rechazar las versiones",
                "Atacar a las versiones"
            ]
        )

        if eleccion == "1":
            player.psique["lucidez"] += 20
            engine.mostrar_nivel(
                "assets/lvl4.jpg",
                """
No elegís.
Las aceptás.
Todas.
Las que duelen.
Las que avergüenzan.
Las que ocultabas.
No desaparecen.
Se alinean.
Y por un instante…
sos completo.
""",
                opciones=False
            )

        elif eleccion == "2":
            player.psique["culpa"] += 15
            player.psique["miedo"] += 10
            engine.mostrar_nivel(
                "assets/lvl4.jpg",
                """
Negás.
Una por una.
Intentás borrar lo que no te gusta.
Pero no se van.
Se deforman.
Se vuelven más intensas.
Más presentes.

La voz susurra:
"Negar es alimentar."
""",
                opciones=False
            )

        elif eleccion == "3":
            player.psique["violencia"] += 20
            player.psique["corrupcion"] += 10
            engine.mostrar_nivel(
                "assets/lvl4.jpg",
                """
Atacás.
Golpeás.
Destruís.
Pero cada versión rota…
se multiplica.
Ahora son más.
Más agresivas.
Más reales.
Y ya no esperan.
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
