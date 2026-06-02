from game.enemies import crear_grieta, crear_hambre

class Level9:

    def __init__(self):
        self.nombre = "La Biblioteca del Olvido"

    def distorsionar_texto(self, texto, player):
        psique = player.psique

        if psique["miedo"] > 25:
            texto = texto.lower()
            texto = "\n".join(
                "  ".join(l.split()) if l.strip() else l
                for l in texto.split("\n")
            )

        if psique["corrupcion"] > 35:
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

        if psique["lucidez"] > 35:
            texto = "[[ " + texto.strip() + " ]]"

        return texto

    # ── LABERINTO ─────────────────────────────────────────────
    def fase_laberinto(self, player, engine):
        """Exploración antes del combate. Uno de los callejones tiene evento de Memoria."""
        explorado = {"libros": False, "vacio": False}

        while True:
            opciones = []
            if not explorado["libros"]:
                opciones.append(("libros", "Explorar la sección de libros que se escriben solos"))
            if not explorado["vacio"]:
                opciones.append(("vacio", "Explorar el pasillo vacío al fondo"))
            opciones.append(("cont", "Continuar hacia el interior"))

            labels = [o[1] for o in opciones]
            ids    = [o[0] for o in opciones]

            texto = self.distorsionar_texto(
                "\nLa biblioteca se extiende en todas las direcciones.\n\n"
                "Hay libros que se escriben solos a la izquierda.\n"
                "Un pasillo completamente vacío al fondo.\n\n"
                f"Aliento del Umbral: {player.aliento}/10\n\n"
                "¿Qué explorás?\n",
                player
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

            if id_elegido == "libros":
                explorado["libros"] = True
                player.modificar_psique({"lucidez": 5})

                # Evento: Memoria como moneda
                if player.historial:
                    engine.mostrar_nivel(
                        "assets/dead_end.jpg",
                        self.distorsionar_texto(
                            "\nLibros que escriben solos.\n"
                            "Ninguno tiene tu nombre.\n"
                            "Todavía.\n\n"
                            "Uno de ellos se detiene.\n"
                            "Te mira.\n"
                            "Ofrece una página en blanco.\n\n"
                            "\"¿Pagás con un recuerdo?\"\n"
                            "A cambio: curación.\n",
                            player
                        ),
                        opciones=False
                    )

                    ultima = player.historial[-1]
                    preview = ultima[:60] + "…" if len(ultima) > 60 else ultima
                    elec2 = engine.mostrar_nivel(
                        "assets/dead_end.jpg",
                        self.distorsionar_texto(
                            f"\nEl libro ofrece borrar:\n\"{preview}\"\n\n"
                            f"A cambio: +20 HP\n\n"
                            f"[ Lucidez +5   +1 Aliento del Umbral ]\n",
                            player
                        ),
                        opciones=True,
                        opciones_lista=["Pagar con el recuerdo  [+20 HP]", "Rechazar"]
                    )

                    if elec2 == "1":
                        player.gastar_memoria(len(player.historial) - 1)
                        player.recuperar(vida=20)
                        msg = "\nEl recuerdo desaparece.\nEl libro lo absorbe.\nHP +20.\n"
                        if not player.historial:
                            msg += "\nNo recordás nada de lo que hiciste.\nEso también dice algo.\n"
                        engine.mostrar_nivel("assets/dead_end.jpg",
                                             self.distorsionar_texto(msg, player),
                                             opciones=False)
                    else:
                        engine.mostrar_nivel(
                            "assets/dead_end.jpg",
                            self.distorsionar_texto("\nRechazás.\nEl libro cierra solo.\n", player),
                            opciones=False
                        )
                else:
                    engine.mostrar_nivel(
                        "assets/dead_end.jpg",
                        self.distorsionar_texto(
                            "\nLibros que escriben solos.\nNinguno tiene tu nombre.\n"
                            "Todavía.\n\n[ Lucidez +5   +1 Aliento del Umbral ]\n",
                            player
                        ),
                        opciones=False
                    )

            elif id_elegido == "vacio":
                explorado["vacio"] = True
                player.modificar_psique({"corrupcion": 8})
                engine.mostrar_nivel(
                    "assets/dead_end.jpg",
                    self.distorsionar_texto(
                        "\nEl pasillo no tiene fin visible.\n\n"
                        "Caminás.\nCaminás.\nCaminás.\n\n"
                        "En algún punto te detenés.\n"
                        "No porque hayas llegado a algún lado.\n"
                        "Sino porque algo te hace detenerte.\n\n"
                        "No sabés qué.\nEso también cambia algo.\n\n"
                        "[ Corrupción +8   +1 Aliento del Umbral ]\n",
                        player
                    ),
                    opciones=False
                )

    def _chequear_hambre_aqui(self, player, engine):
        """
        El Hambre puede aparecer también en Level 9 si no apareció en Level 6
        y los usos violentos superan 6.
        """
        usos_violentos = (
            player.contar_usos_accion("furia") +
            player.contar_usos_accion("apuñalar")
        )
        # Solo aparece aquí si no apareció en Level 6 (más de 6 usos = crecimiento)
        if usos_violentos <= 6:
            return None

        enemy = crear_hambre()
        enemy.texto_intro = (
            "\nOtra vez.\n\n"
            "No aprendiste.\n"
            "O aprendiste demasiado bien.\n\n"
            "El Hambre vuelve.\n"
            "Más hambriento.\n\n"
            "\n[ ESPACIO para continuar ]\n"
        )
        enemy.dificultad = min(enemy.dificultad + 1, 12)  # Un poco más difícil

        resultado = engine.combate_narrativo(enemy)

        if resultado == "muerte":
            return "muerte"

        player.vida_max += 20
        player.recuperar(vida=20)
        engine.mostrar_nivel(
            "assets/enemy_hambre.jpg",
            "\nOtra vez lo venciste.\nAlgo en vos aprende a contenerse.\nO a alimentarse diferente.\n\n[ HP máximo +20 ]\n",
            opciones=False
        )
        return None

    def fase_combate(self, player, engine):
        enemy = crear_grieta()
        return engine.combate_narrativo(enemy)

    def fase_psicologica(self, player, engine):

        player.recuperar(vida=3, energia=6)

        # Cofre de Eco si combate perfecto
        engine.ofrecer_cofre_eco("assets/lvl9.jpg")

        texto = """
Los libros no tienen titulos.

Las paginas estan en blanco.

Pero cuando los abris,
algo se escribe.
No con tinta.
Con ausencia.

Cada libro contiene
algo que olvidaste.
O que decidiste no recordar.

Hay uno que brilla mas que los otros.

¿Que hacés?
"""

        eleccion = engine.mostrar_nivel(
            "assets/lvl9.jpg",
            self.distorsionar_texto(texto, player),
            opciones=True,
            opciones_lista=[
                "Abrir el libro que brilla.",
                "Leer un libro al azar.",
                "Cerrar los ojos y salir sin leer ninguno."
            ]
        )

        if eleccion == "1":
            player.registrar_decision("Abriste el libro que brillaba en la Biblioteca del Olvido.")
            player.psique["lucidez"] += 15
            player.psique["corrupcion"] += 8
            texto_r = """
Lo abris.

El libro contiene
lo que elegiste no saber.

No porque no pudieras saberlo.
Sino porque saber
hubiera requerido cambiar.

Ahora lo sabes.

No cambia lo que hiciste.
Pero cambia lo que sos.
"""
            engine.mostrar_nivel(
                "assets/lvl9.jpg",
                self.distorsionar_texto(texto_r, player),
                opciones=False
            )

        elif eleccion == "2":
            player.registrar_decision("Leiste un libro al azar en la Biblioteca del Olvido.")
            player.psique["culpa"] += 10
            player.psique["miedo"] += 8
            texto_r = """
Abris uno sin pensar.

El contenido no tiene sentido
en el orden en que aparece.

Pero tiene sentido
en un orden que no controlás.

No encontraste lo que buscabas.
Encontraste algo peor:
lo que no sabias que buscabas.
"""
            engine.mostrar_nivel(
                "assets/lvl9.jpg",
                self.distorsionar_texto(texto_r, player),
                opciones=False
            )

        elif eleccion == "3":
            player.registrar_decision("Saliste de la Biblioteca del Olvido sin leer nada.")
            player.psique["corrupcion"] += 15
            player.ganar_aliento(1)  # Elección peligrosa
            texto_r = """
Cerrás los ojos.

Salis.

Lo que no leiste
no desaparece.
Solo pierde nombre.

Y lo sin nombre
crece en los espacios
donde no mirás.

La biblioteca sigue ahi.
Con todos sus libros.
Con el tuyo.

[ +1 Aliento del Umbral ]
"""
            engine.mostrar_nivel(
                "assets/lvl9.jpg",
                self.distorsionar_texto(texto_r, player),
                opciones=False
            )

    def jugar(self, player, engine):
        self.fase_laberinto(player, engine)

        # El Hambre (segunda aparición si los usos superan el umbral)
        resultado_hambre = self._chequear_hambre_aqui(player, engine)
        if resultado_hambre == "muerte":
            return "muerte"

        resultado = self.fase_combate(player, engine)
        if resultado == "muerte":
            return "muerte"

        self.fase_psicologica(player, engine)
        return "continuar"
