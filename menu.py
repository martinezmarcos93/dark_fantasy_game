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
        mapa[str(i)] = "creditos"
        i += 1
        mapa[str(i)] = "salir"

        return mapa.get(eleccion, "salir")

    # ─────────────────────────────────────────
    # PANTALLA DE CRÉDITOS
    # ─────────────────────────────────────────
    def mostrar_creditos(self):
        imagen = self.ui.cargar_imagen("assets/menu.jpg")

        texto = """
Descenso al Umbral


Desarrollo y diseño:
Marcos Martínez


Inspirado en:
Dark Souls · Elden Ring
Psicología Junguiana
Filosofía esotérica


"El dungeon no es un lugar.
Es una proyección."


[ESPACIO para volver]
"""
        self.ui.esperar_input(imagen, texto, opciones=False)
