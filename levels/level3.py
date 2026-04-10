class Level3:
    def __init__(self):
        self.nombre = "El Ritual de la Entrega"

class Level3:

    def jugar(self, player, engine):

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

1. Leer el libro
2. Ofrecer tu sangre
3. Ignorar el altar y seguir
"""

        eleccion = engine.mostrar_nivel("assets/lvl3.jpg", texto)

        # -------------------------
        # DECISIONES
        # -------------------------

        if eleccion == "1":
            player.psique["lucidez"] += 15
            player.psique["corrupcion"] += 5

            texto_resultado = """
Leés.
Las palabras no están escritas.
Se forman mientras las mirás.
Y hablan de vos.
De cosas que no recordabas…
pero que son ciertas.
Cada línea te revela.
Pero también te cambia.
"""

            engine.mostrar_nivel("assets/lvl3.jpg", texto_resultado)
            return "continuar"

        elif eleccion == "2":
            player.psique["corrupcion"] += 20

            texto_resultado = """
Apoyás tu mano.
La piedra está tibia.
La sangre fluye.
El libro responde.
Las páginas se llenan.
Pero no con conocimiento.
Con aceptación.
Algo en vos… ya eligió.
"""

            engine.mostrar_nivel("assets/lvl3.jpg", texto_resultado)
            return "continuar"

        elif eleccion == "3":
            player.psique["miedo"] += 10

            texto_resultado = """
Te alejás.
Pero el altar no desaparece.
Lo sentís.
Como una decisión no tomada.
Como algo pendiente.
Y sabés…
que lo vas a volver a ver.
"""

            engine.mostrar_nivel("assets/lvl3.jpg", texto_resultado)
            return "continuar"

        return "muerte"