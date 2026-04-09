class Level6:
    def __init__(self):
        self.nombre = "El Umbral Final"

    def distorsionar_texto(self, texto, player):
        psique = player.psique

        # Distorsión más intensa que en level 5
        if psique["miedo"] > 40:
            texto = texto.lower()
            texto = texto.replace(" ", "...")

        if psique["corrupcion"] > 50:
            texto = texto.replace("o", "ø").replace("e", "ë")

        if psique["lucidez"] > 50:
            texto = "/// " + texto + " ///"

        return texto

class Level6:

    def jugar(self, player, engine):

        texto = """
No hay más puertas.

No hay más caminos.

No hay cueva.

No hay voz.

Solo vos.

O lo que queda.

Frente a vos…

hay algo.

Tiene tu forma.

Pero no te copia.

Respira con vos.

Piensa con vos.

Sabe todo lo que hiciste.

Y no te juzga.

Solo espera.

¿Qué hacés?

1. Aceptarlo
2. Negarlo
3. Destruirlo
"""

        eleccion = engine.mostrar_nivel("assets/lvl6.jpg", texto)

        # -------------------------
        # DECISION FINAL
        # -------------------------

        if eleccion == "1":
            player.psique["lucidez"] += 20

            texto_resultado = """
No resistís.

No luchás.

Lo mirás.

Y lo aceptás.

No desaparece.

Se integra.

Por primera vez…

no hay conflicto.

Solo totalidad.
"""

            engine.mostrar_nivel("assets/lvl6.jpg", texto_resultado)
            return "continuar"

        elif eleccion == "2":
            player.psique["miedo"] += 20
            player.psique["culpa"] += 10

            texto_resultado = """
Negás.

Intentás separarte.

Decir que eso no sos vos.

Pero no se va.

Se distorsiona.

Se vuelve más presente.

Más inevitable.

Porque no podés negar lo que sos.
"""

            engine.mostrar_nivel("assets/lvl6.jpg", texto_resultado)
            return "continuar"

        elif eleccion == "3":
            player.psique["violencia"] += 20
            player.psique["corrupcion"] += 15

            texto_resultado = """
Atacás.

Sin dudar.

Con todo.

Pero no hay impacto.

Porque no hay distancia.

Cada golpe…

es interno.

Y algo empieza a romperse.

Pero no es eso.

Sos vos.
"""

            engine.mostrar_nivel("assets/lvl6.jpg", texto_resultado)
            return "continuar"

        return "muerte"