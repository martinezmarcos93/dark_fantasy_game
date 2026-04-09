import pygame
import sys

class UI:
    def __init__(self):
        pygame.init()

        self.width = 1000
        self.height = 600

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Descenso al Umbral")

        self.font = pygame.font.SysFont("consolas", 20)

        # Colores
        self.bg_color = (10, 10, 10)
        self.text_color = (200, 200, 200)

    def cargar_imagen(self, path):
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, (500, 600))
        return image

    def dibujar_texto(self, texto):
        x_offset = 520
        y_offset = 20

        lineas = texto.split("\n")

        for linea in lineas:
            render = self.font.render(linea, True, self.text_color)
            self.screen.blit(render, (x_offset, y_offset))
            y_offset += 25

    def render(self, imagen, texto):
        self.screen.fill(self.bg_color)

        # Dibujar imagen
        self.screen.blit(imagen, (0, 0))

        # Dibujar texto
        self.dibujar_texto(texto)

        pygame.display.flip()

    def esperar_input(self, imagen, texto):
        clock = pygame.time.Clock()

        while True:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:

                    if event.unicode == "1":
                        return "1"
                    if event.unicode == "2":
                        return "2"
                    if event.unicode == "3":
                        return "3"

            self.render(imagen, texto)