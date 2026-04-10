class Level5:
    def __init__(self):
        self.nombre = "Las Moradas de los Muertos"

    def distorsionar_texto(self, texto, player):
        psique = player.psique

        # Distorsión por miedo
        if psique["miedo"] > 30:
            texto = texto.replace(" ", "  ")
            texto = texto.lower()

        # Distorsión por corrupción
        if psique["corrupcion"] > 40:
            texto = texto.replace("a", "á").replace("e", "ë")

        # Distorsión por lucidez (más críptico)
        if psique["lucidez"] > 40:
            texto = "..." + texto + "..."

        return texto

class Level5:

    def jugar(self, player, engine):

        texto = """
El espacio se abre.
Pero no es una sala.
Es… algo indefinido.
No hay suelo.
No hay techo.
Solo puertas.
Decenas.
Cada una distinta.
Algunas rotas.
Otras selladas.
Algunas… respiran.
Sentís que cada una lleva a algo distinto.
Pero también sabés algo más:
No estás eligiendo libremente.
Algo en vos ya decidió.
La voz, por última vez:
"No elegís la puerta. La reconocés."

¿Qué hacés?

1. Elegir una puerta al azar
2. Intentar analizar las puertas
3. No elegir ninguna
"""

        eleccion = engine.mostrar_nivel("assets/lvl5.jpg", texto)

        # -------------------------
        # DECISIONES
        # -------------------------

        if eleccion == "1":
            player.psique["corrupcion"] += 10

            texto_resultado = """
Elegís.
Sin pensar.
La puerta cede.
Pero al cruzar…
no sentís cambio.
Porque no cruzaste.
Siempre estuviste ahí.
"""

            engine.mostrar_nivel("assets/lvl5.jpg", texto_resultado)
            return "continuar"

        elif eleccion == "2":
            player.psique["lucidez"] += 10
            player.psique["culpa"] += 5

            texto_resultado = """
Observás.
Comparás.
Intentás entender.
Pero las puertas cambian.
Se reconfiguran.
No hay lógica estable.
Entonces entendés:
No es el entorno.
Sos vos.
"""

            engine.mostrar_nivel("assets/lvl5.jpg", texto_resultado)
            return "continuar"

        elif eleccion == "3":
            player.psique["miedo"] += 15

            texto_resultado = """
No elegís.
Te quedás.
El tiempo no pasa.
O pasa demasiado.
Las puertas siguen ahí.
Esperando.
Como si supieran…
que eventualmente vas a ceder.
"""

            engine.mostrar_nivel("assets/lvl5.jpg", texto_resultado)
            return "continuar"

        return "muerte"