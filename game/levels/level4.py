from game.enemies import crear_sombra, crear_doble
from game.save_system import cargar_ng_plus, existe_ng_plus

class Level4:

    def __init__(self):
        self.nombre = "El Rey de las Sombras"

    def _chequear_doble(self, player, engine):
        """
        El Doble — solo en New Game+.
        Aparece en Level 4, antes del combate principal.
        Usa los valores de psique heredados para escalar sus stats.
        """
        if not existe_ng_plus():
            return

        psique_heredada = cargar_ng_plus()
        if not psique_heredada:
            return

        engine.mostrar_nivel(
            "assets/enemy_doble.jpg",
            f"""
{player.name}.

Algo llega desde la dirección equivocada.

No es la Sombra.

Es algo que lleva fragmentos de tu historial anterior.
Fragmentos de lo que fuiste.
Usados contra lo que sos.

El Doble.
""",
            opciones=False
        )

        enemy = crear_doble(psique_heredada)
        resultado = engine.combate_narrativo(enemy)

        if resultado == "muerte":
            return resultado

        # Recompensa: ítem del tier alto + fragmento de lore
        engine.mostrar_nivel(
            "assets/enemy_doble.jpg",
            """
El Doble se deshace.

Los fragmentos de memoria que lo componían
se dispersan en el aire.

Queda algo atrás.
Un objeto que perteneció a quien fuiste.
""",
            opciones=False
        )

        from game.player import TIER_ALTO, NOMBRES_ITEMS
        import random
        item = random.choice(TIER_ALTO)
        engine._dar_item("assets/enemy_doble.jpg", item,
                         f"El Doble dejó atrás: {NOMBRES_ITEMS.get(item, item)}\n")

        return None  # Continuar con el nivel normal

    def fase_combate(self, player, engine):
        enemy = crear_sombra()
        return engine.combate_narrativo(enemy)

    def fase_psicologica(self, player, engine):

        player.recuperar(vida=5, energia=10)

        # Cofre de Piedra si tiene llave (del Level 3)
        engine.ofrecer_cofre_piedra("assets/chest_stone.jpg")

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
            player.registrar_decision("Aceptaste todas las versiones de vos mismo. Las que dolían también.")
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
            player.registrar_decision("Rechazaste las versiones. Se volvieron más intensas.")
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
            player.registrar_decision("Atacaste a las versiones. Se multiplicaron.")
            player.psique["violencia"] += 20
            player.psique["corrupcion"] += 10
            player.ganar_aliento(1)  # Elección peligrosa
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

[ +1 Aliento del Umbral ]
""",
                opciones=False
            )

    def jugar(self, player, engine):
        # Chequear El Doble (NG+)
        resultado_doble = self._chequear_doble(player, engine)
        if resultado_doble == "muerte":
            return "muerte"

        resultado = self.fase_combate(player, engine)
        if resultado == "muerte":
            return "muerte"

        self.fase_psicologica(player, engine)
        return "continuar"
