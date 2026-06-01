class Level5:

    def __init__(self):
        self.nombre = "Las Moradas de los Muertos"

    def distorsionar_texto(self, texto, player):
        psique = player.psique

        # Miedo: minúsculas + doble espacio entre palabras (lectura fragmentada)
        if psique["miedo"] > 30:
            texto = texto.lower()
            texto = "\n".join(
                "  ".join(l.split()) if l.strip() else l
                for l in texto.split("\n")
            )

        # Corrupción: corromper vocales solo en palabras largas, una de cada tres
        # (evitar artículos/preposiciones cortas que volverían el texto ilegible)
        if psique["corrupcion"] > 40:
            _MAP = str.maketrans("aeiou", "áëïøù")
            lineas = []
            for linea in texto.split("\n"):
                palabras = linea.split(" ")
                nueva = []
                for i, p in enumerate(palabras):
                    if len(p) > 5 and i % 3 == 0:
                        p = p.translate(_MAP)
                    nueva.append(p)
                lineas.append(" ".join(nueva))
            texto = "\n".join(lineas)

        # Lucidez: marco de meta-consciencia (el personaje observa su propio estado)
        if psique["lucidez"] > 40:
            texto = "[ " + texto.strip() + " ]"

        return texto

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
"""

        # La distorsión aplica también a la pregunta: la psique ya afecta la percepción
        eleccion = engine.mostrar_nivel(
            "assets/lvl5.jpg",
            self.distorsionar_texto(texto, player),
            opciones=True,
            opciones_lista=[
                "Elegir una puerta al azar",
                "Intentar analizar las puertas",
                "No elegir ninguna"
            ]
        )

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
            engine.mostrar_nivel(
                "assets/lvl5.jpg",
                self.distorsionar_texto(texto_resultado, player),
                opciones=False
            )

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
            engine.mostrar_nivel(
                "assets/lvl5.jpg",
                self.distorsionar_texto(texto_resultado, player),
                opciones=False
            )

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
            engine.mostrar_nivel(
                "assets/lvl5.jpg",
                self.distorsionar_texto(texto_resultado, player),
                opciones=False
            )

        return "continuar"
