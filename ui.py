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
        self.font = pygame.font.SysFont("consolas", 20)

        # Colores
        self.bg_color = (10, 10, 10)
        self.text_color = (200, 200, 200)

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
    def dibujar_texto(self, texto):
        x_offset = 520
        y_offset = 40
        max_width = 400
        line_height = 28

        # 🔥 respetar saltos de línea originales
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

            # dibujar última parte de la línea
            render = self.font.render(linea_actual, True, self.text_color)
            self.screen.blit(render, (x_offset, y_offset))
            y_offset += line_height

    # -------------------------
    # RENDER NORMAL (SIN EFECTOS)
    # -------------------------
    def render(self, imagen, texto):
        self.screen.fill(self.bg_color)
        self.screen.blit(imagen, (0, 0))
        self.dibujar_texto(texto)
        pygame.display.flip()

    # -------------------------
    # INPUT DEL USUARIO
    # -------------------------
    def esperar_input(self, imagen, texto, opciones=True):
        clock = pygame.time.Clock()

        # 🔥 Fade SOLO UNA VEZ al entrar
        self.fade_in(imagen, texto)

        while True:
            clock.tick(60)

            # 🔊 Control de música
            if not pygame.mixer.music.get_busy():
                self.reproducir_musica()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if not opciones:
                        return "continuar"

                    if event.unicode == "1":
                        return "1"
                    if event.unicode == "2":
                        return "2"
                    if event.unicode == "3":
                        return "3"

            # Render estable (sin fade)
            self.render(imagen, texto)

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