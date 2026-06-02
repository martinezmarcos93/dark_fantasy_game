from game.enemies import crear_otro

class Level5:

    def __init__(self):
        self.nombre = "Las Moradas de los Muertos"

    def distorsionar_texto(self, texto, player):
        psique = player.psique

        if psique["miedo"] > 30:
            texto = texto.lower()
            texto = "\n".join(
                "  ".join(l.split()) if l.strip() else l
                for l in texto.split("\n")
            )

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

        if psique["lucidez"] > 40:
            texto = "[ " + texto.strip() + " ]"

        return texto

    def _chequear_otro(self, player, engine):
        """
        El Otro — aparece si todos los valores de psique están
        dentro de un rango de 10 puntos entre sí.
        Reemplaza la transición entre Level 4 y Level 5.
        """
        if not player.psique_equilibrada():
            return None

        engine.mostrar_nivel(
            "assets/enemy_otro.jpg",
            """
Antes de que te adentres en las moradas…

algo te espera en el umbral.

No es una criatura.
No es un guardián.

Es lo que ocurre cuando
todas las partes de vos
están, por primera vez,
en equilibrio.

El Otro.

No podés ignorarlo.
Viene de adentro.
""",
            opciones=False
        )

        enemy = crear_otro()
        resultado = engine.combate_narrativo(enemy)

        if resultado == "muerte":
            return "muerte"

        # Ofrecer fusión (ending secreto)
        engine.ofrecer_fusion_con_otro("assets/enemy_otro.jpg")

        return None  # Continuar con el nivel

    def _chequear_voz_umbral(self, player, engine):
        """La Voz del Umbral — aliado de información. Requiere lucidez >= 30."""
        engine.encuentro_voz_umbral("assets/npc_voz.jpg")

    def jugar(self, player, engine):

        # Chequear El Otro (psique equilibrada)
        resultado_otro = self._chequear_otro(player, engine)
        if resultado_otro == "muerte":
            return "muerte"

        # La Voz del Umbral (si lucidez >= 30 y sin aliado)
        self._chequear_voz_umbral(player, engine)

        # Cofre de Eco: basado en si el último combate (Level 4) fue perfecto
        engine.ofrecer_cofre_eco("assets/lvl5.jpg")

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
            player.registrar_decision("Elegiste una puerta al azar. Siempre estuviste ahí.")
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
            player.registrar_decision("Intentaste analizar las puertas. La lógica no aplicaba.")
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
            player.registrar_decision("No elegiste ninguna puerta. Las puertas esperaron.")
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
