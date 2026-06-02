# blender/ — Scripts de generación procedural

Scripts de Python para Blender que generan assets para la versión Godot del juego.
No requieren Blender abierto — pueden ejecutarse en modo headless.

## Requisitos

- Blender 3.x o 4.x instalado
- `blender` disponible en PATH (o usar ruta absoluta)

## Scripts

### `frame_generator.py` — Marco de la interfaz

Genera `godot/assets/images/ui_frame.png` (1000×600 px, RGBA).

Resuelve los defectos de "LA ELEGIDA" (referencia en `docs/ui-reference/`):
- ✓ Canal alpha real en los paneles (no negro sólido)
- ✓ 4 calaveras simétricas y completas en las esquinas
- ✓ Divisor del panel derecho prominente (22px con relieve)
- ✓ HUD strip 90px — suficiente para nombre + clase + barras
- ✓ Resolución exacta 1000×600

**Ejecutar:**
```bash
# Modo headless (sin abrir Blender)
blender --background --python blender/frame_generator.py

# Modo interactivo (abre Blender, útil para ajustes)
blender blender/frame_generator.py
```

**Ajustar parámetros:**
Todos los valores editables están en la sección `# CONFIG` al inicio del script.
Bajar `RENDER_SAMPLES = 32` para iteraciones rápidas (calidad baja).
Subir a `256` o `512` para el render final.

**Salida:**
```
godot/assets/images/ui_frame.png
```

## Layout del frame generado

```
┌────────────────────────────────────────────────────────────┐
│  BORDE TOP (42px)                    [calavera TL] [cál TR]│
│  ┌──────────────┬──────┬────────────────────────────────┐  │
│  │              │ [P]  │  Texto narrativo               │  │
│  │  Panel       │[COL] │  (scroll)                      │  │
│  │  Imagen      │      │                                │  │
│  │  (280px ancho│      │                                │  │
│  │              │      │══════════════════════════════  │  │
│  │              │      │  Opciones / Botones            │  │
│  ├──────────────┤      │                                │  │
│  │  HUD strip   │      │                                │  │
│  │  (90px alto) │      │                                │  │
│  └──────────────┴──────┴────────────────────────────────┘  │
│  BORDE BOT (42px)   [cálav BL]  [cálav CB]  [cálav BR]     │
└────────────────────────────────────────────────────────────┘
[P] = Pentáculo con anillo ornamental
[COL] = Columna central (68px)
══ = Divisor prominente (22px, relieve Z_FRAME + Z_DIVIDER)
```

## Workflow de iteración

1. Ejecutar con `RENDER_SAMPLES = 32` para ver el resultado rápido
2. Ajustar parámetros en CONFIG (posiciones, proporciones, colores)
3. Re-ejecutar hasta estar conforme
4. Render final con `RENDER_SAMPLES = 256`
5. Copiar al proyecto Godot (el script ya apunta a `godot/assets/images/`)
6. En Godot: refrescar el import del archivo
