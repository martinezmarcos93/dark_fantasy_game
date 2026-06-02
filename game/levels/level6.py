from game.enemies import crear_hambre

class Level6:

    def __init__(self):
        self.nombre = "El Umbral Final"

    def distorsionar_texto(self, texto, player):
        psique = player.psique

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

        if psique["lucidez"] > 50:
            texto = "/// " + texto.strip() + " ///"

        return texto

    def _chequear_hambre(self, player, engine):
        """
        El Hambre — aparece si furia (Guerrero) o apuñalar (Ladrón)
        se usaron más de 4 veces en total en la run.
        Aparece sin intro al inicio del nivel.
        """
        usos_violentos = (
            player.contar_usos_accion("furia") +
            player.contar_usos_accion("apuñalar")
        )
        if usos_violentos <= 4:
            return None

        # Aparece sin pantalla de intro — directamente en el encabezado de combate
        enemy = crear_hambre()
        # Sobreescribir texto_intro para que sea mínimo
        enemy.texto_intro = (
            "\nNo hubo aviso.\n"
            "No hubo transición.\n"
            "\nEl Hambre ya estaba acá.\n"
            "\n\n[ ESPACIO para continuar ]\n"
        )

        resultado = engine.combate_narrativo(enemy)

        if resultado == "muerte":
            return "muerte"

        # Reward: +20 HP máximo permanente
        player.vida_max += 20
        player.recuperar(vida=20)
        player.registrar_decision("Venciste al Hambre. Algo en vos aprendió a contenerlo.")
        engine.mostrar_nivel(
            "assets/enemy_hambre.jpg",
            """
El Hambre retrocedió.

No porque hayas ganado.
Sino porque, por ahora,
está satisfecho.

Algo en vos absorbe lo que dejó.

[ HP máximo +20 — permanente hasta el fin del run ]
""",
            opciones=False
        )
        return None

    def jugar(self, player, engine):
        # El Hambre (consecuencia de violencia acumulada)
        resultado_hambre = self._chequear_hambre(player, engine)
        if resultado_hambre == "muerte":
            return "muerte"

        # Cofre del Umbral (si aliento >= 5 y aún disponible)
        engine.ofrecer_cofre_umbral("assets/lvl6.jpg")

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

            engine.mostrar_nivel(
                "assets/lvl6.jpg",
                self.distorsionar_texto(texto_resultado, player),
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

            engine.mostrar_nivel(
                "assets/lvl6.jpg",
                self.distorsionar_texto(texto_resultado, player),
                opciones=False
            )
            return "continuar"

        elif eleccion == "3":
            player.registrar_decision("Intentaste destruirlo. Cada golpe fue interno.")
            player.psique["violencia"] += 20
            player.psique["corrupcion"] += 15
            player.ganar_aliento(1)  # Elección peligrosa

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

[ +1 Aliento del Umbral ]
"""

            engine.mostrar_nivel(
                "assets/lvl6.jpg",
                self.distorsionar_texto(texto_resultado, player),
                opciones=False
            )
            return "continuar"

        return "muerte"
