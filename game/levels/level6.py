class Level6:

    def __init__(self):
        self.nombre = "El Umbral Final"

    def distorsionar_texto(self, texto, player):
        psique = player.psique

        # Miedo extremo: minúsculas + fragmentar cada línea larga con pausa (…)
        if psique["miedo"] > 40:
            texto = texto.lower()
            lineas = []
            for linea in texto.split("\n"):
                palabras = linea.split()
                if len(palabras) > 3:
                    mitad = len(palabras) // 2
                    linea = " ".join(palabras[:mitad]) + "…\n" + " ".join(palabras[mitad:])
                lineas.append(linea)
            texto = "\n".join(lineas)

        # Corrupción intensa: corromper vocales en palabras largas, una de cada dos
        if psique["corrupcion"] > 50:
            _MAP = str.maketrans("aeiou", "áëïøù")
            lineas = []
            for linea in texto.split("\n"):
                palabras = linea.split(" ")
                nueva = []
                for i, p in enumerate(palabras):
                    if len(p) > 4 and i % 2 == 0:
                        p = p.translate(_MAP)
                    nueva.append(p)
                lineas.append(" ".join(nueva))
            texto = "\n".join(lineas)

        # Lucidez: doble marcador (el umbral final rompe la cuarta pared)
        if psique["lucidez"] > 50:
            texto = "/// " + texto.strip() + " ///"

        return texto

    def jugar(self, player, engine):

        texto = f"""
No hay más puertas.
No hay más caminos.
No hay cueva.
No hay voz.
Solo vos.
O lo que queda de {player.name}.

Frente a vos…
hay algo.
Tiene tu forma.
Pero no te copia.
Respira con vos.
Piensa con vos.
Sabe todo lo que hiciste.

Sabe que sos {player.name}.
Y no te juzga.
Solo espera.

¿Qué hacés?
"""

        # La distorsión aplica al texto de pregunta: el umbral final ya afecta la percepción
        eleccion = engine.mostrar_nivel(
            "assets/lvl6.jpg",
            self.distorsionar_texto(texto, player),
            opciones=True,
            opciones_lista=[
                "Aceptar lo que sos",
                "Negarlo",
                "Destruirlo"
            ]
        )

        # -------------------------
        # DECISIÓN FINAL
        # -------------------------

        if eleccion == "1":
            player.registrar_decision("Aceptaste lo que sos. Todo. Sin condiciones.")
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

            texto_resultado = self.distorsionar_texto(texto_resultado, player)

            engine.mostrar_nivel(
                "assets/lvl6.jpg",
                texto_resultado,
                opciones=False
            )
            return "continuar"

        elif eleccion == "2":
            player.registrar_decision("Negaste lo que sos. Se volvió más presente.")
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

            texto_resultado = self.distorsionar_texto(texto_resultado, player)

            engine.mostrar_nivel(
                "assets/lvl6.jpg",
                texto_resultado,
                opciones=False
            )
            return "continuar"

        elif eleccion == "3":
            player.registrar_decision("Intentaste destruirlo. Cada golpe fue interno.")
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

            texto_resultado = self.distorsionar_texto(texto_resultado, player)

            engine.mostrar_nivel(
                "assets/lvl6.jpg",
                texto_resultado,
                opciones=False
            )
            return "continuar"

        return "muerte"