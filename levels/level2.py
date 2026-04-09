class Level2:
    def __init__(self):
        self.nombre = "El Espejo de las Formas"

class Level2:

    def jugar(self, player, engine):

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

1. Mirar fijamente el espejo
2. Romper el espejo
3. Dar la espalda y seguir
"""

        eleccion = engine.mostrar_nivel("assets/lvl2.jpg", texto)

        # -------------------------
        # DECISIONES
        # -------------------------

        if eleccion == "1":
            player.psique["lucidez"] += 15

            texto_resultado = """
Te acercás.

Tu reflejo no te copia.

Se adelanta.

Sonríe antes que vos.

Y entonces entendés…

No estás mirando.

Estás siendo observado.
"""

            engine.mostrar_nivel("assets/lvl2.jpg", texto_resultado)
            return "continuar"

        elif eleccion == "2":
            player.psique["violencia"] += 15

            texto_resultado = """
Golpeás el espejo.

Se rompe.

Pero no desaparece.

Cada fragmento sigue reflejando.

Versiones tuyas.

Peores.

Más sinceras.

La voz:
"Romper no elimina."
"""

            engine.mostrar_nivel("assets/lvl2.jpg", texto_resultado)
            return "continuar"

        elif eleccion == "3":
            player.psique["miedo"] += 10

            texto_resultado = """
Das la espalda.

Pero sentís la mirada.

El reflejo no depende del espejo.

Ahora está en vos.

Y no podés dejar de sentirlo.
"""

            engine.mostrar_nivel("assets/lvl2.jpg", texto_resultado)
            return "continuar"

        return "muerte"