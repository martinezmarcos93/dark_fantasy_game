# Roadmap de Migración — Descenso al Umbral → Godot
*Branch: gdot — Especulativo*

---

## Por qué migrar

| Pygame (actual) | Godot (objetivo) |
|---|---|
| Filtro de psique = tinte plano calculado a mano | Shader: aberración cromática, vignette, distorsión |
| Fade básico entre pantallas | Dissolve, wipe, shader custom por nivel |
| Texto distorsionado = caracteres reemplazados | ShaderMaterial sobre RichTextLabel |
| Partículas: no existen | GPUParticles2D — polvo, vapor, chispas |
| Música: crossfade no existe | AudioStreamPlayer con fade real entre pistas |
| Distribución: requiere Python instalado | Exporta a .exe / .app / .web sin dependencias |

---

## Layout de UI confirmado

El diseño objetivo es un **split-screen con marco ornamental**:

```
┌─────────────────────────────────────────────────────┐
│  ┌─────────────┐  ┌─────────────────────────────┐   │
│  │             │  │  Título / Texto narrativo    │   │
│  │  IMAGEN     │  │                              │   │
│  │  DEL NIVEL  │  │  (área de scroll)            │   │
│  │             │  ├─────────────────────────────┤   │
│  │             │  │  1. Opción A                 │   │
│  ├─────────────┤  │  2. Opción B                 │   │
│  │ Clase — HP  │  │  3. Opción C                 │   │
│  │ ██████░░ MA │  └─────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
         MARCO ORNAMENTAL (ui_frame.svg / LA ELEGIDA)
```

- **Panel izquierdo (~35%)**: imagen de nivel/enemigo/cofre/NPC
- **Panel derecho superior (~60%, ~65% alto)**: texto narrativo con scroll
- **Panel derecho inferior (~60%, ~35% alto)**: opciones numeradas como botones
- **Strip inferior izquierdo**: nombre, clase, barras HP y energía
- **Marco**: overlay ornamental que envuelve todo — `LA ELEGIDA.png`

---

## Fase 0 — Proyecto Godot + estructura
*~2 horas, sin lógica todavía*

```
descenso_godot/
├── project.godot
├── autoloads/
│   ├── GameEngine.gd          # Director global (Autoload)
│   ├── SaveSystem.gd          # 3 slots + NG+
│   └── AudioManager.gd        # música por nivel con crossfade
├── scenes/
│   ├── Main.tscn              # escena raíz
│   ├── Menu.tscn
│   ├── Intro.tscn
│   ├── GameScreen.tscn        # la pantalla de juego (layout de arriba)
│   └── Combat.tscn            # igual a GameScreen pero con estado de combate
├── scripts/
│   ├── Player.gd              # Resource — datos del jugador
│   ├── Enemy.gd               # Resource — configuración de enemigo
│   ├── CombatState.gd         # lógica de combate
│   └── levels/                # Level1.gd ... Level10.gd
├── resources/
│   └── enemies/               # .tres por cada enemigo
├── shaders/
│   ├── psique_overlay.gdshader  # tinte + aberración por psique
│   └── text_distort.gdshader    # distorsión de texto en niveles profundos
├── assets/                    # mismas 35 imágenes, sin cambios
└── music/                     # mismos 14 mp3, sin cambios
```

---

## Fase 1 — Portar lógica de datos
*~1 día — traducción casi mecánica de Python a GDScript*

GDScript es Python con tipado opcional. La traducción es directa:

| Python | GDScript |
|---|---|
| `class Player:` | `class_name Player extends Resource` |
| `self.psique = {}` | `var psique: Dictionary = {}` |
| `def modificar_psique(self, cambios):` | `func modificar_psique(cambios: Dictionary):` |
| `json.dump(data, f)` | `FileAccess.open(...); file.store_string(JSON.stringify(data))` |
| `random.randint(1, 6)` | `randi_range(1, 6)` |

**Archivos a portar:** `player.py` → `Player.gd`, `save_system.py` → `SaveSystem.gd`,
`combat_system.py` → `CombatState.gd`, `enemies.py` → Resources `.tres`

---

## Fase 2 — GameScreen (el corazón de la UI)
*~2 días — el reemplazo de ui.py*

