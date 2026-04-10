import pygame
import sys
import os
import random


class UI:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        # Pantalla
        self.width = 1000
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Descenso al Umbral")

        # Fuente
        self.font = pygame.font.Font("fonts/Goth.ttf", 22)

        # Colores
        self.text_color = (180, 180, 180)
        self.bg_color = (5, 5, 5)

        # Música
        self.reproducir_musica()

    # -------------------------
    # CARGAR IMAGEN
    # -------------------------
    def cargar_imagen(self, path):
        image = pygame.image.load(path).convert()
        image = pygame.transform.scale(image, (500, 600))
        return image

    # -------------------------
    # DIBUJAR TEXTO (CON WRAP)
    # -------------------------
    def dibujar_texto(self, texto, scroll_y=0):
        x_offset = 520
        y_offset = 40 + scroll_y
        max_width = 400
        line_height = 28

        lineas_originales = texto.split("\n")

        for linea in lineas_originales:
            palabras = linea.split(" ")
            linea_actual = ""

            for palabra in palabras:
                test_line = linea_actual + palabra + " "
                ancho, _ = self.font.size(test_line)

                if ancho < max_width:
                    linea_actual = test_line
                else:
                    render = self.font.render(linea_actual, True, self.text_color)
                    self.screen.blit(render, (x_offset, y_offset))
                    y_offset += line_height
                    linea_actual = palabra + " "

            render = self.font.render(linea_actual, True, self.text_color)
            self.screen.blit(render, (x_offset, y_offset))
            y_offset += line_height

    # -------------------------
    # RENDER NORMAL (SIN EFECTOS)
    # -------------------------
    def render(self, imagen, texto, scroll_y=0, opciones=None):
        self.screen.fill(self.bg_color)
        self.screen.blit(imagen, (0, 0))

        self.dibujar_texto(texto, scroll_y)

        botones = []

        if opciones:
            x = 520
            y = 420

            mouse_pos = pygame.mouse.get_pos()

            for i, opcion in enumerate(opciones):
                txt = f"{i+1}. {opcion}"

                # 🔥 detectar hover
                render = self.font.render(txt, True, self.text_color)
                rect = render.get_rect(topleft=(x, y))

                if rect.collidepoint(mouse_pos):
                    render = self.font.render(txt, True, (255, 100, 100))  # hover rojo

                self.screen.blit(render, rect)
                botones.append((rect, str(i+1)))

                y += 40

        pygame.display.flip()
        return botones


    # -------------------------
    # INPUT DEL USUARIO
    # -------------------------
    def esperar_input(self, imagen, texto, opciones=True, opciones_lista=None):
        clock = pygame.time.Clock()
        scroll_y = 0

        self.fade_in(imagen, texto)

        while True:
            clock.tick(60)

            if not pygame.mixer.music.get_busy():
                self.reproducir_musica()

            botones = self.render(imagen, texto, scroll_y, opciones_lista)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:

                    # scroll
                    if event.key == pygame.K_DOWN:
                        scroll_y -= 20
                    if event.key == pygame.K_UP:
                        scroll_y += 20

                    # sin opciones → SPACE
                    if not opciones:
                        if event.key == pygame.K_SPACE:
                            return "continuar"

                    # con opciones → teclado
                    else:
                        if event.key == pygame.K_1:
                            return "1"
                        if event.key == pygame.K_2:
                            return "2"
                        if event.key == pygame.K_3:
                            return "3"

                # 🖱️ CLICK (AHORA SEGURO)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if opciones_lista:  # 🔥 SOLO si hay botones
                        mouse_pos = pygame.mouse.get_pos()

                        for rect, valor in botones:
                            if rect.collidepoint(mouse_pos):
                                return valor

    # -------------------------
    # FADE IN CORRECTO (SIN BUG)
    # -------------------------
    def fade_in(self, imagen, texto):
        temp = imagen.copy()

        for alpha in range(0, 255, 15):
            self.screen.fill(self.bg_color)

            temp.set_alpha(alpha)
            self.screen.blit(temp, (0, 0))

            self.dibujar_texto(texto)

            pygame.display.flip()
            pygame.time.delay(20)

    # -------------------------
    # MÚSICA ALEATORIA
    # -------------------------
    def reproducir_musica(self):
        carpeta = "music"

        if not os.path.exists(carpeta):
            return

        canciones = [f for f in os.listdir(carpeta) if f.endswith(".mp3")]

        if not canciones:
            return

        cancion = random.choice(canciones)
        ruta = os.path.join(carpeta, cancion)

        pygame.mixer.music.load(ruta)
        pygame.mixer.music.play()
        carpeta = "music"
        canciones = [f for f in os.listdir(carpeta) if f.endswith(".mp3")]

        if not canciones:
            return

        cancion = random.choice(canciones)
        ruta = os.path.join(carpeta, cancion)

        pygame.mixer.music.load(ruta)
        pygame.mixer.music.play()

    def dibujar_opciones(self, opciones):
        botones = []

        x = 520
        y = 400

        for i, opcion in enumerate(opciones):
            texto = f"{i+1}. {opcion}"

            render = self.font.render(texto, True, (255, 255, 255))
            rect = render.get_rect(topleft=(x, y))

            self.screen.blit(render, rect)
            botones.append((rect, str(i+1)))

            y += 40

        return botones