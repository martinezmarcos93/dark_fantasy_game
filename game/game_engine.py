import random
from game.ui import UI, EscapeAlMenu
from game.player import Player, NOMBRES_ITEMS, ITEMS_ENTRE_COMBATES, ITEMS_CONSUMIBLES, TIER_BASICO, TIER_MEDIO, TIER_ALTO
from game.menu import Menu
from game.intro import Intro
from game.save_system import (guardar_partida, cargar_partida, borrar_partida,
                               listar_slots, guardar_ng_plus, cargar_ng_plus, existe_ng_plus)

_LEVEL_IMGS = [
    "assets/lvl1.jpg", "assets/lvl2.jpg", "assets/lvl3.jpg",
    "assets/lvl4.jpg", "assets/lvl5.jpg", "assets/lvl6.jpg",
    "assets/lvl7.jpg", "assets/lvl8.jpg", "assets/lvl9.jpg",
    "assets/lvl10.jpg",
]


class GameEngine:
    def __init__(self):
        self.player = None
        self.current_level_index = 0
        self.levels = []
        self.save_slot = 0
        self.modo_lectura = False
        self.dificultad_global = 1.0
        self.ui = UI()
        self.menu = Menu(self.ui)
        self.intro = Intro(self.ui)
        # Rastrear si el jugador huyó en el nivel actual
        self.huyo_este_nivel = False

    # ─────────────────────────────────────────
    # INICIO
    # ─────────────────────────────────────────
    def iniciar(self):
        while True:
            accion = self.menu.mostrar()

            if accion == "nueva":
                slot = self._elegir_slot(modo="nueva")
                if slot is None:
                    continue
                self.save_slot = slot
                borrar_partida(slot)
                self.current_level_index = 0
                try:
                    self.intro.mostrar()
                    self.crear_personaje()
                except EscapeAlMenu:
                    continue
                self.cargar_niveles()
                self.jugar()

            elif accion == "cargar":
                slot = self._elegir_slot(modo="cargar")
                if slot is None:
                    continue
                self.save_slot = slot
                exito = self.cargar_juego(slot)
                if exito:
                    self.cargar_niveles()
                    self.jugar()

            elif accion == "lectura":
                slot = self._elegir_slot(modo="nueva")
                if slot is None:
                    continue
                self.save_slot = slot
                self.modo_lectura = True
                borrar_partida(slot)
                self.current_level_index = 0
                try:
                    self.intro.mostrar()
                    self.crear_personaje()
                except EscapeAlMenu:
                    self.modo_lectura = False
                    continue
                self.cargar_niveles()
                self.jugar()
                self.modo_lectura = False

            elif accion == "creditos":
                self.menu.mostrar_creditos()

            elif accion == "salir":
                import pygame, sys
                pygame.quit()
                sys.exit()

    # ─────────────────────────────────────────
    # CREAR JUGADOR
    # ─────────────────────────────────────────
    def crear_personaje(self):
        texto_clase = """
=== CREACIÓN DE PERSONAJE ===


Elegí tu senda:
"""
        opciones = ["Guerrero", "Hechicero", "Ladrón"]
        eleccion = self.mostrar_nivel("assets/lvl1.jpg", texto_clase, opciones=True, opciones_lista=opciones)

        clases = {"1": "Guerrero", "2": "Hechicero", "3": "Ladrón"}
        clase = clases.get(eleccion, "Errante")

        self._mostrar_retrato_clase(clase)

        imagen = self.ui.cargar_imagen(self._retrato_path(clase))
        nombre = self.ui.pedir_nombre(imagen, clase)
        self.player = Player(nombre, clase)

        psique_previa = cargar_ng_plus()
        if psique_previa:
            self._aplicar_herencia_ng_plus(psique_previa)

        self._elegir_dificultad()

    def _retrato_path(self, clase):
        retratos = {
            "Guerrero":  "assets/portrait_warrior.jpg",
            "Hechicero": "assets/portrait_mage.jpg",
            "Ladrón":    "assets/portrait_rogue.jpg",
        }
        return retratos.get(clase, "assets/lvl1.jpg")

    def _mostrar_retrato_clase(self, clase):
        descripciones = {
            "Guerrero": """
La senda del Guerrero.

Fuerza como primera respuesta.
Resistencia como segunda.

Stamina: 40
Recurso más bajo — cada acción especial cuesta.
Golpe Cargado y Furia Ciega son devastadores,
pero no infinitos.

Dos Defenders seguidos desbloquean
el Contraataque Total.

La fuerza no es solo del cuerpo.
""",
            "Hechicero": """
La senda del Hechicero.

Conocimiento como arma.
La mente como campo de batalla.

Magia: 100
El recurso más alto — pero cada hechizo se usa
una sola vez por combate.

Los hechizos más poderosos se desbloquean
a medida que descends.
Nombre Verdadero en nivel 3.
Fragmento del Abismo en nivel 4.

Saber tiene un precio.
""",
            "Ladrón": """
La senda del Ladrón.

Posición como ventaja.
La paciencia como táctica.

Ingenio: 70
Observar primero habilita ataques devastadores.
Sin setup, solo opciones básicas.

Sin Ingenio: Improvisar como última salida.
El resultado es incierto.

No todo se puede planear.
""",
        }
        texto = descripciones.get(clase, "Clase desconocida.")
        self.ui.esperar_input(
            self.ui.cargar_imagen(self._retrato_path(clase)),
            texto,
            opciones=False,
            player=None
        )

    def _aplicar_herencia_ng_plus(self, psique_previa):
        herencia = {k: int(v * 0.20) for k, v in psique_previa.items() if v > 0}
        if not herencia:
            return

        self.player.modificar_psique(herencia)

        lineas = "\n".join(
            f"  {k:<12} +{v}"
            for k, v in herencia.items() if v > 0
        )
        texto = f"""
Algo persistió.

No es un recuerdo exacto.
Es una marca.
Lo que el Umbral te dejó
antes de que empezara este descenso.

{lineas}

Empezás con eso.
Ya era tuyo de antes.
"""
        self.ui.esperar_input(
            self.ui.cargar_imagen("assets/lvl1.jpg"),
            texto,
            opciones=False,
            player=self.player
        )

    def _elegir_dificultad(self):
        texto = """
¿Qué tan profundo querés descender?

La dificultad afecta el daño enemigo y las tiradas de combate.
La narrativa y los finales son siempre los mismos.
"""
        opciones = [
            "Umbral Suave  [enemigos más fáciles]",
            "Umbral Normal  [experiencia diseñada]",
            "Umbral Profundo  [enemigos más duros]",
        ]
        eleccion = self.mostrar_nivel("assets/lvl1.jpg", texto, opciones=True, opciones_lista=opciones)
        mapa = {"1": 0.7, "2": 1.0, "3": 1.4}
        self.dificultad_global = mapa.get(eleccion, 1.0)

    # ─────────────────────────────────────────
    # CARGAR NIVELES
    # ─────────────────────────────────────────
    def cargar_niveles(self):
        from game.levels.level1  import Level1
        from game.levels.level2  import Level2
        from game.levels.level3  import Level3
        from game.levels.level4  import Level4
        from game.levels.level5  import Level5
        from game.levels.level6  import Level6
        from game.levels.level7  import Level7
        from game.levels.level8  import Level8
        from game.levels.level9  import Level9
        from game.levels.level10 import Level10

        self.levels = [
            Level1(),
            Level2(),
            Level3(),
            Level4(),
            Level5(),
            Level6(),
            Level7(),
            Level8(),
            Level9(),
            Level10(),
        ]

    # ─────────────────────────────────────────
    # MOSTRAR NIVEL — wrapper central
    # ─────────────────────────────────────────
    def mostrar_nivel(self, imagen_path, texto, opciones=True, opciones_lista=None):
        imagen = self.ui.cargar_imagen(imagen_path)
        return self.ui.esperar_input(imagen, texto, opciones, opciones_lista, self.player,
                                     nivel=self.current_level_index)

    # ─────────────────────────────────────────
    # COMBATE NARRATIVO
    # ─────────────────────────────────────────
    def combate_narrativo(self, enemy):
        if self.modo_lectura:
            self.mostrar_nivel(enemy.imagen, enemy.texto_intro, opciones=False)
            self.player.modificar_psique(enemy.psique_victoria_jugador)
            return "vivo"
        import math
        enemy.dificultad = max(1, round(enemy.dificultad * self.dificultad_global))
        from game.combat_system import combate_completo
        return combate_completo(enemy, self.player, self)

    # ─────────────────────────────────────────
    # LOOP PRINCIPAL
    # ─────────────────────────────────────────
    def jugar(self):
        try:
            while self.player.alive and self.current_level_index < len(self.levels):
                self.huyo_este_nivel = False  # Reset por nivel

                nivel = self.levels[self.current_level_index]
                resultado = nivel.jugar(self.player, self)

                if resultado == "muerte":
                    self.player.morir("Fallaste en la prueba.")
                    break

                elif resultado == "continuar":
                    # Bonus por no haber huido
                    if not self.huyo_este_nivel:
                        self.player.ganar_aliento(1)

                    self._mostrar_resumen_psique()
                    self._entre_niveles()  # Gestión de inventario y descanso

                    self.current_level_index += 1
                    self.player.level = self.current_level_index + 1
                    guardar_partida(self.player, self.current_level_index, self.save_slot)

                else:
                    break

            self.final_juego()

        except EscapeAlMenu:
            if self.player and self.player.alive:
                guardar_partida(self.player, self.current_level_index, self.save_slot)
            return

    # ─────────────────────────────────────────
    # GESTIÓN ENTRE NIVELES
    # ─────────────────────────────────────────
    def _entre_niveles(self):
        """Pantalla de inventario y descanso entre niveles."""
        img_path = _LEVEL_IMGS[min(self.current_level_index, len(_LEVEL_IMGS) - 1)]

        while True:
            acciones = []  # lista de (id, label)

            if self.player.aliento >= 2:
                acciones.append(("descanso", f"Descanso  [−2 Aliento → +10 HP]  (HP: {self.player.vida}/{self.player.vida_max})"))

            for item in self.player.inventario:
                if item in ITEMS_ENTRE_COMBATES:
                    label = NOMBRES_ITEMS.get(item, item)
                    acciones.append((f"usar_{item}", f"Usar: {label}"))

            acciones.append(("continuar", "Continuar al siguiente nivel"))

            inv_txt = ", ".join(NOMBRES_ITEMS.get(i, i) for i in self.player.inventario) or "—"
            texto = (
                f"\n— Entre niveles —\n\n"
                f"Aliento del Umbral: {self.player.aliento}/10\n"
                f"Inventario: {inv_txt}\n"
                f"HP: {self.player.vida}/{self.player.vida_max}   "
                f"{self.player.energia_nombre}: {self.player.energia}/{self.player.energia_max}\n\n"
                f"¿Hacés algo antes de continuar?\n"
            )

            labels = [a[1] for a in acciones]
            ids    = [a[0] for a in acciones]

            eleccion = self.mostrar_nivel(img_path, texto, opciones=True, opciones_lista=labels)

            try:
                idx = int(eleccion) - 1
                id_elegido = ids[idx]
            except (ValueError, IndexError):
                id_elegido = "continuar"

            if id_elegido == "continuar":
                break
            elif id_elegido == "descanso":
                self.player.gastar_aliento(2)
                self.player.recuperar(vida=10)
                self.mostrar_nivel(
                    img_path,
                    "\nDescansás un momento. El peso se alivia apenas.\n[ −2 Aliento   +10 HP ]\n",
                    opciones=False
                )
            elif id_elegido.startswith("usar_"):
                item_id = id_elegido[5:]  # remove "usar_" prefix
                self._aplicar_item(item_id, img_path)

    def _aplicar_item(self, item_id, img_path):
        """Aplica el efecto de un ítem entre combates."""
        nombre = NOMBRES_ITEMS.get(item_id, item_id)
        consumible = item_id in ITEMS_CONSUMIBLES

        if item_id == "antorcha":
            self.player.modificar_psique({"miedo": -10, "lucidez": 5})
            texto = f"La Antorcha arde. La luz revela demasiado.\n[ Miedo −10   Lucidez +5 ]"

        elif item_id == "sal":
            self.player.modificar_psique({"corrupcion": -15, "culpa": 8})
            texto = f"La Sal Consagrada purifica. El precio es moral.\n[ Corrupción −15   Culpa +8 ]\n(consumida)"

        elif item_id == "vendas":
            self.player.recuperar(vida=25)
            texto = f"Las Vendas Viejas. Algo tan simple como sobrevivir.\n[ HP +25 ]\n(consumidas)"

        elif item_id == "espejo":
            psique = self.player.psique
            dominante = max(psique, key=psique.get)
            val = psique[dominante]
            nombres_p = {
                "violencia": "Violencia", "miedo": "Miedo", "culpa": "Culpa",
                "lucidez": "Lucidez", "corrupcion": "Corrupción"
            }
            self.player.modificar_psique({"miedo": 5})
            texto = (
                f"El Fragmento de Espejo muestra lo que sos.\n\n"
                f"Psique dominante: {nombres_p.get(dominante, dominante)} ({val}/100)\n\n"
                f"Saber tiene un precio.\n[ Miedo +5 ]\n(consumido)"
            )

        elif item_id == "sangre":
            self.player.modificar_psique({"culpa": 5})
            self.player.recuperar(vida=15)
            texto = f"Sangre Seca. Funciona. El cuerpo no pregunta de dónde viene.\n[ HP +15   Culpa +5 ]"
            consumible = False  # Reutilizable — no se quita del inventario

        elif item_id == "mapa":
            # Revelar si el próximo nivel tiene potencial enemigo secreto
            # Índices 0-based: L4=3 (Doble), L5=4 (Otro), L6=5 (Hambre), L9=8 (Hambre)
            prox = self.current_level_index + 1
            usos_violentos = (self.player.contar_usos_accion("furia") +
                              self.player.contar_usos_accion("apuñalar"))
            tiene_secreto = (
                prox in {3, 4} or
                (prox in {5, 8} and usos_violentos > 4)
            )
            if tiene_secreto:
                texto_mapa = "El mapa susurra: hay algo que no debería estar en el siguiente nivel."
            else:
                texto_mapa = "El mapa dice: el camino parece despejado."
            texto = f"Mapa Roto — {texto_mapa}\n(consumido)"

        elif item_id == "elixir":
            if not self.player.historial:
                self.mostrar_nivel(img_path, "El Elixir del Olvido no tiene nada que borrar.\nTu historial está vacío.", opciones=False)
                return
            # Mostrar historial y pedir qué borrar
            entries = self.player.historial
            labels_mem = [f"Olvidar: {e[:50]}…" if len(e) > 50 else f"Olvidar: {e}" for e in entries]
            labels_mem.append("Cancelar")
            elec = self.mostrar_nivel(
                img_path,
                "El Elixir del Olvido. Elegí qué borrar:\n[ Lucidez −10 ]\n",
                opciones=True,
                opciones_lista=labels_mem
            )
            try:
                idx = int(elec) - 1
                if idx < len(entries):
                    self.player.gastar_memoria(idx)
                    self.player.modificar_psique({"lucidez": -10})
                    texto = "Un recuerdo se disuelve. El Elixir se consume.\n[ Lucidez −10 ]\n(consumido)"
                    if not self.player.historial:
                        texto += "\n\nNo recordás nada de lo que hiciste.\nEso también dice algo."
                    self.mostrar_nivel(img_path, texto, opciones=False)
                return
            except (ValueError, IndexError):
                return
        else:
            return

        self.mostrar_nivel(img_path, texto, opciones=False)
        if consumible:
            self.player.quitar_item(item_id)

    # ─────────────────────────────────────────
    # COFRES
    # ─────────────────────────────────────────
    def ofrecer_cofre_eco(self, imagen_path=None):
        """Cofre de Eco: solo si el último combate fue perfecto (3/3 rondas)."""
        if not self.player.ultimo_combate_perfecto:
            return
        img = imagen_path or _LEVEL_IMGS[min(self.current_level_index, 9)]
        item = random.choice(TIER_MEDIO)
        texto_cofre = (
            f"Cofre de Eco.\n\n"
            f"Ganaste cada ronda.\nEl cofre lo sabe.\n\n"
            f"Contenido: {NOMBRES_ITEMS.get(item, item)}\n"
        )
        self._dar_item(img, item, texto_cofre)

    def ofrecer_cofre_piedra(self, imagen_path=None):
        """Cofre de Piedra: requiere llave de piedra."""
        if not self.player.llave_piedra:
            return
        self.player.llave_piedra = False
        img = "assets/chest_stone.jpg"
        item = random.choice(TIER_BASICO)
        texto_cofre = (
            f"Cofre de Piedra.\n\n"
            f"La llave encaja en silencio.\nAlgo guardado durante mucho tiempo.\n\n"
            f"Contenido: {NOMBRES_ITEMS.get(item, item)}\n"
        )
        self._dar_item(img, item, texto_cofre)

    def ofrecer_cofre_umbral(self, imagen_path=None):
        """Cofre del Umbral: requiere ≥5 aliento y cofre disponible."""
        if not self.player.cofre_umbral_disponible:
            return
        if self.player.aliento < 5:
            return
        self.player.cofre_umbral_disponible = False
        self.player.gastar_aliento(5)
        img = "assets/chest_umbral.jpg"
        item = random.choice(TIER_ALTO)
        texto_cofre = (
            f"Cofre del Umbral.\n\n"
            f"El Aliento que acumulaste abre esto.\n"
            f"No cualquiera llega con tanto peso.\n\n"
            f"Contenido: {NOMBRES_ITEMS.get(item, item)}\n"
            f"[ −5 Aliento del Umbral ]\n"
        )
        # Fragmento del ending actual como bonus narrativo
        ending_preview = self.determinar_final()
        texto_cofre += f"\n— El cofre también muestra un fragmento de tu destino —\n{ending_preview[:300]}…\n"
        self._dar_item(img, item, texto_cofre)

    def _dar_item(self, img_path, item_id, texto_cofre):
        """Muestra el cofre y entrega el ítem. Si el inventario está lleno, pide qué soltar."""
        if len(self.player.inventario) < 3:
            self.player.agregar_item(item_id)
            self.mostrar_nivel(img_path, texto_cofre + "\n[ Ítem añadido al inventario ]", opciones=False)
        else:
            self.mostrar_nivel(img_path, texto_cofre + "\n— Inventario lleno. Elegí qué soltar —", opciones=False)
            labels = [f"Soltar: {NOMBRES_ITEMS.get(i, i)}" for i in self.player.inventario]
            labels.append("Dejar el cofre cerrado")
            elec = self.mostrar_nivel(img_path, "", opciones=True, opciones_lista=labels)
            try:
                idx = int(elec) - 1
                if idx < len(self.player.inventario):
                    self.player.inventario[idx] = item_id
                    self.mostrar_nivel(
                        img_path,
                        f"Intercambiaste. Ahora llevás: {NOMBRES_ITEMS.get(item_id, item_id)}.",
                        opciones=False
                    )
            except (ValueError, IndexError):
                pass

    # ─────────────────────────────────────────
    # ENCUENTRO: LA VOZ DEL UMBRAL
    # ─────────────────────────────────────────
    def encuentro_voz_umbral(self, imagen_path):
        """La Voz del Umbral — aliado de información. Level 5, lucidez ≥ 30."""
        if self.player.psique["lucidez"] < 30:
            return
        if self.player.aliado_tipo is not None:
            return

        self.player.aliado_tipo = "voz"
        self.player.modificar_psique({"culpa": 10})

        ending_texto = self.determinar_final()

        psique = self.player.psique
        dominante = max(psique, key=psique.get)
        nombres_psique = {
            "violencia": "Violencia", "miedo": "Miedo", "culpa": "Culpa",
            "lucidez": "Lucidez", "corrupcion": "Corrupción"
        }

        texto = (
            f"La voz que siempre estuvo ahí.\n"
            f"Ahora elige responder.\n\n"
            f"— Tu destino proyectado —\n\n"
            f"{ending_texto}\n\n"
            f"El factor dominante: {nombres_psique.get(dominante, dominante)} ({psique[dominante]}/100).\n\n"
            f"Eso dice hacia dónde vas.\n"
            f"Si querés otro destino, ya sabés qué cambiar.\n\n"
            f"[ Culpa +10 por saber tu destino ]\n"
        )
        self.mostrar_nivel(imagen_path, texto, opciones=False)

    # ─────────────────────────────────────────
    # ENCUENTRO POSTERIOR AL OTRO: FUSIÓN
    # ─────────────────────────────────────────
    def ofrecer_fusion_con_otro(self, imagen_path):
        """Tras derrotar a El Otro, ofrecer fusionarse (ending secreto)."""
        self.player.ganar_aliento(2)

        texto = (
            f"El Otro está derrotado.\n\n"
            f"Pero no del todo.\n\n"
            f"Todavía está ahí. En el límite.\n"
            f"Y ofrece algo que ningún enemigo ofreció:\n\n"
            f"Fusionarte con él.\n\n"
            f"No desaparecerías.\n"
            f"Serías más completo.\n"
            f"Y también menos singular.\n\n"
            f"[ +2 Aliento del Umbral ]\n"
        )
        eleccion = self.mostrar_nivel(
            imagen_path, texto, opciones=True,
            opciones_lista=["Fusionarte con El Otro", "Alejarte"]
        )

        if eleccion == "1":
            self.player.fusionado_con_otro = True
            self.player.registrar_decision("Te fusionaste con El Otro. La dualidad terminó.")
            self.mostrar_nivel(
                imagen_path,
                "\nNo hay dos voces ahora.\nSolo una.\nMás silenciosa.\nMás completa.\n",
                opciones=False
            )
        else:
            self.mostrar_nivel(
                imagen_path,
                "\nTe alejás.\nEl Otro se queda donde estaba.\nSiempre estuvo ahí.\n",
                opciones=False
            )

    # ─────────────────────────────────────────
    # CARGAR JUEGO DESDE JSON
    # ─────────────────────────────────────────
    def _elegir_slot(self, modo="cargar"):
        slots = listar_slots()
        imagen = self.ui.cargar_imagen("assets/lvl1.jpg")

        if modo == "cargar":
            opciones_validas = [s for s in slots if not s["vacio"]]
            if not opciones_validas:
                return None
            labels_cargables = [
                f"Slot {s['slot']+1}  — {s['nombre']} ({s['clase']})  Nivel {s['nivel']}"
                for s in slots if not s["vacio"]
            ]
            ids_cargables = [s["slot"] for s in slots if not s["vacio"]]
            if not ids_cargables:
                return None
            eleccion = self.ui.esperar_input(
                imagen,
                "\n¿Qué partida querés cargar?\n",
                opciones=True,
                opciones_lista=labels_cargables
            )
            try:
                return ids_cargables[int(eleccion) - 1]
            except (ValueError, IndexError):
                return ids_cargables[0]

        else:
            labels = []
            for s in slots:
                if s["vacio"]:
                    labels.append(f"Slot {s['slot']+1}  [libre]")
                else:
                    labels.append(
                        f"Slot {s['slot']+1}  — {s['nombre']} ({s['clase']})  [sobreescribir]"
                    )
            eleccion = self.ui.esperar_input(
                imagen,
                "\n¿En qué slot guardás la nueva partida?\n",
                opciones=True,
                opciones_lista=labels
            )
            try:
                return int(eleccion) - 1
            except (ValueError, IndexError):
                return 0

    def cargar_juego(self, slot=0):
        data = cargar_partida(slot)
        if not data:
            return False

        REQUIRED = {"nombre", "clase", "stats", "psique", "alive", "nivel_actual"}
        if not REQUIRED.issubset(data.keys()):
            return False

        self.player = Player(data["nombre"], data["clase"])
        self.player.stats  = data["stats"]
        self.player.psique = data["psique"]
        self.player.alive  = data["alive"]
        self.player.vida    = data.get("vida", self.player.vida_max)
        self.player.energia = data.get("energia", self.player.energia_max)
        self.player.historial      = data.get("historial", [])
        self.player.stats_combate  = data.get("stats_combate", self.player.stats_combate)
        self.current_level_index   = data["nivel_actual"]
        # Nuevos campos (con defaults para partidas antiguas)
        self.player.aliento                 = data.get("aliento", 0)
        self.player.inventario              = data.get("inventario", [])
        self.player.llave_piedra            = data.get("llave_piedra", False)
        self.player.aliado_tipo             = data.get("aliado_tipo", None)
        self.player.viajero_activo          = data.get("viajero_activo", False)
        self.player.viajero_usado           = data.get("viajero_usado", False)
        self.player.fusionado_con_otro      = data.get("fusionado_con_otro", False)
        self.player.memorias_gastadas       = data.get("memorias_gastadas", 0)
        self.player.ultimo_combate_perfecto = data.get("ultimo_combate_perfecto", False)
        self.player.cofre_umbral_disponible = data.get("cofre_umbral_disponible", True)
        return True

    # ─────────────────────────────────────────
    # PANTALLA DE MUERTE
    # ─────────────────────────────────────────
    def pantalla_muerte(self):
        clase = self.player.clase
        nivel = self.current_level_index

        imagenes = {
            "Guerrero":  "assets/death_warrior.jpg",
            "Hechicero": "assets/death_mage.jpg",
            "Ladrón":    "assets/death_rogue.jpg",
        }
        imagen_path = imagenes.get(clase, "assets/game_over.jpg")
        self.ui.reproducir_musica(nombre="ambiente")

        textos_guerrero = [
            f"{self.player.name}.\n\nLa piedra no distingue entre los valientes y los demás.\nSolo entre lo que resiste... y lo que cede.\n\nCediste.\n\nEl Umbral absorbió tu fuerza.\nAhora es suya.\n",
            f"{self.player.name}.\n\nPeleaste contra vos mismo.\nY perdiste.\n\nNo hay vergüenza en eso.\nSolo hay silencio.\n\nEl reflejo sigue ahí.\nCon tu cara.\nCon tu fuerza.\nSin vos.\n",
            f"{self.player.name}.\n\nEl Sacerdote no te mató.\nTomó algo.\n\nY sin eso...\nel cuerpo siguió un rato más.\nPero vos ya no estabas adentro.\n",
            f"{self.player.name}.\n\nLa Sombra Soberana te conocía\nmejor de lo que te conocías vos.\n\nCada derrota que alguna vez tuviste\nya estaba en ella.\n\nAhora también estás vos.\n",
        ]

        textos_hechicero = [
            f"{self.player.name}.\n\nLa piedra no tiene memoria.\nTenías razón.\n\nPero tampoco tiene piedad.\n\nTu hechizo volvió.\nY fue más honesto que vos.\n",
            f"{self.player.name}.\n\nEl conocimiento que usaste contra el Reflejo\nera tuyo.\n\nY él te lo devolvió\nmultiplicado por todo lo que sabías.\n\nMoriste de tu propia comprensión.\n",
            f"{self.player.name}.\n\nIntentaste nombrarlo.\nFallaste.\n\nLo que no puede ser nombrado\ntampoco puede ser detenido.\n\nSe llevó algo tuyo.\nEl nombre que más importaba.\nEl tuyo.\n",
            f"{self.player.name}.\n\nHabía demasiadas historias en la Sombra.\nNo podías contenerlas todas.\n\nUna mente que lo intenta igual\nse rompe igual.\n\nLa tuya resistió hasta el final.\nEso es suficiente.\nO debería serlo.\n",
        ]

        textos_ladron = [
            f"{self.player.name}.\n\nSiempre hay alguien que te ve\naunque no quieras ser visto.\n\nEl Guardián no tenía ojos.\nPero te encontró igual.\n\nAlgunas cosas no se pueden esquivar.\nSolo se pueden recibir.\n",
            f"{self.player.name}.\n\nIntentaste desaparecer.\nEl Reflejo sabía adónde ibas\nantes de que lo supieras vos.\n\nPorque eras predecible.\nNo por tus movimientos.\nPor tus miedos.\n",
            f"{self.player.name}.\n\nTe vaciaste de intención.\nCasi lo lograste.\n\nPero quedó un rastro.\nPequeño.\nSuficiente.\n\nEl Sacerdote marcó ese rastro.\nY lo que está marcado\nno puede ocultarse más.\n",
            f"{self.player.name}.\n\nLe diste algo tuyo como señuelo.\nLa Sombra no lo aceptó.\n\nFue por vos directamente.\n\nPorque ya te tenía adentro\ndesde antes de que empezara la pelea.\n",
        ]

        textos = {
            "Guerrero":  textos_guerrero,
            "Hechicero": textos_hechicero,
            "Ladrón":    textos_ladron,
        }

        lista = textos.get(clase, textos_guerrero)
        idx = min(nivel, len(lista) - 1)
        texto_muerte = lista[idx]

        self.ui.esperar_input(
            self.ui.cargar_imagen(imagen_path),
            texto_muerte,
            opciones=False
        )

    # ─────────────────────────────────────────
    # FINAL DEL JUEGO
    # ─────────────────────────────────────────
    def final_juego(self):
        if not self.player.alive:
            self.pantalla_muerte()
            borrar_partida(self.save_slot)
            return

        self._mostrar_estadisticas()
        self._mostrar_historial()

        ending = self.determinar_final()
        texto = f"\n{self.player.name}.\n\nTu destino:\n\n{ending}\n"
        self.ui.esperar_input(
            self.ui.cargar_imagen("assets/lvl6.jpg"),
            texto,
            opciones=False
        )
        guardar_ng_plus(self.player.psique)
        borrar_partida(self.save_slot)

    def _mostrar_estadisticas(self):
        sc = self.player.stats_combate
        total_rondas = sc["rondas_ganadas"] + sc["rondas_perdidas"]
        winrate = int(sc["rondas_ganadas"] / total_rondas * 100) if total_rondas > 0 else 0

        if sc["acciones"]:
            accion_top = max(sc["acciones"], key=sc["acciones"].get)
            veces_top  = sc["acciones"][accion_top]
            linea_accion = f"Acción más usada:   {accion_top}  ({veces_top} veces)"
        else:
            linea_accion = "Acción más usada:   —"

        mem_txt = ""
        if self.player.memorias_gastadas > 0:
            mem_txt = f"Memorias borradas:  {self.player.memorias_gastadas}\n"

        texto = (
            f"\n— Lo que dejaste en el camino —\n\n\n"
            f"Daño infligido:     {sc['daño_infligido']}\n"
            f"Daño recibido:      {sc['daño_recibido']}\n"
            f"Rondas ganadas:     {sc['rondas_ganadas']} / {total_rondas}  ({winrate}%)\n"
            f"Golpes críticos:    {sc['criticos']}\n"
            f"{linea_accion}\n"
            f"Aliento acumulado:  {self.player.aliento}/10\n"
            f"{mem_txt}\n"
            f"Estos números no mienten.\n"
            f"Aunque vos sí lo hayas hecho.\n\n"
        )
        self.ui.esperar_input(
            self.ui.cargar_imagen("assets/lvl6.jpg"),
            texto,
            opciones=False,
            player=self.player
        )

    def _mostrar_resumen_psique(self):
        p = self.player.psique
        nombres = {
            "violencia":  "Violencia",
            "miedo":      "Miedo",
            "culpa":      "Culpa",
            "lucidez":    "Lucidez",
            "corrupcion": "Corrupción",
        }
        barras = ""
        for clave, label in nombres.items():
            val = p[clave]
            llenas = int(val / 10)
            vacias = 10 - llenas
            barra = "█" * llenas + "░" * vacias
            barras += f"{label:<12} [{barra}] {val:>3}/100\n"

        aliento_barra = "●" * self.player.aliento + "○" * (10 - self.player.aliento)
        inv_txt = ", ".join(NOMBRES_ITEMS.get(i, i) for i in self.player.inventario) or "—"

        texto = (
            f"\n— Estado psicológico —\n\n\n"
            f"{barras}\n"
            f"Aliento del Umbral  [{aliento_barra}] {self.player.aliento}/10\n"
            f"Inventario: {inv_txt}\n\n"
            f"Lo que sentís va dejando marca.\n\n"
        )
        imagen = self.ui.cargar_imagen(
            _LEVEL_IMGS[min(self.current_level_index, len(_LEVEL_IMGS) - 1)]
        )
        self.ui.esperar_input(imagen, texto, opciones=False, player=self.player)

    def _mostrar_historial(self):
        if not self.player.historial:
            if self.player.memorias_gastadas > 0:
                self.ui.esperar_input(
                    self.ui.cargar_imagen("assets/lvl6.jpg"),
                    "\nNo recordás nada de lo que hiciste.\nEso también dice algo.\n",
                    opciones=False
                )
            return
        lineas = "\n".join(f"— {d}" for d in self.player.historial)
        texto = (
            f"\nLo que hiciste no desaparece.\nSolo se acumula.\n\n"
            f"{lineas}\n\n"
            f"Eso sos.\nTodo eso junto.\n"
        )
        self.ui.esperar_input(
            self.ui.cargar_imagen("assets/lvl6.jpg"),
            texto,
            opciones=False,
            player=self.player
        )

    # ─────────────────────────────────────────
    # SISTEMA DE FINALES
    # ─────────────────────────────────────────
    def determinar_final(self):
        # Ending secreto: fusión con El Otro
        if self.player.fusionado_con_otro:
            return (
                "\nEl Otro ya no está frente a vos.\n"
                "Porque ahora sos también él.\n\n"
                "No hay tensión.\n"
                "No hay dualidad.\n"
                "Solo la quietud de quien finalmente\n"
                "no tiene nada que esconder de sí mismo.\n\n"
                "Algunos llaman a eso paz.\n"
                "Otros lo llaman vaciamiento.\n"
                "La diferencia no importa\n"
                "cuando ya no hay dos voces para discutirlo.\n"
            )

        psique = self.player.psique
        v  = psique["violencia"]
        m  = psique["miedo"]
        c  = psique["culpa"]
        l  = psique["lucidez"]
        co = psique["corrupcion"]

        dominante = max(psique, key=psique.get)
        segundo   = sorted(psique, key=psique.get, reverse=True)[1]
        val_dom   = psique[dominante]
        val_seg   = psique[segundo]

        combo = (dominante, segundo) if val_seg >= 35 else (dominante, None)

        if combo == ("miedo", "culpa") or combo == ("culpa", "miedo"):
            return "\nNo corrés.\nNo te quedás.\nEstás suspendido entre las dos.\nEl miedo dice: movete.\nLa culpa dice: no merecés escapar.\nY así…\nel tiempo pasa alrededor.\nSin vos adentro.\n"
        if combo == ("violencia", "miedo") or combo == ("miedo", "violencia"):
            return "\nAtacás porque tenés miedo.\nNo porque seas valiente.\nCada golpe es un grito\nque nadie escucha.\nIncluyéndote.\nLa violencia no te protegió.\nSolo te aisló más rápido.\n"
        if combo == ("culpa", "lucidez") or combo == ("lucidez", "culpa"):
            return "\nLo entendés todo.\nCada error.\nCada momento en que pudiste elegir distinto.\nLa lucidez no te absuelve.\nTe hace cómplice\nde cada versión tuya\nque sabía\ny eligió igual.\n"
        if combo == ("miedo", "lucidez") or combo == ("lucidez", "miedo"):
            return "\nVes exactamente por qué tenés miedo.\nPodés nombrarlo.\nDescribirlo.\nRastrearlo hasta su origen.\nY aun así…\nno desaparece.\nEntender no es sanar.\nA veces es solo\nuna forma más precisa de sufrir.\n"
        if combo == ("violencia", "culpa") or combo == ("culpa", "violencia"):
            return "\nGolpeaste.\nY después lo lamentaste.\nUna y otra vez.\nEl ciclo no es debilidad.\nEs la forma que encontraste\nde no quedarte quieto\ncon lo que hiciste.\nEl movimiento como anestesia.\nFunciona.\nHasta que deja de funcionar.\n"
        if combo == ("corrupcion", "lucidez") or combo == ("lucidez", "corrupcion"):
            return "\nLo ves.\nTodo.\nSin filtros.\nSin excusas.\nY aún así…\nno te detenés.\nAlgo en vos entiende.\nY algo en vos elige continuar.\nNo sos víctima.\nNo sos héroe.\nSos voluntad.\nY el abismo… ahora tiene ojos.\n"

        if dominante == "corrupcion" and co >= 40:
            return "\nEl silencio ya no te resulta ajeno.\nLate contigo.\nLa cueva… respira como vos.\nNo entraste a destruir nada.\nEntraste a recordar.\nY ahora…\nalguien más desciende.\nVos esperás.\n"
        if dominante == "lucidez" and co < 50:
            return "\nNo hay salida.\nPero tampoco prisión.\nLo que enfrentaste…\nno desaparece.\nSe integra.\nDas un paso.\nNo hacia afuera.\nSino hacia algo más amplio.\nEl ciclo… no se rompe.\nSe comprende.\n"
        if dominante == "miedo":
            return "\nCorrés.\nPero no hay dirección.\nLas puertas ya no existen.\nEl espacio se pliega.\nTu mente intenta sostener algo que ya no tiene forma.\nY entonces…\ntodo se fragmenta.\nSeguís ahí.\nPero ya no sabés qué sos.\n"
        if dominante == "violencia":
            return "\nIntentaste destruirlo.\nPero nunca estuvo separado.\nCada golpe fue hacia adentro.\nCada intento… una grieta más.\nHasta que no quedó nada coherente.\nSolo impulso.\nSolo reacción.\nSolo ruptura.\n"
        if dominante == "culpa":
            return "\nRecordás.\nUna y otra vez.\nCada decisión.\nCada omisión.\nCada instante en el que pudiste ser distinto.\nPero no lo fuiste.\nNo hay castigo externo.\nNo hace falta.\nVos ya sos suficiente.\n"
        return "\nSalís.\nO al menos… eso parece.\nEl mundo sigue.\nLa gente habla.\nEl tiempo avanza.\nPero algo falta.\nNo recordás qué.\nY nunca lo harás.\n"
