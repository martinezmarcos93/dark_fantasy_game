from ui import UI
from player import Player
 
class GameEngine:
    def __init__(self):
        self.player = None
        self.current_level_index = 0
        self.levels = []
        self.ui = UI()
 
# -------------------------
# CREAR JUGADOR (PYGAME)
# -------------------------
    def crear_personaje(self):
 
        texto = """
        === CREACIÓN DE PERSONAJE ===
 
        Elegí tu clase:
        """
 
        opciones = ["Guerrero", "Hechicero", "Ladrón"]
 
        eleccion = self.mostrar_nivel("assets/lvl1.jpg", texto, opciones=True, opciones_lista=opciones)
 
        clases = {
            "1": "Guerrero",
            "2": "Hechicero",
            "3": "Ladrón"
        }
 
        clase = clases.get(eleccion, "Errante")
 
        # Nombre temporal automático (luego lo hacemos interactivo)
        nombre = "Viajero"
 
        self.player = Player(nombre, clase)
 
    # -------------------------
    # CARGAR NIVELES
    # -------------------------
    def cargar_niveles(self):
        # IMPORTANTE: después vamos a importar desde /levels
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
 
 
    def mostrar_nivel(self, imagen_path, texto, opciones=True, opciones_lista=None):
        imagen = self.ui.cargar_imagen(imagen_path)
        return self.ui.esperar_input(imagen, texto, opciones, opciones_lista)
    # -------------------------
    # LOOP PRINCIPAL
    # -------------------------
    def jugar(self):
        self.crear_personaje()
        self.cargar_niveles()
 
 
        while self.player.alive and self.current_level_index < len(self.levels):
            nivel = self.levels[self.current_level_index]
 
 
            resultado = nivel.jugar(self.player, self)
 
            if resultado == "muerte":
                self.player.morir("Fallaste en la prueba.")
                break
 
            elif resultado == "continuar":
                self.current_level_index += 1
 
            else:
                print("Error en el nivel.")
                break
 
        self.final_juego()
 
    # -------------------------
    # FINAL DEL JUEGO
    # -------------------------
    def final_juego(self):
 
        if not self.player.alive:
            texto = """
    Tu historia termina en la oscuridad.
    """
            self.ui.esperar_input(
                self.ui.cargar_imagen("assets/lvl6.jpg"),
                texto,
                opciones=False
            )
            return
 
        ending = self.determinar_final()
 
        texto = f"""
    Tu destino final es:
 
    {ending}
    """
 
        self.ui.esperar_input(
            self.ui.cargar_imagen("assets/lvl6.jpg"),
            texto,
            opciones=False
        )
 
 
    # -------------------------
    # SISTEMA DE FINALES
    # -------------------------
    def determinar_final(self):
        psique = self.player.psique
 
        v = psique["violencia"]
        m = psique["miedo"]
        c = psique["culpa"]
        l = psique["lucidez"]
        co = psique["corrupcion"]
 
        # -------------------------
        # FINAL 1 — ENTIDAD DEL ABISMO
        # -------------------------
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
 
        # -------------------------
        # FINAL 2 — LUCIDEZ TOTAL
        # -------------------------
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
 
        # -------------------------
        # FINAL 3 — LOCURA POR MIEDO
        # -------------------------
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
 
        # -------------------------
        # FINAL 4 — AUTODESTRUCCIÓN
        # -------------------------
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
 
        # -------------------------
        # FINAL 5 — CULPA ETERNA
        # -------------------------
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
 
        # -------------------------
        # FINAL 6 — ENTIDAD CONSCIENTE (HÍBRIDO)
        # -------------------------
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
 
        # -------------------------
        # FINAL 7 — DISOLUCIÓN
        # -------------------------
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
 
        # -------------------------
        # FINAL 8 — OLVIDO
        # -------------------------
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