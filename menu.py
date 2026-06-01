import pygame
import sys
from save_system import existe_partida

class Menu:

    def __init__(self, ui):
        self.ui = ui

    # ─────────────────────────────────────────
    # PANTALLA PRINCIPAL
    # Devuelve: "nueva", "cargar", "creditos", "salir"
    # ─────────────────────────────────────────
    def mostrar(self):
        imagen = self.ui.cargar_imagen("assets/menu.jpg")

        hay_guardado = existe_partida()

        opciones = ["Nueva partida"]
        if hay_guardado:
            opciones.append("Continuar")
        opciones.append("Modo Lectura  [sin combate]")
        opciones.append("Créditos")
        opciones.append("Salir")

        texto = """
Descenso al Umbral


El mundo se consume en silencio.
Los que descienden no regresan.
Los que regresan... ya no son los mismos.


¿Quién sos vos para intentarlo?
"""

        eleccion = self.ui.esperar_input(imagen, texto, opciones=True, opciones_lista=opciones)

        # Mapear índice a acción
        mapa = {}
        i = 1
        mapa[str(i)] = "nueva"
        i += 1
        if hay_guardado:
            mapa[str(i)] = "cargar"
            i += 1
        mapa[str(i)] = "lectura"
        i += 1
        mapa[str(i)] = "creditos"
        i += 1
        mapa[str(i)] = "salir"

        return mapa.get(eleccion, "salir")

    # ─────────────────────────────────────────
    # PANTALLA DE CRÉDITOS
    # ─────────────────────────────────────────
    def mostrar_creditos(self):
        import pygame, sys
        imagen = self.ui.cargar_imagen("assets/menu.jpg")

        bloques = [
            "Descenso al Umbral",
            "Desarrollo y diseño\nMarcos Martínez",
            "Inspirado en\nDark Souls  ·  Elden Ring\nPsicología Junguiana\nFilosofía esotérica",
            '"El dungeon no es un lugar.\nEs una proyección."',
            "[ ESPACIO para volver ]",
        ]

        clock = pygame.time.Clock()
        font  = self.ui.font
        ui    = self.ui

        for bloque in bloques:
            # Fade in del bloque
            for alpha in range(0, 256, 8):
                clock.tick(60)
                ui.canvas.fill(ui.bg_color)
                ui.canvas.blit(imagen, (ui.IMG_X, ui.IMG_Y))

                surf = pygame.Surface((ui.width, ui.height), pygame.SRCALPHA)
                y = 220
                for linea in bloque.split("\n"):
                    r = font.render(linea, True, ui.text_color)
                    r.set_alpha(alpha)
                    surf.blit(r, (ui.width // 2 - r.get_width() // 2, y))
                    y += 36
                ui.canvas.blit(surf, (0, 0))
                ui._blit_canvas()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit(); sys.exit()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        return

            # Pausa visible
            pausa = 90 if bloque != "[ ESPACIO para volver ]" else 9999
            for _ in range(pausa):
                clock.tick(60)
                ui.canvas.fill(ui.bg_color)
                ui.canvas.blit(imagen, (ui.IMG_X, ui.IMG_Y))
                y = 220
                for linea in bloque.split("\n"):
                    r = font.render(linea, True, ui.text_color)
                    ui.canvas.blit(r, (ui.width // 2 - r.get_width() // 2, y))
                    y += 36
                ui._blit_canvas()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit(); sys.exit()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        return

            # Fade out
            for alpha in range(255, -1, -8):
                clock.tick(60)
                ui.canvas.fill(ui.bg_color)
                ui.canvas.blit(imagen, (ui.IMG_X, ui.IMG_Y))
                surf = pygame.Surface((ui.width, ui.height), pygame.SRCALPHA)
                y = 220
                for linea in bloque.split("\n"):
                    r = font.render(linea, True, ui.text_color)
                    r.set_alpha(alpha)
                    surf.blit(r, (ui.width // 2 - r.get_width() // 2, y))
                    y += 36
                ui.canvas.blit(surf, (0, 0))
                ui._blit_canvas()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit(); sys.exit()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        return
