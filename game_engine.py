from ui import UI, EscapeAlMenu
from player import Player
from menu import Menu
from intro import Intro
from save_system import (guardar_partida, cargar_partida, borrar_partida,
                         listar_slots, guardar_ng_plus, cargar_ng_plus, existe_ng_plus)

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
        imagen = self.ui.cargar_imagen("assets/lvl1.jpg")

        texto_clase = """
=== CREACIÓN DE PERSONAJE ===


Elegí tu senda:
"""
        opciones = ["Guerrero", "Hechicero", "Ladrón"]
        eleccion = self.mostrar_nivel("assets/lvl1.jpg", texto_clase, opciones=True, opciones_lista=opciones)

        clases = {"1": "Guerrero", "2": "Hechicero", "3": "Ladrón"}
        clase = clases.get(eleccion, "Errante")

        nombre = self.ui.pedir_nombre(imagen, clase)
        self.player = Player(nombre, clase)

        psique_previa = cargar_ng_plus()
        if psique_previa:
            self._aplicar_herencia_ng_plus(psique_previa)

        self._elegir_dificultad()

    def _aplicar_herencia_ng_plus(self, psique_previa):
        """
        Transfiere el 20% de la psique del run anterior como "eco" psicológico.
        Muestra una pantalla narrativa informando al jugador del efecto.
        """
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
        from levels.level1 import Level1
        from levels.level2 import Level2
        from levels.level3 import Level3
        from levels.level4 import Level4
        from levels.level5 import Level5
        from levels.level6 import Level6

        self.levels = [
            Level1(),
            Level2(),
            Level3(),
            Level4(),
            Level5(),
            Level6()
        ]

    # ─────────────────────────────────────────
    # MOSTRAR NIVEL — wrapper central
    # ─────────────────────────────────────────
    def mostrar_nivel(self, imagen_path, texto, opciones=True, opciones_lista=None):
        imagen = self.ui.cargar_imagen(imagen_path)
        return self.ui.esperar_input(imagen, texto, opciones, opciones_lista, self.player,
                                     nivel=self.current_level_index)

    # ─────────────────────────────────────────
    # COMBATE NARRATIVO — nuevo sistema multironda
    # Recibe un objeto Enemy (de enemies.py).
    # Delega toda la lógica a combat_system.combate_completo().
    # Devuelve "vivo" o "muerte".
    # ─────────────────────────────────────────
    def combate_narrativo(self, enemy):
        if self.modo_lectura:
            self.mostrar_nivel(enemy.imagen, enemy.texto_intro, opciones=False)
            self.player.modificar_psique(enemy.psique_victoria_jugador)
            return "vivo"
        # Aplicar modificador de dificultad global (no muta la definición original)
        import math
        enemy.dificultad = max(1, round(enemy.dificultad * self.dificultad_global))
        from combat_system import combate_completo
        return combate_completo(enemy, self.player, self)

    # ─────────────────────────────────────────
    # LOOP PRINCIPAL
    # ─────────────────────────────────────────
    def jugar(self):
        try:
            while self.player.alive and self.current_level_index < len(self.levels):
                nivel = self.levels[self.current_level_index]
                resultado = nivel.jugar(self.player, self)

                if resultado == "muerte":
                    self.player.morir("Fallaste en la prueba.")
                    break

                elif resultado == "continuar":
                    self._mostrar_resumen_psique()
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
    # CARGAR JUEGO DESDE JSON
    # ─────────────────────────────────────────
    def _elegir_slot(self, modo="cargar"):
        slots = listar_slots()
        imagen = self.ui.cargar_imagen("assets/lvl1.jpg")

        if modo == "cargar":
            opciones_validas = [s for s in slots if not s["vacio"]]
            if not opciones_validas:
                return None
            labels = []
            ids    = []
            for s in slots:
                if s["vacio"]:
                    labels.append(f"Slot {s['slot']+1}  [vacío]")
                else:
                    labels.append(
                        f"Slot {s['slot']+1}  — {s['nombre']} ({s['clase']})  Nivel {s['nivel']}"
                    )
                    ids.append(s["slot"])
            # Filtrar labels solo de slots con datos
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

        else:  # modo == "nueva"
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
        return True

    # ─────────────────────────────────────────
    # PANTALLA DE MUERTE
    # Imagen según clase + texto según nivel donde murió
    # ─────────────────────────────────────────
    def pantalla_muerte(self):
        clase = self.player.clase
        nivel = self.current_level_index  # 0-3 para muertes en combate

        imagenes = {
            "Guerrero":  "assets/death_warrior.jpg",
            "Hechicero": "assets/death_mage.jpg",
            "Ladrón":    "assets/death_rogue.jpg",
        }
        imagen_path = imagenes.get(clase, "assets/lvl6.jpg")

        textos_guerrero = [
            f"""
{self.player.name}.

La piedra no distingue entre los valientes y los demás.
Solo entre lo que resiste... y lo que cede.

Cediste.

El Umbral absorbió tu fuerza.
Ahora es suya.
""",
            f"""
{self.player.name}.

Peleaste contra vos mismo.
Y perdiste.

No hay vergüenza en eso.
Solo hay silencio.

El reflejo sigue ahí.
Con tu cara.
Con tu fuerza.
Sin vos.
""",
            f"""
{self.player.name}.

El Sacerdote no te mató.
Tomó algo.

Y sin eso...
el cuerpo siguió un rato más.
Pero vos ya no estabas adentro.
""",
            f"""
{self.player.name}.

La Sombra Soberana te conocía
mejor de lo que te conocías vos.

Cada derrota que alguna vez tuviste
ya estaba en ella.

Ahora también estás vos.
"""
        ]

        textos_hechicero = [
            f"""
{self.player.name}.

La piedra no tiene memoria.
Tenías razón.

Pero tampoco tiene piedad.

Tu hechizo volvió.
Y fue más honesto que vos.
""",
            f"""
{self.player.name}.

El conocimiento que usaste contra el Reflejo
era tuyo.

Y él te lo devolvió
multiplicado por todo lo que sabías.

Moriste de tu propia comprensión.
""",
            f"""
{self.player.name}.

Intentaste nombrarlo.
Fallaste.

Lo que no puede ser nombrado
tampoco puede ser detenido.

Se llevó algo tuyo.
El nombre que más importaba.
El tuyo.
""",
            f"""
{self.player.name}.

Había demasiadas historias en la Sombra.
No podías contenerlas todas.

Una mente que lo intenta igual
se rompe igual.

La tuya resistió hasta el final.
Eso es suficiente.
O debería serlo.
"""
        ]

        textos_ladron = [
            f"""
{self.player.name}.

Siempre hay alguien que te ve
aunque no quieras ser visto.

El Guardián no tenía ojos.
Pero te encontró igual.

Algunas cosas no se pueden esquivar.
Solo se pueden recibir.
""",
            f"""
{self.player.name}.

Intentaste desaparecer.
El Reflejo sabía adónde ibas
antes de que lo supieras vos.

Porque eras predecible.
No por tus movimientos.
Por tus miedos.
""",
            f"""
{self.player.name}.

Te vaciaste de intención.
Casi lo lograste.

Pero quedó un rastro.
Pequeño.
Suficiente.

El Sacerdote marcó ese rastro.
Y lo que está marcado
no puede ocultarse más.
""",
            f"""
{self.player.name}.

Le diste algo tuyo como señuelo.
La Sombra no lo aceptó.

Fue por vos directamente.

Porque ya te tenía adentro
desde antes de que empezara la pelea.
"""
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
        texto = f"""
{self.player.name}.

Tu destino:

{ending}
"""
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

        # Acción más usada
        if sc["acciones"]:
            accion_top = max(sc["acciones"], key=sc["acciones"].get)
            veces_top  = sc["acciones"][accion_top]
            linea_accion = f"Acción más usada:   {accion_top}  ({veces_top} veces)"
        else:
            linea_accion = "Acción más usada:   —"

        texto = f"""
— Lo que dejaste en el camino —


Daño infligido:     {sc['daño_infligido']}
Daño recibido:      {sc['daño_recibido']}
Rondas ganadas:     {sc['rondas_ganadas']} / {total_rondas}  ({winrate}%)
Golpes críticos:    {sc['criticos']}
{linea_accion}

Estos números no mienten.
Aunque vos sí lo hayas hecho.

"""
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

        texto = f"""
— Estado psicológico —


{barras}

Lo que sentís va dejando marca.

"""
        imagen = self.ui.cargar_imagen(
            ["assets/lvl1.jpg","assets/lvl2.jpg","assets/lvl3.jpg",
             "assets/lvl4.jpg","assets/lvl5.jpg","assets/lvl6.jpg"]
            [min(self.current_level_index, 5)]
        )
        self.ui.esperar_input(imagen, texto, opciones=False, player=self.player)

    def _mostrar_historial(self):
        if not self.player.historial:
            return
        lineas = "\n".join(f"— {d}" for d in self.player.historial)
        texto = f"""
Lo que hiciste no desaparece.
Solo se acumula.

{lineas}

Eso sos.
Todo eso junto.
"""
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

        # Combinación dominante + segundo significativo (ambos >= 35)
        combo = (dominante, segundo) if val_seg >= 35 else (dominante, None)

        # ── Combos dobles ────────────────────────────────────────
        if combo == ("miedo", "culpa") or combo == ("culpa", "miedo"):
            return """
No corrés.
No te quedás.
Estás suspendido entre las dos.
El miedo dice: movete.
La culpa dice: no merecés escapar.
Y así…
el tiempo pasa alrededor.
Sin vos adentro.
"""
        if combo == ("violencia", "miedo") or combo == ("miedo", "violencia"):
            return """
Atacás porque tenés miedo.
No porque seas valiente.
Cada golpe es un grito
que nadie escucha.
Incluyéndote.
La violencia no te protegió.
Solo te aisló más rápido.
"""
        if combo == ("culpa", "lucidez") or combo == ("lucidez", "culpa"):
            return """
Lo entendés todo.
Cada error.
Cada momento en que pudiste elegir distinto.
La lucidez no te absuelve.
Te hace cómplice
de cada versión tuya
que sabía
y eligió igual.
"""
        if combo == ("miedo", "lucidez") or combo == ("lucidez", "miedo"):
            return """
Ves exactamente por qué tenés miedo.
Podés nombrarlo.
Describirlo.
Rastrearlo hasta su origen.
Y aun así…
no desaparece.
Entender no es sanar.
A veces es solo
una forma más precisa de sufrir.
"""
        if combo == ("violencia", "culpa") or combo == ("culpa", "violencia"):
            return """
Golpeaste.
Y después lo lamentaste.
Una y otra vez.
El ciclo no es debilidad.
Es la forma que encontraste
de no quedarte quieto
con lo que hiciste.
El movimiento como anestesia.
Funciona.
Hasta que deja de funcionar.
"""
        if combo == ("corrupcion", "lucidez") or combo == ("lucidez", "corrupcion"):
            return """
Lo ves.
Todo.
Sin filtros.
Sin excusas.
Y aún así…
no te detenés.
Algo en vos entiende.
Y algo en vos elige continuar.
No sos víctima.
No sos héroe.
Sos voluntad.
Y el abismo… ahora tiene ojos.
"""

        # ── Endings por stat dominante único ─────────────────────
        if dominante == "corrupcion" and co >= 40:
            return """
El silencio ya no te resulta ajeno.
Late contigo.
La cueva… respira como vos.
No entraste a destruir nada.
Entraste a recordar.
Y ahora…
alguien más desciende.
Vos esperás.
"""
        if dominante == "lucidez" and co < 50:
            return """
No hay salida.
Pero tampoco prisión.
Lo que enfrentaste…
no desaparece.
Se integra.
Das un paso.
No hacia afuera.
Sino hacia algo más amplio.
El ciclo… no se rompe.
Se comprende.
"""
        if dominante == "miedo":
            return """
Corrés.
Pero no hay dirección.
Las puertas ya no existen.
El espacio se pliega.
Tu mente intenta sostener algo que ya no tiene forma.
Y entonces…
todo se fragmenta.
Seguís ahí.
Pero ya no sabés qué sos.
"""
        if dominante == "violencia":
            return """
Intentaste destruirlo.
Pero nunca estuvo separado.
Cada golpe fue hacia adentro.
Cada intento… una grieta más.
Hasta que no quedó nada coherente.
Solo impulso.
Solo reacción.
Solo ruptura.
"""
        if dominante == "culpa":
            return """
Recordás.
Una y otra vez.
Cada decisión.
Cada omisión.
Cada instante en el que pudiste ser distinto.
Pero no lo fuiste.
No hay castigo externo.
No hace falta.
Vos ya sos suficiente.
"""
        # Psique equilibrada o todos los valores bajos → salida vacía
        return """
Salís.
O al menos… eso parece.
El mundo sigue.
La gente habla.
El tiempo avanza.
Pero algo falta.
No recordás qué.
Y nunca lo harás.
"""
