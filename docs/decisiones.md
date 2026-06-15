# Decisiones de Arquitectura — Descenso al Umbral (Godot)

Registro de decisiones técnicas en formato ADR ligero.
Cada decisión tiene contexto, la elección tomada y sus consecuencias.

---

## ADR-001: Lenguaje — GDScript, no C#

**Fecha:** 2026-06-02
**Estado:** Aceptado

**Contexto:**
El juego original está en Python. Al migrar a Godot se puede elegir GDScript o C#.

**Decisión:** GDScript.

**Motivos:**
1. La sintaxis de GDScript es casi idéntica a Python — la traducción de `player.py`, `combat_system.py`, etc. es casi línea por línea, minimizando bugs de lógica en la migración.
2. Para un juego narrativo 2D con combate por turnos, el rendimiento de GDScript es más que suficiente. C# no aporta nada relevante.
3. Los asistentes de IA generan ejemplos más confiables de GDScript moderno (Godot 4) que de C# con las APIs de Godot 4.
4. El desarrollador es principiante en Godot — GDScript tiene mejor integración con el editor y más tutoriales disponibles.

**Consecuencias:**
- Todo el código nuevo será GDScript.
- `ui.py` y `game_engine.py` se reescriben desde cero en GDScript (no se traducen, se reimplementan).
- `player.py`, `combat_system.py`, `enemies.py`, `save_system.py` se traducen casi 1:1.

---

## ADR-002: Aproximación visual — 2D base, 3D opcional y acotado

**Fecha:** 2026-06-02
**Estado:** Aceptado

**Contexto:**
El juego actual usa ilustraciones 2D estáticas (35 imágenes `.jpg`). Se planteó si migrar a 3D completo.

**Decisión:** Base 2D, con elementos 3D opcionales solo para objetos icónicos.

**Motivos:**
1. Las ilustraciones actuales tienen identidad visual fuerte (estilo vermis/manuscrito). Ir a 3D cambiaría el tono radicalmente.
2. El juego es narrativo — el texto y la imagen estática son el medio, no la acción.
3. Objetos 3D (cofre del Umbral rotando, llave de piedra, espejo) se pueden insertar como `SubViewport` → `TextureRect` sin tocar la lógica 2D.
4. Sin Blender: los `.glb` se generan con Python + `trimesh`, sin necesidad de instalar Blender.

**Consecuencias:**
- La escena base usa `TextureRect` para la imagen de nivel (mismo `.jpg`).
- 3D solo para Fase 6 del roadmap, opcional y acotado a objetos icónicos.
- Todos los assets actuales se reutilizan sin modificar.

---

## ADR-003: Assets existentes se reutilizan intactos

**Fecha:** 2026-06-02
**Estado:** Aceptado

**Contexto:**
35 imágenes `.jpg/.png`, 14 pistas `.mp3`, 3 fuentes `.ttf` ya existen y son parte de la identidad visual del juego.

**Decisión:** Reutilizar todos los assets sin modificaciones. No regenerar ni "mejorar" con IA.

**Motivos:**
1. Las imágenes tienen coherencia estilística (estilo vermis). Cualquier imagen nueva debe seguir los mismos prompts y parámetros.
2. La música ya está nombrada correctamente (`nivel_N.mp3`, `boss.mp3`, etc.) y el sistema de reproducción por nivel ya funciona.
3. Regenerar sería tiempo perdido — el objetivo de esta fase es la migración, no la producción de nuevos assets.

**Consecuencias:**
- `assets/` se copia al proyecto Godot sin cambios.
- Godot importa `.jpg` nativamente — no se necesita conversión.
- Si se agrega un asset nuevo, debe seguir el estilo vermis documentado en `docs/roadmap-mecanicas.md` y `docs/assets-pendientes.md`.

---

## ADR-004: UI frame — regenerado en Blender (supera a "LA ELEGIDA")

**Fecha:** 2026-06-02
**Estado:** Aceptado

**Contexto:**
Se exploraron varios frames ornamentales (dorado/bronce, nórdico, steampunk).
Se eligió el concepto de "LA ELEGIDA" (dorado/bronce con calaveras y pentáculo),
pero su archivo AI tiene defectos técnicos que impiden usarlo en Godot.

**Decisión:** Conservar el *concepto* de LA ELEGIDA pero **regenerar el frame
proceduralmente en Blender** (`blender/frame_generator.py`), produciendo
`godot/assets/images/ui_frame.png` (1000×600, RGBA).

**Motivos (7 defectos de LA ELEGIDA que el script resuelve):**
1. Paneles en negro sólido sin alpha → bloqueante en Godot. Fix: `film_transparent`.
2. Calavera inferior derecha cortada por el canvas AI. Fix: geometría procedural.
3. Calavera inferior izquierda ausente (asimetría). Fix: 5 calaveras por código.
4. Divisor del panel derecho de 2px, invisible. Fix: 22px con relieve elevado.
5. HUD strip de ~50px, insuficiente. Fix: 90px.
6. Resolución ~640px escalada. Fix: render nativo 1000×600.
7. Opciones duplicadas en el mockup por falta de jerarquía. Fix: divisor claro.

