import random
from ui import UI, EscapeAlMenu
from player import Player
from menu import Menu
from intro import Intro
from save_system import guardar_partida, cargar_partida, borrar_partida

class GameEngine:
    def __init__(self):
        self.player = None
        self.current_level_index = 0
        self.levels = []
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
                borrar_partida()
                self.current_level_index = 0
                try:
                    self.intro.mostrar()
                    self.crear_personaje()
                except EscapeAlMenu:
                    continue  # volver al menú principal
                self.cargar_niveles()
                self.jugar()

            elif accion == "cargar":
                exito = self.cargar_juego()
                if exito:
                    self.cargar_niveles()
                    self.jugar()

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
        return self.ui.esperar_input(imagen, texto, opciones, opciones_lista, self.player)

    # ─────────────────────────────────────────
    # COMBATE NARRATIVO — nuevo sistema multironda
    # Recibe un objeto Enemy (de enemies.py).
    # Delega toda la lógica a combat_system.combate_completo().
    # Devuelve "vivo" o "muerte".
    # ─────────────────────────────────────────
    def combate_narrativo(self, enemy):
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
                    self.current_level_index += 1
                    guardar_partida(self.player, self.current_level_index)

                else:
                    break

            self.final_juego()

        except EscapeAlMenu:
            # Guardar estado y volver al loop principal (iniciar())
            if self.player and self.player.alive:
                guardar_partida(self.player, self.current_level_index)
            return

    # ─────────────────────────────────────────
    # CARGAR JUEGO DESDE JSON
    # ─────────────────────────────────────────
    def cargar_juego(self):
        data = cargar_partida()
        if not data:
            return False

        self.player = Player(data["nombre"], data["clase"])
        self.player.stats  = data["stats"]
        self.player.psique = data["psique"]
        self.player.alive  = data["alive"]
        # Restaurar vida y energía si están guardadas
        self.player.vida   = data.get("vida", self.player.vida_max)
        self.player.energia = data.get("energia", self.player.energia_max)
        self.current_level_index = data["nivel_actual"]
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
            borrar_partida()
            return

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
        borrar_partida()

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

        if co > 70:
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
        elif l > 70 and co < 50:
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
        elif m > 60:
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
        elif v > 60 and co > 40:
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
        elif c > 50:
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
        elif co > 50 and l > 50:
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
        elif m > 30 and l < 30:
            return """
Te desvanecés lentamente.
Sin ruido.
Sin forma.
Sin resistencia.
No hay dolor.
No hay comprensión.
Solo una pérdida progresiva de todo.
Incluso de la idea de haber sido algo.
"""
        else:
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
