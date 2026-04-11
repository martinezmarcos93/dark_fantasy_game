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
        self.font      = pygame.font.Font("fonts/Goth.ttf", 24)
        self.font_btn  = pygame.font.Font("fonts/Goth.ttf", 24)

        # Colores
        self.text_color    = (80, 140, 60)      # verde podredumbre
        self.btn_color     = (110, 170, 85)     # verde más claro en reposo
        self.btn_hover     = (210, 40, 40)      # rojo brillante al hover
        self.divider_color = (50, 80, 35)       # verde oscuro para la línea
        self.bg_color      = (5, 5, 5)

        # ─────────────────────────────────────────
        # ZONAS FIJAS (corazón del nuevo sistema)
        # ─────────────────────────────────────────
        #
        #  ┌──────────────┬────────────────────────┐
        #  │              │   ZONA TEXTO           │
        #  │  ZONA IMAGEN │   y: 0 → 390           │
        #  │  x: 0→480    │   x: 490→980           │
        #  │  y: 0→600    ├────────────────────────┤
        #  │              │   ZONA BOTONES         │
        #  │              │   y: 400→600           │
        #  └──────────────┴────────────────────────┘

        self.IMG_X      = 0
        self.IMG_Y      = 0
        self.IMG_W      = 480
        self.IMG_H      = 600

        self.TEXT_X     = 495
        self.TEXT_Y     = 20
        self.TEXT_W     = 475          # ancho máximo del texto
        self.TEXT_H     = 370          # altura disponible antes de los botones
        self.LINE_H     = 28

        self.BTN_X      = 495
        self.BTN_Y      = 410          # siempre debajo de la línea divisoria
        self.BTN_H      = 40
        self.DIVIDER_Y  = 400          # línea visual entre texto y botones

        # Música
        self.reproducir_musica()

    # ─────────────────────────────────────────
    # CARGAR IMAGEN
    # ─────────────────────────────────────────
    def cargar_imagen(self, path):
        image = pygame.image.load(path).convert()
        image = pygame.transform.scale(image, (self.IMG_W, self.IMG_H))
        return image

    # ─────────────────────────────────────────
    # DIBUJAR TEXTO — confinado a ZONA TEXTO
    # El texto se recorta si excede TEXT_H
    # scroll_y desplaza hacia arriba el contenido
    # ─────────────────────────────────────────
    def dibujar_texto(self, texto, scroll_y=0):
        # Construir todas las líneas con word-wrap
        lineas_render = []
        for linea in texto.split("\n"):
            palabras = linea.split(" ")
            linea_actual = ""
            for palabra in palabras:
                test = linea_actual + palabra + " "
                ancho, _ = self.font.size(test)
                if ancho < self.TEXT_W - 10:
                    linea_actual = test
                else:
                    lineas_render.append(linea_actual)
                    linea_actual = palabra + " "
            lineas_render.append(linea_actual)

        # Dibujar sólo lo que cabe dentro de ZONA TEXTO
        # Usamos clip para que nada se derrame hacia los botones
        clip_rect = pygame.Rect(self.TEXT_X, self.TEXT_Y, self.TEXT_W, self.TEXT_H)
        self.screen.set_clip(clip_rect)

        y = self.TEXT_Y + scroll_y
        for linea in lineas_render:
            if y + self.LINE_H > self.TEXT_Y + self.TEXT_H:
                break                          # ya no entra más → cortar
            if y >= self.TEXT_Y:               # no dibujar lo que está "arriba" del clip
                render = self.font.render(linea, True, self.text_color)
                self.screen.blit(render, (self.TEXT_X, y))
            y += self.LINE_H

        self.screen.set_clip(None)             # liberar el clip

    # ─────────────────────────────────────────
    # DIBUJAR LÍNEA DIVISORIA
    # ─────────────────────────────────────────
    def dibujar_divisor(self):
        pygame.draw.line(
            self.screen,
            self.divider_color,
            (self.BTN_X, self.DIVIDER_Y),
            (self.width - 20, self.DIVIDER_Y),
            1
        )

    # ─────────────────────────────────────────
    # RENDER PRINCIPAL
    # ─────────────────────────────────────────
    def render(self, imagen, texto, scroll_y=0, opciones=None):
        self.screen.fill(self.bg_color)

        # Zona 1 — imagen
        self.screen.blit(imagen, (self.IMG_X, self.IMG_Y))

        # Zona 2 — texto (con clip)
        self.dibujar_texto(texto, scroll_y)

        # Línea separadora
        self.dibujar_divisor()

        # Zona 3 — botones (siempre en BTN_Y, nunca se mueven)
        botones = []
        if opciones:
            mouse_pos = pygame.mouse.get_pos()
            y = self.BTN_Y

            for i, opcion in enumerate(opciones):
                txt = f"{i+1}. {opcion}"

                render_normal = self.font_btn.render(txt, True, self.btn_color)
                rect = render_normal.get_rect(topleft=(self.BTN_X, y))

                if rect.collidepoint(mouse_pos):
                    render_final = self.font_btn.render(txt, True, self.btn_hover)
                else:
                    render_final = render_normal

                self.screen.blit(render_final, rect)
                botones.append((rect, str(i+1)))
                y += self.BTN_H

        pygame.display.flip()
        return botones

    # ─────────────────────────────────────────
    # INPUT DEL USUARIO
    # ─────────────────────────────────────────
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

                    # Scroll con flechas
                    if event.key == pygame.K_DOWN:
                        scroll_y -= self.LINE_H
                    if event.key == pygame.K_UP:
                        scroll_y += self.LINE_H
                    # Evitar scroll positivo excesivo
                    if scroll_y > 0:
                        scroll_y = 0

                    # Sin opciones → SPACE avanza
                    if not opciones:
                        if event.key == pygame.K_SPACE:
                            return "continuar"

                    # Con opciones → teclado
                    else:
                        if event.key == pygame.K_1:
                            return "1"
                        if event.key == pygame.K_2:
                            return "2"
                        if event.key == pygame.K_3:
                            return "3"

                # Click con mouse
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if opciones_lista:
                        mouse_pos = pygame.mouse.get_pos()
                        for rect, valor in botones:
                            if rect.collidepoint(mouse_pos):
                                return valor

    # ─────────────────────────────────────────
    # FADE IN
    # ─────────────────────────────────────────
    def fade_in(self, imagen, texto):
        temp = imagen.copy()

        for alpha in range(0, 255, 15):
            self.screen.fill(self.bg_color)

            temp.set_alpha(alpha)
            self.screen.blit(temp, (self.IMG_X, self.IMG_Y))

            self.dibujar_texto(texto)
            self.dibujar_divisor()

            pygame.display.flip()
            pygame.time.delay(20)

    # ─────────────────────────────────────────
    # INPUT DE NOMBRE — captura texto libre
    # Muestra el nombre mientras se escribe
    # Devuelve el string ingresado
    # ─────────────────────────────────────────
    def pedir_nombre(self, imagen, clase):
        clock = pygame.time.Clock()
        nombre = ""
        cursor_visible = True
        cursor_timer = 0

        while True:
            clock.tick(60)
            cursor_timer += 1
            if cursor_timer >= 30:
                cursor_visible = not cursor_visible
                cursor_timer = 0

            # Texto narrativo fijo
            texto = f"""
Has elegido la senda del {clase}.


Antes de descender...
¿Cómo te llaman?


"""
            # Render de pantalla
            self.screen.fill(self.bg_color)
            self.screen.blit(imagen, (self.IMG_X, self.IMG_Y))
            self.dibujar_texto(texto)
            self.dibujar_divisor()

            # Mostrar nombre escribiéndose en zona botones
            cursor = "|" if cursor_visible else " "
            linea_nombre = f"> {nombre}{cursor}"
            render_nombre = self.font_btn.render(linea_nombre, True, self.btn_hover)
            self.screen.blit(render_nombre, (self.BTN_X, self.BTN_Y))

            # Instrucción debajo
            instruccion = self.font.render("[ ENTER para confirmar ]", True, (60, 100, 45))
            self.screen.blit(instruccion, (self.BTN_X, self.BTN_Y + 50))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # Confirmar — si está vacío usar "Errante"
                        return nombre.strip() if nombre.strip() else "Errante"
                    elif event.key == pygame.K_BACKSPACE:
                        nombre = nombre[:-1]
                    elif len(nombre) < 20:
                        # Solo letras, números y espacios
                        if event.unicode.isprintable():
                            nombre += event.unicode

    # ─────────────────────────────────────────
    # MÚSICA ALEATORIA
    # ─────────────────────────────────────────
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

    # ─────────────────────────────────────────
    # dibujar_opciones — mantenido por compatibilidad
    # (ya no se usa internamente, pero no rompe nada)
    # ─────────────────────────────────────────
    def dibujar_opciones(self, opciones):
        botones = []
        y = self.BTN_Y

        for i, opcion in enumerate(opciones):
            texto = f"{i+1}. {opcion}"
            render = self.font.render(texto, True, (255, 255, 255))
            rect = render.get_rect(topleft=(self.BTN_X, y))
            self.screen.blit(render, rect)
            botones.append((rect, str(i+1)))
            y += self.BTN_H

        return botones
