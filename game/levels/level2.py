from game.enemies import crear_reflejo

class Level2:

    def __init__(self):
        self.nombre = "El Espejo de las Formas"

    # ── CALLEJÓN: El Viajero Perdido ─────────────────────────
    def fase_callejon(self, player, engine):
        """
        Callejón sin salida antes del combate.
        Si Aliento >= 3, encontrás al Viajero Perdido.
        """
        texto = """
Antes de llegar al espejo notan un pasadizo lateral.
Estrecho. Apenas visible.

¿Explorás?
"""
        eleccion = engine.mostrar_nivel(
            "assets/dead_end.jpg",
            texto,
            opciones=True,
            opciones_lista=["Explorar el pasadizo", "Ignorarlo y continuar"]
        )

        if eleccion != "1":
            return

        player.ganar_aliento(1)  # Explorar callejón

        if player.aliento >= 3 and player.aliado_tipo is None:
            # El Viajero Perdido
            engine.mostrar_nivel(
                "assets/npc_viajero.jpg",
                """
Al final del pasadizo hay una figura.

Ropa de viaje desgastada.
Equipo demasiado ligero para este lugar.
No habla mucho.

Solo dice:
"También estoy bajando."

Te mira. Calcula algo.
Después dice:
"Puedo acompañarte una vez. Si me convencés."

Costo: 3 Aliento del Umbral.

[ +1 Aliento del Umbral por explorar ]
""",
                opciones=False
            )

            if player.aliento >= 3:
                eleccion2 = engine.mostrar_nivel(
                    "assets/npc_viajero.jpg",
                    f"\nAliento actual: {player.aliento}/10\n\n¿Convencés al Viajero para que te acompañe?\n",
                    opciones=True,
                    opciones_lista=[
                        "Convencerlo  [−3 Aliento]",
                        "Dejarlo ir"
                    ]
                )
                if eleccion2 == "1" and player.gastar_aliento(3):
                    player.aliado_tipo    = "viajero"
                    player.viajero_activo = True
                    player.registrar_decision("Convenciste al Viajero Perdido de acompañarte.")
                    engine.mostrar_nivel(
                        "assets/npc_viajero.jpg",
                        """
Asiente.

Sin palabras.
Te sigue hacia la sala del espejo.

Aparecerá al inicio del próximo combate.
Una sola vez.
Después se irá.

[ −3 Aliento del Umbral — El Viajero te acompaña ]
""",
                        opciones=False
                    )
            else:
                engine.mostrar_nivel(
                    "assets/npc_viajero.jpg",
                    "\nNo tenés suficiente Aliento del Umbral para convencerlo.\nSe queda donde está.\n",
                    opciones=False
                )
        else:
            # Callejón sin El Viajero: solo lore
            engine.mostrar_nivel(
                "assets/dead_end.jpg",
                """
El pasadizo termina en pared.

Marcas en la piedra.
Alguien estuvo acá antes.
Las marcas dicen que siguió.

No hay nada más aquí.

[ +1 Aliento del Umbral por explorar ]
""",
                opciones=False
            )

    def fase_combate(self, player, engine):
        enemy = crear_reflejo()
        return engine.combate_narrativo(enemy)

    def fase_psicologica(self, player, engine):

        player.recuperar(vida=8, energia=15)

        # Cofre de Eco si combate perfecto
        engine.ofrecer_cofre_eco("assets/lvl2.jpg")

        # Cofre de Piedra si tiene la llave (del Level 1)
        engine.ofrecer_cofre_piedra("assets/chest_stone.jpg")

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
"""

        eleccion = engine.mostrar_nivel(
            "assets/lvl2.jpg",
            texto,
            opciones=True,
            opciones_lista=[
                "Mirar fijamente el espejo",
                "Romper el espejo",
                "Dar la espalda y seguir"
            ]
        )

        if eleccion == "1":
            player.registrar_decision("Miraste fijamente el espejo aunque el reflejo se adelantara.")
            player.psique["lucidez"] += 15
            engine.mostrar_nivel(
                "assets/lvl2.jpg",
                """
Te acercás.
Tu reflejo no te copia.
Se adelanta.
Sonríe antes que vos.
Y entonces entendés…
No estás mirando.
Estás siendo observado.
""",
                opciones=False
            )

        elif eleccion == "2":
            player.registrar_decision("Rompiste el espejo. Las versiones peores siguen ahí.")
            player.psique["violencia"] += 15
            player.ganar_aliento(1)  # Elección peligrosa
            engine.mostrar_nivel(
                "assets/lvl2.jpg",
                """
Golpeás el espejo.
Se rompe.
Pero no desaparece.
Cada fragmento sigue reflejando.
Versiones tuyas.
Peores.
Más sinceras.

La voz:
"Romper no elimina."

[ +1 Aliento del Umbral ]
""",
                opciones=False
            )

        elif eleccion == "3":
            player.registrar_decision("Le diste la espalda al espejo. El reflejo no necesitó verlo.")
            player.psique["miedo"] += 10
            engine.mostrar_nivel(
                "assets/lvl2.jpg",
                """
Das la espalda.
Pero sentís la mirada.
El reflejo no depende del espejo.
Ahora está en vos.
Y no podés dejar de sentirlo.
""",
                opciones=False
            )

    def jugar(self, player, engine):
        self.fase_callejon(player, engine)

        resultado = self.fase_combate(player, engine)
        if resultado == "muerte":
            return "muerte"

        self.fase_psicologica(player, engine)
        return "continuar"
