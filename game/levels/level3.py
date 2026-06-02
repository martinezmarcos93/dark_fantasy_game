from game.enemies import crear_sacerdote

class Level3:

    def __init__(self):
        self.nombre = "El Ritual de la Entrega"

    # ── LABERINTO ─────────────────────────────────────────────
    def fase_laberinto(self, player, engine):
        """Fase de exploración antes del combate. Callejones sin salida dan Aliento."""
        explorado = {"izquierda": False, "derecha": False}

        while True:
            opciones = []
            if not explorado["izquierda"]:
                opciones.append(("izq", "Explorar la izquierda  [oscuro, sin sonido]"))
            if not explorado["derecha"]:
                opciones.append(("der", "Explorar la derecha  [hay algo que brilla]"))
            opciones.append(("cont", "Continuar hacia el altar"))

            labels = [o[1] for o in opciones]
            ids    = [o[0] for o in opciones]

            texto = (
                "\nEl pasaje se bifurca antes de llegar al altar.\n\n"
                "El corredor de la izquierda está en silencio absoluto.\n"
                "El de la derecha tiene un brillo apenas visible.\n\n"
                f"Aliento del Umbral: {player.aliento}/10\n\n"
                "¿Qué explorás?\n"
            )

            eleccion = engine.mostrar_nivel("assets/maze.jpg", texto, opciones=True, opciones_lista=labels)

            try:
                idx = int(eleccion) - 1
                id_elegido = ids[idx]
            except (ValueError, IndexError):
                id_elegido = "cont"

            if id_elegido == "cont":
                break

            player.ganar_aliento(1)

            if id_elegido == "izq":
                explorado["izquierda"] = True
                engine.mostrar_nivel(
                    "assets/dead_end.jpg",
                    """
Un callejón estrecho termina en pared.

Encontrás marcas en la piedra.
Alguien pasó antes que vos.
Las marcas son recientes.
Las manos que las hicieron conocían este lugar.

No hay nadie ahora.

[ +1 Aliento del Umbral ]
""",
                    opciones=False
                )

            elif id_elegido == "der":
                explorado["derecha"] = True
                player.modificar_psique({"corrupcion": 5})
                engine.mostrar_nivel(
                    "assets/dead_end.jpg",
                    """
El brillo no tiene fuente visible.

Seguís el corredor hasta que termina en nada.
No hay objeto. No hay criatura.
Solo un brillo que no debería existir.

Al darte vuelta sentís que algo cambió.
No sabés qué.
Eso es parte del problema.

[ +1 Aliento del Umbral   Corrupción +5 ]
""",
                    opciones=False
                )

    def fase_combate(self, player, engine):
        enemy = crear_sacerdote()
        return engine.combate_narrativo(enemy)

    def fase_psicologica(self, player, engine):

        player.recuperar(vida=6, energia=12)

        # Cofre de Eco si combate perfecto
        engine.ofrecer_cofre_eco("assets/lvl3.jpg")

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
"""

        eleccion = engine.mostrar_nivel(
            "assets/lvl3.jpg",
            texto,
            opciones=True,
            opciones_lista=[
                "Leer el libro",
                "Ofrecer tu sangre",
                "Ignorar el altar y seguir"
            ]
        )

        if eleccion == "1":
            player.registrar_decision("Leíste el libro. Las palabras hablaban de vos.")
            player.psique["lucidez"] += 15
            player.psique["corrupcion"] += 5
            engine.mostrar_nivel(
                "assets/lvl3.jpg",
                """
Leés.
Las palabras no están escritas.
Se forman mientras las mirás.
Y hablan de vos.
De cosas que no recordabas…
pero que son ciertas.
Cada línea te revela.
Pero también te cambia.
""",
                opciones=False
            )

        elif eleccion == "2":
            player.registrar_decision("Ofreciste tu sangre al altar. Algo en vos ya había elegido.")
            player.psique["corrupcion"] += 20
            player.ganar_aliento(1)  # Elección peligrosa
            engine.mostrar_nivel(
                "assets/lvl3.jpg",
                """
Apoyás tu mano.
La piedra está tibia.
La sangre fluye.
El libro responde.
Las páginas se llenan.
Pero no con conocimiento.
Con aceptación.
Algo en vos… ya eligió.

[ +1 Aliento del Umbral ]
""",
                opciones=False
            )

        elif eleccion == "3":
            player.registrar_decision("Ignoraste el altar. La decisión pendiente te siguió.")
            player.psique["miedo"] += 10
            engine.mostrar_nivel(
                "assets/lvl3.jpg",
                """
Te alejás.
Pero el altar no desaparece.
Lo sentís.
Como una decisión no tomada.
Como algo pendiente.
Y sabés…
que lo vas a volver a ver.
""",
                opciones=False
            )

        # Llave de piedra para el Nivel 4
        player.llave_piedra = True
        engine.mostrar_nivel(
            "assets/key_stone.jpg",
            """
Al salir del altar encontrás algo grabado en el umbral.

Una llave de piedra, pequeña, casi decorativa.
Como si alguien la hubiera dejado a propósito.

O como si siempre hubiera estado esperando.

[ Llave de Piedra obtenida ]
""",
            opciones=False
        )

    def jugar(self, player, engine):
        self.fase_laberinto(player, engine)

        resultado = self.fase_combate(player, engine)
        if resultado == "muerte":
            return "muerte"

        self.fase_psicologica(player, engine)
        return "continuar"
