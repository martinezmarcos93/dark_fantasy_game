from game.enemies import crear_eco

class Level7:

    def __init__(self):
        self.nombre = "La Sala del Juicio"

    # ── LABERINTO ─────────────────────────────────────────────
    def fase_laberinto(self, player, engine):
        """Fase de exploración antes del combate. El espejo roto está al fondo."""
        explorado = {"izquierda": False, "espejo_roto": False}

        while True:
            opciones = []
            if not explorado["izquierda"]:
                opciones.append(("izq", "Explorar el pasillo izquierdo  [silencio, asientos vacíos]"))
            if not explorado["espejo_roto"]:
                opciones.append(("espejo", "Explorar el callejón del fondo  [brilla algo roto]"))
            opciones.append(("cont", "Entrar a la Sala del Juicio"))

            labels = [o[1] for o in opciones]
            ids    = [o[0] for o in opciones]

            texto = (
                "\nAntes de entrar a la Sala del Juicio\nhay corredores laterales.\n\n"
                "El pasillo izquierdo está lleno de asientos de piedra vacíos.\n"
                "Al fondo se ve algo roto que capta la luz.\n\n"
                f"Aliento del Umbral: {player.aliento}/10\n\n"
                "¿Explorás?\n"
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
                player.modificar_psique({"miedo": 5})
                engine.mostrar_nivel(
                    "assets/dead_end.jpg",
                    """
Miles de asientos de piedra.

Todos vacíos.

Pero el polvo en cada uno está asentado
de formas que sugieren que alguien estuvo ahí.

No recientemente.
Pero estuvo.

El silencio aquí no es ausencia de sonido.
Es la acumulación de todos los veredictos
que nunca se pronunciaron.

[ +1 Aliento del Umbral   Miedo +5 ]
""",
                    opciones=False
                )

            elif id_elegido == "espejo":
                explorado["espejo_roto"] = True
                player.modificar_psique({"lucidez": 8, "miedo": 5})
                engine.mostrar_nivel(
                    "assets/dead_end.jpg",
                    """
Un espejo roto en el suelo.

Grande. De alguna sala que ya no existe.

Los fragmentos reflejan algo.
Pero la imagen que muestran
no es exactamente la tuya.

Es vos.
Pero desde un ángulo que no existe.
Como si el espejo te recordara
de una vez que todavía no pasó.

[ +1 Aliento del Umbral   Lucidez +8   Miedo +5 ]
""",
                    opciones=False
                )

    def fase_combate(self, player, engine):
        enemy = crear_eco()
        return engine.combate_narrativo(enemy)

    def fase_psicologica(self, player, engine):

        player.recuperar(vida=5, energia=10)

        # Cofre de Eco si combate perfecto
        engine.ofrecer_cofre_eco("assets/lvl7.jpg")

        texto = """
La Sala del Juicio está vacía.

Miles de asientos de piedra.
Ningún juez.
Solo vos en el centro.

El silencio no es ausencia de sonido.
Es la acumulación de todo lo que
dijiste y deberías haber callado.
Y de todo lo que callaste
y deberías haber dicho.

Una voz que es tu voz pero no es tu voz:
"¿Qué testimonio darías de vos mismo?"

¿Qué hacés?
"""

        eleccion = engine.mostrar_nivel(
            "assets/lvl7.jpg",
            texto,
            opciones=True,
            opciones_lista=[
                "Hablar. Decir todo.",
                "Guardar silencio.",
                "Negar que haya algo que decir."
            ]
        )

        if eleccion == "1":
            player.registrar_decision("Hablaste. Dijiste todo en la Sala del Juicio.")
            player.psique["lucidez"] += 12
            player.psique["culpa"] += 8
            engine.mostrar_nivel(
                "assets/lvl7.jpg",
                """
Hablás.

Todo.
Sin orden.
Sin filtro.

Las palabras llenan la sala
y rebotan en el vacío.

No hay nadie para escucharte.
Pero el acto de decirlo
cambia algo.

No te absuelve.
Solo te hace más real.
""",
                opciones=False
            )

        elif eleccion == "2":
            player.registrar_decision("Guardaste silencio ante el juicio.")
            player.psique["miedo"] += 10
            player.psique["lucidez"] += 5
            engine.mostrar_nivel(
                "assets/lvl7.jpg",
                """
No decís nada.

El silencio se asienta.

La sala no te juzga por callarte.
No tiene capacidad de juzgar nada.

Pero vos te juzgás a vos mismo.
Y eso ocupa más espacio
que cualquier veredicto externo.
""",
                opciones=False
            )

        elif eleccion == "3":
            player.registrar_decision("Negaste tener algo que decir en el juicio.")
            player.psique["corrupcion"] += 12
            player.psique["violencia"] += 5
            player.ganar_aliento(1)  # Elección peligrosa
            engine.mostrar_nivel(
                "assets/lvl7.jpg",
                """
Decís que no hay nada.

La sala no responde.

Pero algo en el aire
cambia de temperatura.

Lo que negas
no desaparece.
Solo deja de tener nombre.
Y lo sin nombre
es más peligroso.

[ +1 Aliento del Umbral ]
""",
                opciones=False
            )

        # Llave de piedra para el Nivel 8
        player.llave_piedra = True
        engine.mostrar_nivel(
            "assets/key_stone.jpg",
            """
Al salir de la Sala encontrás algo en la silla central.

Una llave de piedra.
Pequeña.
Como si el juicio hubiera dejado algo para vos.

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
