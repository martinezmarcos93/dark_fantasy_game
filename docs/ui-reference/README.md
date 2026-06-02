# Referencia de UI — Descenso al Umbral (Godot)

## El marco real del juego

**`godot/assets/images/ui_frame.png`** — generado por
`blender/frame_generator.py`. Este es el marco que usa el juego.

Reemplaza a LA ELEGIDA, resolviendo sus 7 defectos:
canal alpha real, 5 calaveras simétricas sin clipping, divisor prominente,
HUD strip con altura suficiente, resolución exacta 1000×600.

Para regenerarlo o ajustarlo, editar la sección CONFIG del script y correr:
```bash
blender --background --python blender/frame_generator.py
```

## Archivos de referencia (diseño, NO se usan en el juego)

### `LA ELEGIDA.png`
Boceto AI original que definió el *concepto* del marco: dorado/bronce,
calaveras en esquinas, pentáculo en la columna, dos paneles + divisor.
Tiene defectos técnicos que impiden usarlo directamente (negro sólido
sin alpha, calaveras cortadas, baja resolución). Sirvió de guía para
`frame_generator.py`. Ver ADR-004 en `docs/decisiones.md`.

### `mockup-ui-poblado.png`
Mockup de cómo se ve el juego funcionando dentro del marco.
Muestra imagen de nivel a la izquierda, texto narrativo arriba a la derecha,
opciones numeradas abajo a la derecha, HUD con HP/MA abajo a la izquierda.

**Uso:** Referencia de layout durante la implementación de `GameScreen.tscn`.

---

## Layout del panel de juego

```
┌─────────────────────────────────────────────────────┐
│  MARCO ORNAMENTAL (LA ELEGIDA.png)                  │
│  ┌──────────────┐  ┌────────────────────────────┐   │
│  │              │  │  Título del nivel / enemigo │   │
│  │  TextureRect │  │  ─────────────────────────  │   │
│  │  (imagen     │  │  Texto narrativo            │   │
│  │   del nivel) │  │  con scroll                 │   │
│  │              │  │  (RichTextLabel)             │   │
│  │  ~35% ancho  │  ├────────────────────────────┤   │
│  │              │  │  1. Opción A               │   │
│  ├──────────────┤  │  2. Opción B               │   │
│  │ Clase  HP ██ │  │  3. Opción C               │   │
│  │ Nombre EN ░░ │  │  (VBoxContainer + Button)  │   │
│  └──────────────┘  └────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

---

## Frames alternativos (descartados)

Los tres frames de estilo nórdico/steampunk ("Rama: yota") están en
`D:\01-Marcos\00-Programacion\XXX-Elementos dispersos\INTERFAZ del dark fantasy game\`
y **no se usan**. Fueron explorados y descartados. Ver ADR-004 en `docs/decisiones.md`.
