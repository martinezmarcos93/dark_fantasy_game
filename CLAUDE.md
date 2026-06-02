# descenso-al-umbral — guía para asistentes de IA

Este archivo lo lee Claude Code (y cualquier asistente) al iniciar.
Mantenerlo corto y de alta señal. Es la principal defensa para que la
migración desde Pygame no rompa la lógica existente ni use APIs incorrectas.

---

## Qué es el proyecto

**Descenso al Umbral** — aventura narrativa psicológica, texto + imágenes,
10 niveles, sistema de psique oculto (5 variables 0–100), combate por turnos
(2d6 + stat vs dificultad×2), 15 endings, 35 assets visuales, 14 pistas de
música.

Rama **`main`**: versión jugable en Python/Pygame — **no tocar**.
Rama **`gdot`**: migración activa a Godot 4. Todo el trabajo nuevo va acá.

La lógica de negocio vive en `game/`. La UI (`ui.py`, `game_engine.py`)
se descarta y se rehace en Godot. Ver `docs/roadmap-godot.md`.

---

## ⚠️ Reglas que no se negocian

### Godot
- **Versión: 4.6.x** (estable actual: 4.6.3). Verificar toda API contra
  [docs.godotengine.org/en/stable](https://docs.godotengine.org/en/stable/)
  antes de usarla. **Nunca APIs de Godot 3.**
- **Lenguaje: GDScript.** No C#. Python → GDScript es casi 1:1. Decisión
  documentada en `docs/decisiones.md` (ADR-001).
- **Input por acciones del Input Map** (`interactuar`, `opcion_1`…), nunca
  teclas físicas hardcodeadas.
- `godot-mcp` está **descartado** (CVE-2026-25546). No proponerlo.

### El juego original es la referencia
- La lógica de psique, combate, finales y niveles debe comportarse
  **idénticamente** a la versión Python. Portá, no reinventés.
- Los **textos narrativos son sagrados.** No parafrasear, no "mejorar",
  no resumir. Si `enemies.py` dice "La piedra no entiende de hechizos",
  eso debe aparecer exactamente igual en Godot.
- Los **96 tests de `test_game.py`** son el contrato de comportamiento.
  Cualquier cambio en lógica debe pasar por esa referencia.
- Los **35 assets** (imágenes y música) se reutilizan sin modificar.

### UI
- El marco visual es **`docs/ui-reference/LA ELEGIDA.png`**.
  El layout de referencia es **`docs/ui-reference/mockup-ui-poblado.png`**.
- Panel izquierdo (~35%): imagen del nivel/enemigo/NPC.
- Panel derecho superior: texto narrativo con scroll.
- Panel derecho inferior: opciones numeradas como botones.
- Strip inferior izquierdo: nombre, clase, barras HP/energía/Aliento.
- El filtro de psique (tinte de color actual) se reemplaza por un **shader**
  de Godot. Comportamiento visual equivalente o superior, nunca más simple.

### 3D (si aplica)
- 3D solo para objetos icónicos: cofres, llave, espejo final.
- Sin Blender: usar Python + `trimesh` para generar `.glb`.
- Los objetos 3D van en `SubViewport` → `TextureRect`, sobre el fondo 2D.
- No cambiar el plano principal del juego a 3D sin consultar.

---

## Convenciones

- `snake_case` para archivos, carpetas y variables. `PascalCase` para
  nombres de nodos y clases.
- Escenas autocontenidas. Pasar referencias desde arriba con `@export`,
  nunca buscar nodos con `get_node()` desde adentro.
- Señales en pasado: `nivel_cargado`, `combate_iniciado`, `opcion_elegida`.
- Assets en `assets/images/` y `assets/music/` — misma estructura, sin
  subcarpetas por nivel.
- Cada `LevelN.py` de Python = una escena `LevelN.tscn` que extiende
  `scenes/Level.tscn` (escena base).

---

## Verificar cambios (headless)

```bash
# Importar y registrar scripts nuevos
godot --headless --path . --import

# Correr escena principal
godot --headless --path . --quit-after 5

# Si un class_name nuevo no se reconoce: correr --import primero
```

---

## No romper lo que funciona

- Antes de modificar cualquier función portada, confirmar el comportamiento
  esperado leyendo el Python original.
- El "contrato" del juego es la versión Pygame: si algo se siente diferente
  (timing de diálogos, flujo de niveles), es una regresión.
- Al terminar un cambio: listar qué se tocó y qué se verificó.

---

## Cómo trabajar

- **Prototipo incremental**: Fase 0 → 1 → 2 → … según `docs/roadmap-godot.md`.
- **Git en `gdot`** — no mergear a `main` hasta que el juego esté funcional.
- Las escenas `.tscn` conflictúan fácil en merges — coordinar quién toca cuál.
- Decisiones técnicas → registrar en `docs/decisiones.md` (formato ADR).
- El usuario conoce bien el juego original pero es principiante en Godot.
  **Explicar el porqué de cada decisión de Godot**, no solo el qué.
- **Idioma: español.**

---

## Punteros rápidos

| Necesito… | Voy a… |
|---|---|
| Entender el juego original | `README.md` |
| Ver el roadmap de migración | `docs/roadmap-godot.md` |
| Ver el layout de UI objetivo | `docs/ui-reference/mockup-ui-poblado.png` |
| Ver el marco visual elegido | `docs/ui-reference/LA ELEGIDA.png` |
| Ver decisiones tomadas | `docs/decisiones.md` |
| Ver todas las mecánicas | `docs/roadmap-mecanicas.md` |
| Tests de comportamiento | `test_game.py` (96 tests, referencia de lógica) |