**Consecuencias:**
- `ui_frame.png` va como `TextureRect` en el `CanvasLayer` superior de `GameScreen.tscn`.
- El layout (panel imagen izq, texto+opciones der, HUD inferior) lo fija el script,
  con todas las proporciones en la sección CONFIG (editable y reproducible).
- LA ELEGIDA queda como referencia de diseño en `docs/ui-reference/`, no se usa.
- Para ajustar el frame: editar CONFIG y re-ejecutar el script (no editar el PNG).

---

## ADR-005: Estructura de escenas — una por nivel, heredando de base

**Fecha:** 2026-06-02
**Estado:** ~~Aceptado~~ **Superado por ADR-007 (2026-06-14)**

**Contexto:**
Los 10 niveles de Python tienen una estructura uniforme: `fase_laberinto()`, `fase_combate()`, `fase_psicologica()`. Se necesita una equivalencia en Godot.

**Decisión:** Una escena base `scenes/Level.tscn` + `scripts/levels/BaseLevel.gd`. Cada nivel hereda: `Level1.tscn` extiende `Level.tscn`, `scripts/levels/Level1.gd` extiende `BaseLevel.gd`.

**Motivos:**
1. Sigue exactamente la estructura actual — cada `LevelN.py` se convierte en `LevelN.gd` que sobreescribe los tres métodos de la clase base.
2. Evita duplicación de la lógica de UI, transiciones y guardado entre niveles.
3. Permite agregar mecánicas comunes (cofres, aliento) en la clase base sin tocar cada nivel individual.

**Consecuencias:**
- `GameEngine.gd` (Autoload) instancia la escena del nivel actual y llama sus métodos.
- El cambio de nivel es `get_tree().change_scene_to_file("res://scenes/levels/Level2.tscn")`.
- Los laberintos (Level 3, 7, 9) añaden un método `fase_laberinto()` que la base deja vacío por defecto.

---

## ADR-006: godot-mcp descartado por seguridad

**Fecha:** 2026-06-02
**Estado:** Aceptado

**Contexto:**
Existe un plugin MCP para integrar Godot con asistentes de IA directamente. Un proyecto paralelo (tango-uego de Facu Nuevo) advirtió sobre él.

**Decisión:** No instalar ni usar `godot-mcp`.

**Motivos:**
1. CVE-2026-25546 — vulnerabilidad confirmada en la herramienta.
2. El flujo actual (Claude Code en terminal + Godot headless para verificar) es suficiente y seguro.

**Consecuencias:**
- Ninguna extensión de IA se instala en el editor de Godot.
- El workflow es: Claude escribe código → se pega en el editor → se verifica headless o en el editor manualmente.

---

## ADR-007: Niveles como scripts que conducen una GameScreen única (supera ADR-005)

**Fecha:** 2026-06-14
**Estado:** Aceptado

**Contexto:**
ADR-005 planeaba una escena `.tscn` por nivel heredando de `Level.tscn`. Al portar
la Fase 3 (combate) quedó claro que la `GameScreen` es una UI persistente que se
*conduce* con llamadas `async` (`await mostrar_pantalla(...)`), igual que ya lo hace
`CombatSystem.combate_completo`. Revisando `levelN.py`, los niveles son **lógica
narrativa pura**: no aportan ningún nodo visual propio — todos usan la misma pantalla.

**Decisión:** Cada nivel es un **script** (`scripts/levels/base_level.gd` +
`level1.gd`…`level10.gd`), no una escena. `GameEngine` (Autoload) es el director:
mantiene la `GameScreen` y recorre los niveles llamando `await nivel.jugar(player, engine)`.

**Motivos:**
1. Una `.tscn` por nivel serían 11 escenas casi vacías envolviendo un script — complejidad sin beneficio.
2. Las `.tscn` conflictúan feo en merges; los `.gd` son texto plano, fáciles de revisar y mergear.
3. La `GameScreen` ya es una sola Un­idad conducida por `async`; cambiar de escena por nivel rompería ese flujo y el `await` del combate.
4. Mapea 1:1 con el Python: cada `LevelN.py` → `LevelN.gd` que sobreescribe `fase_combate`/`fase_psicologica`/`fase_laberinto`.

**Consecuencias:**
- No se crean `scenes/levels/*.tscn`. La carpeta `scenes/levels/` queda sin uso.
- `base_level.gd` define `jugar()` (combate → psicológica) y deja `fase_laberinto()` vacío por defecto (lo usan los niveles 3, 7, 9).
- `GameEngine` gana `mostrar_nivel()`, `combate_narrativo()` y los cofres, conduciendo la `GameScreen`.
- `mostrar_nivel()` devuelve el índice 0-based de la opción (la versión Python devolvía el string "1".."N"); los ports de nivel comparan por índice.
