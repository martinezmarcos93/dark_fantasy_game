class Level4:

    def __init__(self):
        self.nombre = "El Rey de las Sombras"

    def jugar(self, player, engine):

        texto = """
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
"No sos uno. Elegí."

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

        # -------------------------
        # DECISIONES
        # -------------------------

        if eleccion == "1":
            player.psique["lucidez"] += 20

            texto_resultado = """
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
"""

            engine.mostrar_nivel(
                "assets/lvl4.jpg",
                texto_resultado,
                opciones=False
            )
            return "continuar"

        elif eleccion == "2":
            player.psique["culpa"] += 15
            player.psique["miedo"] += 10

            texto_resultado = """
Negás.
Una por una.
Intentás borrar lo que no te gusta.
Pero no se van.
Se deforman.
Se vuelven más intensas.
Más presentes.

La voz susurra:
"Negar es alimentar."
"""

            engine.mostrar_nivel(
                "assets/lvl4.jpg",
                texto_resultado,
                opciones=False
            )
            return "continuar"

        elif eleccion == "3":
            player.psique["violencia"] += 20
            player.psique["corrupcion"] += 10

            texto_resultado = """
Atacás.
Golpeás.
Destruís.
Pero cada versión rota…
se multiplica.
Ahora son más.
Más agresivas.
Más reales.
Y ya no esperan.
"""

            engine.mostrar_nivel(
                "assets/lvl4.jpg",
                texto_resultado,
                opciones=False
            )
            return "continuar"

        return "muerte"