```
GameScreen.tscn
├── CanvasLayer (marco, siempre encima)
│   └── TextureRect (LA ELEGIDA.png, stretch=KEEP_ASPECT_COVERED)
├── MarginContainer (respeta los bordes del marco)
│   ├── HSplitContainer
│   │   ├── Panel izquierdo
│   │   │   ├── TextureRect (imagen del nivel) ← cambia con cada pantalla
│   │   │   └── HBoxContainer (HUD)
│   │   │       ├── Label (nombre — clase)
│   │   │       ├── ProgressBar (HP, color rojo)
│   │   │       └── ProgressBar (energía, color azul/verde/amarillo)
│   │   └── VSplitContainer (panel derecho)
│   │       ├── RichTextLabel (texto narrativo, scroll automático)
│   │       │   └── efecto typewriter vía Timer
│   │       └── VBoxContainer (opciones)
│   │           └── Button × N (generados dinámicamente)
└── ColorRect (overlay de psique, con shader)
```

**Shader de psique** — reemplaza las ~60 líneas de cálculo manual de Pygame:
```glsl
uniform vec4 psique_color : hint_color = vec4(0.0);
uniform float intensidad : hint_range(0.0, 1.0) = 0.0;
void fragment() {
    vec4 base = texture(TEXTURE, UV);
    COLOR = mix(base, base * psique_color, intensidad);
}
```

---

## Fase 3 — Sistema de combate
*~1 día — equivalente al actual con animaciones*

`CombatState.gd` porta `combat_system.py` completo. Mejoras posibles:
- `Tween` para animar barras de HP al recibir daño
- `AudioStreamPlayer` con `pitch_scale` dinámico para tensión en rondas finales
- Flash de daño: `ColorRect` rojo sobre la imagen, `Tween` opacity 0→1→0

---

## Fase 4 — Los 10 niveles
*~2-3 días — repetitivo pero mecánico*

Cada `LevelN.gd` extiende `BaseLevel.gd` y sobreescribe:
```gdscript
class_name Level3 extends BaseLevel

func fase_laberinto():
    # mismo contenido que level3.py
    pass

func fase_combate():
    var enemy = EnemySacerdote.new()
    return await engine.combate_narrativo(enemy)

func fase_psicologica():
    pass
```

---

## Fase 5 — Mejoras visuales exclusivas de Godot
*~1-2 días — lo que justifica la migración*

| Feature | Implementación |
|---|---|
| Transición entre niveles | `SceneTree.change_scene_to_file()` con `TransitionLayer` |
| Texto distorsionado | `RichTextEffect` custom + shader en label |
| Partículas de polvo en cuevas | `GPUParticles2D` en fondo del panel izquierdo |
| Música con crossfade real | Dos `AudioStreamPlayer`, Tween volume entre ellos |
| Vignette según psique | Shader en CanvasLayer, intensidad = max(psique) / 100 |

---

## Fase 6 — Elementos 3D selectivos (opcional)
*Sin Blender — Python + trimesh genera .glb, Godot los importa*

Para objetos icónicos, no personajes:

| Objeto | Complejidad | Uso |
|---|---|---|
| Cofre del Umbral (rotando) | Baja | Pantalla de apertura de cofre |
| Llave de Piedra | Baja | Pantalla al recogerla |
| El Espejo Final | Media | Level 10 — shader de reflejo con mundo paralelo |
| Columnas de cueva | Baja | Ambientación de fondo en panel izquierdo |

Workflow sin Blender:
```
Python script (trimesh) → .glb → importar en Godot → Node3D en SubViewport → TextureRect
```

---

## Estimación de tiempo total

| Fase | Tiempo | Estado |
|---|---|---|
| 0 — Estructura Godot | 2h | Pendiente |
| 1 — Lógica de datos | 1 día | Pendiente |
| 2 — GameScreen UI | 2 días | Pendiente |
| 3 — Combate | 1 día | Pendiente |
| 4 — 10 niveles | 3 días | Pendiente |
| 5 — Mejoras visuales | 2 días | Pendiente |
| 6 — Elementos 3D | Variable | Opcional |
| **Total mínimo** | **~9 días** | |

---

## Assets existentes — compatibilidad

| Asset | Formato | Compatible con Godot |
|---|---|---|
| 35 imágenes de juego | .jpg / .png | ✅ Importa directamente |
| ui_frame.svg | .svg | ✅ Godot renderiza SVG nativamente |
| LA ELEGIDA.png | .png | ✅ |
| 14 pistas de música | .mp3 | ✅ |
| Fuentes góticas | .ttf | ✅ |

**Ningún asset visual o de audio necesita ser regenerado.**

---

## Marco elegido

`LA ELEGIDA.png` — frame dorado/bronce con calaveras y pentáculo.
Mockup de referencia con contenido: `fb381c2c-144b-4b6c-8a4e-f134fc5d54c0.png`

Hay 3 frames alternativos descartados (estilo nórdico/steampunk, "Rama: yota").
