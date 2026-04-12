import pygame
import sys
import os
import random


# ─────────────────────────────────────────
# EXCEPCIÓN PARA ESCAPE AL MENÚ
# Se lanza desde esperar_input / pedir_nombre
# El engine la atrapa en jugar() e iniciar() y vuelve al menú
# ─────────────────────────────────────────
class EscapeAlMenu(Exception):
    pass


class UI:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        # Resolución lógica fija — todo se dibuja aquí
        self.width  = 1000
        self.height = 600

        # Ventana real (redimensionable + maximizable)
        self.screen = pygame.display.set_mode(
            (self.width, self.height),
            pygame.RESIZABLE
        )
        pygame.display.set_caption("Descenso al Umbral")

        # Canvas lógico — siempre 1000×600
        self.canvas = pygame.Surface((self.width, self.height))

        # Fuente
        self.font      = pygame.font.Font("fonts/Goth.ttf", 24)
        self.font_btn  = pygame.font.Font("fonts/Goth.ttf", 24)

        # Colores
        self.text_color    = (80, 140, 60)
        self.btn_color     = (110, 170, 85)
        self.btn_hover     = (210, 40, 40)
        self.divider_color = (50, 80, 35)
        self.bg_color      = (5, 5, 5)

        # ─────────────────────────────────────────
        # ZONAS FIJAS
        # ─────────────────────────────────────────
        self.IMG_X      = 0
        self.IMG_Y      = 0
        self.IMG_W      = 480
        self.IMG_H      = 500

        # HUD
        self.HUD_X       = 0
        self.HUD_Y       = 508
        self.HUD_W       = 480
        self.HUD_H       = 92
        self.font_hud    = pygame.font.Font("fonts/Goth.ttf", 16)
        self.font_hud_sm = pygame.font.Font("fonts/Goth.ttf", 13)

        self.TEXT_X     = 495
        self.TEXT_Y     = 20
        self.TEXT_W     = 475
        self.TEXT_H     = 370
        self.LINE_H     = 28

        self.BTN_X      = 495
        self.BTN_Y      = 410
        self.BTN_H      = 40
        self.DIVIDER_Y  = 400

        # ─────────────────────────────────────────
        # SONIDOS DE TECLA (aleatorios)
        # Carga todos los .wav de sounds/ — reproduce uno al azar por tecla
        # ─────────────────────────────────────────
        self.sonidos_tecla = []
        carpeta_sounds = "sounds"
        if os.path.exists(carpeta_sounds):
            for archivo in sorted(os.listdir(carpeta_sounds)):
                if archivo.endswith(".wav") or archivo.endswith(".mp3"):
                    ruta = os.path.join(carpeta_sounds, archivo)
                    try:
                        s = pygame.mixer.Sound(ruta)
                        s.set_volume(0.4)
                        self.sonidos_tecla.append(s)
                    except Exception:
                        pass

        # Música
        self.reproducir_musica()

    # ─────────────────────────────────────────
    # CARGAR IMAGEN — respeta proporción con letterbox
    # ─────────────────────────────────────────
    def cargar_imagen(self, path):
        original = pygame.image.load(path).convert()
        orig_w, orig_h = original.get_size()

        escala = min(self.IMG_W / orig_w, self.IMG_H / orig_h)
        nuevo_w = int(orig_w * escala)
        nuevo_h = int(orig_h * escala)

        scaled = pygame.transform.scale(original, (nuevo_w, nuevo_h))

        canvas = pygame.Surface((self.IMG_W, self.IMG_H))
        canvas.fill(self.bg_color)

        offset_x = (self.IMG_W - nuevo_w) // 2
        offset_y = (self.IMG_H - nuevo_h) // 2
        canvas.blit(scaled, (offset_x, offset_y))

        return canvas

    # ─────────────────────────────────────────
    # DIBUJAR TEXTO
    # ─────────────────────────────────────────
    def dibujar_texto(self, texto, scroll_y=0):
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

        clip_rect = pygame.Rect(self.TEXT_X, self.TEXT_Y, self.TEXT_W, self.TEXT_H)
        self.canvas.set_clip(clip_rect)

        y = self.TEXT_Y + scroll_y
        for linea in lineas_render:
            if y + self.LINE_H > self.TEXT_Y + self.TEXT_H:
                break
            if y >= self.TEXT_Y:
                render = self.font.render(linea, True, self.text_color)
                self.canvas.blit(render, (self.TEXT_X, y))
            y += self.LINE_H

        self.canvas.set_clip(None)

    # ─────────────────────────────────────────
    # DIBUJAR LÍNEA DIVISORIA
    # ─────────────────────────────────────────
    def dibujar_divisor(self):
        pygame.draw.line(
            self.canvas,
            self.divider_color,
            (self.BTN_X, self.DIVIDER_Y),
            (self.width - 20, self.DIVIDER_Y),
            1
        )

    # ─────────────────────────────────────────
    # HUD
    # ─────────────────────────────────────────
    def dibujar_hud(self, player=None):
        pygame.draw.rect(self.canvas, (10, 10, 10),
                         (self.HUD_X, self.HUD_Y, self.HUD_W, self.HUD_H))
        pygame.draw.rect(self.canvas, (10, 10, 10),
                         (self.HUD_X, self.HUD_Y, self.HUD_W, self.HUD_H))
        pygame.draw.line(self.canvas, self.divider_color,
                         (self.HUD_X, self.HUD_Y),
                         (self.HUD_X + self.HUD_W, self.HUD_Y), 1)

        if player is None:
            return

        x = self.HUD_X + 12
        y = self.HUD_Y + 10

        nombre_txt = self.font_hud.render(
            f"{player.name}  ·  {player.clase}", True, (90, 130, 70))
        self.canvas.blit(nombre_txt, (x, y))
        y += 22

        self._dibujar_barra(x, y,
            valor=player.vida, maximo=player.vida_max,
            color_llena=(160, 30, 30), color_vacia=(40, 10, 10), etiqueta="HP")
        y += 22

        color_e = (40, 80, 160) if player.clase == "Hechicero" else (140, 120, 20)
        color_e_vacia = (10, 20, 40) if player.clase == "Hechicero" else (35, 30, 5)
        self._dibujar_barra(x, y,
            valor=player.energia, maximo=player.energia_max,
            color_llena=color_e, color_vacia=color_e_vacia,
            etiqueta=player.energia_nombre[:2].upper())

    def _dibujar_barra(self, x, y, valor, maximo, color_llena, color_vacia, etiqueta):
        BAR_W, BAR_H = 300, 14
        lbl = self.font_hud_sm.render(etiqueta, True, (100, 100, 100))
        self.canvas.blit(lbl, (x, y))
        bx = x + 30
        pygame.draw.rect(self.canvas, color_vacia, (bx, y + 1, BAR_W, BAR_H))
        proporcion = max(0, valor / maximo) if maximo > 0 else 0
        pygame.draw.rect(self.canvas, color_llena, (bx, y + 1, int(BAR_W * proporcion), BAR_H))
        pygame.draw.rect(self.canvas, (60, 60, 60), (bx, y + 1, BAR_W, BAR_H), 1)
        num_txt = self.font_hud_sm.render(f"{valor}/{maximo}", True, (120, 120, 120))
        self.canvas.blit(num_txt, (bx + BAR_W + 6, y))

    # ─────────────────────────────────────────
    # LETTERBOX — escala canvas lógico a ventana real
    # ─────────────────────────────────────────
    def _blit_canvas(self):
        win_w, win_h = self.screen.get_size()
        escala = min(win_w / self.width, win_h / self.height)
        nuevo_w = int(self.width  * escala)
        nuevo_h = int(self.height * escala)
        escalado = pygame.transform.scale(self.canvas, (nuevo_w, nuevo_h))
        offset_x = (win_w - nuevo_w) // 2
        offset_y = (win_h - nuevo_h) // 2
        self.screen.fill((0, 0, 0))
        self.screen.blit(escalado, (offset_x, offset_y))
        pygame.display.flip()

    # ─────────────────────────────────────────
    # MOUSE → coordenadas logicas
    # ─────────────────────────────────────────
    def _mouse_logico(self):
        mx, my = pygame.mouse.get_pos()
        win_w, win_h = self.screen.get_size()
        escala = min(win_w / self.width, win_h / self.height)
        nuevo_w = int(self.width  * escala)
        nuevo_h = int(self.height * escala)
        offset_x = (win_w - nuevo_w) // 2
        offset_y = (win_h - nuevo_h) // 2
        lx = (mx - offset_x) / escala
        ly = (my - offset_y) / escala
        return (lx, ly)

    # ─────────────────────────────────────────
    # RENDER PRINCIPAL
    # ─────────────────────────────────────────
    def render(self, imagen, texto, scroll_y=0, opciones=None, player=None):
        self.canvas.fill(self.bg_color)
        self.canvas.blit(imagen, (self.IMG_X, self.IMG_Y))
        self.dibujar_hud(player)
        self.dibujar_texto(texto, scroll_y)
        self.dibujar_divisor()

        botones = []
        if opciones:
            mouse_pos = self._mouse_logico()
            y = self.BTN_Y
            for i, opcion in enumerate(opciones):
                txt = f"{i+1}. {opcion}"
                render_normal = self.font_btn.render(txt, True, self.btn_color)
                rect = render_normal.get_rect(topleft=(self.BTN_X, y))
                if rect.collidepoint(mouse_pos):
                    render_final = self.font_btn.render(txt, True, self.btn_hover)
                else:
                    render_final = render_normal
                self.canvas.blit(render_final, rect)
                botones.append((rect, str(i+1)))
                y += self.BTN_H

        self._blit_canvas()
        return botones

    # ─────────────────────────────────────────
    # FADE IN
    # ─────────────────────────────────────────
    def fade_in(self, imagen, texto, player=None):
        temp = imagen.copy()
        for alpha in range(0, 255, 15):
            self.canvas.fill(self.bg_color)
            temp.set_alpha(alpha)
            self.canvas.blit(temp, (self.IMG_X, self.IMG_Y))
            self.dibujar_hud(player)
            self.dibujar_texto(texto)
            self.dibujar_divisor()
            self._blit_canvas()
            pygame.time.delay(20)

    # ─────────────────────────────────────────
    # FADE OUT — oscurece toda la pantalla antes de salir
    # ─────────────────────────────────────────
    def fade_out(self):
        overlay = pygame.Surface((self.width, self.height))
        overlay.fill((0, 0, 0))
        for alpha in range(0, 256, 18):
            overlay.set_alpha(alpha)
            self.canvas.blit(overlay, (0, 0))
            self._blit_canvas()
            pygame.time.delay(18)

    # ─────────────────────────────────────────
    # CARTEL PSIQUE
    # Overlay centrado que aparece ~2s y se desvanece.
    # Se llama desde game_engine tras modificar_psique con impacto.
    # ─────────────────────────────────────────
    def mostrar_cartel_psique(self):
        font_cartel = pygame.font.Font("fonts/Goth.ttf", 20)

        ancho_cartel = 400
        alto_cartel  = 82
        cx = (self.width  - ancho_cartel) // 2
        cy = (self.height - alto_cartel)  // 2

        overlay = pygame.Surface((ancho_cartel, alto_cartel))
        overlay.set_alpha(215)
        overlay.fill((12, 8, 4))

        borde_color = (110, 75, 20)

        clock = pygame.time.Clock()
        for frame in range(130):
            clock.tick(60)

            # Fade in / estable / fade out
            if frame < 20:
                alpha_txt = int(255 * frame / 20)
            elif frame > 110:
                alpha_txt = int(255 * (130 - frame) / 20)
            else:
                alpha_txt = 255

            self.canvas.blit(overlay, (cx, cy))
            pygame.draw.rect(self.canvas, borde_color,
                             (cx, cy, ancho_cartel, alto_cartel), 1)

            l1 = font_cartel.render("Esto tendrá repercusión", True, (190, 150, 40))
            l2 = font_cartel.render("en tu futuro.", True, (190, 150, 40))
            l1.set_alpha(alpha_txt)
            l2.set_alpha(alpha_txt)

            self.canvas.blit(l1, (cx + (ancho_cartel - l1.get_width()) // 2, cy + 12))
            self.canvas.blit(l2, (cx + (ancho_cartel - l2.get_width()) // 2, cy + 46))

            self._blit_canvas()

            # Cualquier tecla lo cierra antes
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    return

    # ─────────────────────────────────────────
    # INPUT DEL USUARIO
    # ESC → lanza EscapeAlMenu
    # Fade out antes de cada return
    # ─────────────────────────────────────────
    def esperar_input(self, imagen, texto, opciones=True, opciones_lista=None, player=None):
        clock = pygame.time.Clock()
        scroll_y = 0

        self.fade_in(imagen, texto, player)

        while True:
            clock.tick(60)

            if not pygame.mixer.music.get_busy():
                self.reproducir_musica()

            botones = self.render(imagen, texto, scroll_y, opciones_lista, player)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode(
                        (event.w, event.h), pygame.RESIZABLE
                    )

                if event.type == pygame.KEYDOWN:

                    # ESC → menú principal
                    if event.key == pygame.K_ESCAPE:
                        self.fade_out()
                        raise EscapeAlMenu()

                    # Scroll
                    if event.key == pygame.K_DOWN:
                        scroll_y -= self.LINE_H
                    if event.key == pygame.K_UP:
                        scroll_y += self.LINE_H
                    if scroll_y > 0:
                        scroll_y = 0

                    # Sin opciones → SPACE
                    if not opciones:
                        if event.key == pygame.K_SPACE:
                            self.fade_out()
                            return "continuar"
                    else:
                        if event.key == pygame.K_1:
                            self.fade_out()
                            return "1"
                        if event.key == pygame.K_2:
                            self.fade_out()
                            return "2"
                        if event.key == pygame.K_3:
                            self.fade_out()
                            return "3"

                # Click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if opciones_lista:
                        mouse_pos = self._mouse_logico()
                        for rect, valor in botones:
                            if rect.collidepoint(mouse_pos):
                                self.fade_out()
                                return valor

    # ─────────────────────────────────────────
    # INPUT DE NOMBRE
    # Sonido de tecla al escribir
    # ESC → EscapeAlMenu / fade out al confirmar
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

            texto = f"""
Has elegido la senda del {clase}.


Antes de descender...
¿Cómo te llaman?


"""
            self.canvas.fill(self.bg_color)
            self.canvas.blit(imagen, (self.IMG_X, self.IMG_Y))
            self.dibujar_texto(texto)
            self.dibujar_divisor()

            cursor = "|" if cursor_visible else " "
            linea_nombre = f"> {nombre}{cursor}"
            render_nombre = self.font_btn.render(linea_nombre, True, self.btn_hover)
            self.canvas.blit(render_nombre, (self.BTN_X, self.BTN_Y))

            instruccion = self.font.render("[ ENTER para confirmar ]", True, (60, 100, 45))
            self.canvas.blit(instruccion, (self.BTN_X, self.BTN_Y + 50))

            self._blit_canvas()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode(
                        (event.w, event.h), pygame.RESIZABLE
                    )

                if event.type == pygame.KEYDOWN:

                    # ESC → menú principal
                    if event.key == pygame.K_ESCAPE:
                        self.fade_out()
                        raise EscapeAlMenu()

                    elif event.key == pygame.K_RETURN:
                        self.fade_out()
                        return nombre.strip() if nombre.strip() else "Errante"

                    elif event.key == pygame.K_BACKSPACE:
                        if nombre:
                            nombre = nombre[:-1]
                            if self.sonidos_tecla:
                                random.choice(self.sonidos_tecla).play()

                    elif len(nombre) < 20 and event.unicode.isprintable():
                        nombre += event.unicode
                        if self.sonidos_tecla:
                            random.choice(self.sonidos_tecla).play()

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
        pygame.mixer.music.load(os.path.join(carpeta, cancion))
        pygame.mixer.music.play()

    # ─────────────────────────────────────────
    # dibujar_opciones — mantenido por compatibilidad
    # ─────────────────────────────────────────
    def dibujar_opciones(self, opciones):
        botones = []
        y = self.BTN_Y
        for i, opcion in enumerate(opciones):
            texto = f"{i+1}. {opcion}"
            render = self.font.render(texto, True, (255, 255, 255))
            rect = render.get_rect(topleft=(self.BTN_X, y))
            self.canvas.blit(render, rect)
            botones.append((rect, str(i+1)))
            y += self.BTN_H
        return botones
