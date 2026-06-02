# Referencia de UI — Descenso al Umbral (Godot)

## Archivos

### `LA ELEGIDA.png`
El marco visual definitivo para todas las pantallas de juego.
Frame dorado/bronce con calaveras en esquinas, pentáculo arriba al centro,
divisor horizontal en el panel derecho.

**Uso en Godot:** `TextureRect` en `CanvasLayer` superior de `GameScreen.tscn`.

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
