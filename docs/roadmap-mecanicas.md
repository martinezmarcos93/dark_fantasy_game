# Roadmap de Mecánicas — Descenso al Umbral

Documento de planificación. Todo lo que figura aquí es futuro — nada está implementado aún.

---

## Análisis de género y referencias

El juego cruza tres linajes que rara vez se mezclan:

**Narrative RPG psicológico**
- **Planescape: Torment** — stats ocultos, múltiples finales, narrativa antes que combate
- **Disco Elysium** — chequeos 2d6, stats que representan estados mentales, el mundo reacciona a lo interno
- **Cultist Simulator** — recursos ocultos, mecánicas que se descubren muriendo, endings por combinaciones

**Dungeon Crawler narrativo**
- **Sunless Sea** — progresión por zonas, encuentros aleatorios, la muerte como parte de la experiencia
- **Slay the Spire** — combate por rondas, pool de recursos limitados, builds por clase
- **FTL** — consecuencias diferidas, información escasa, tono hostil

**Soulsborne (atmósfera, no mecánica)**
- **Dark Souls / Elden Ring** — lore en los ítems, la muerte que deja algo, enemigos como fuerzas naturales
- **Bloodborne** — horror psicológico como mecánica central, la cordura como recurso

**Género:** Narrative Dungeon Crawler Psicológico / subgénero roguelite por runs acumulativas.

---

## Sistema base nuevo: Aliento del Umbral

Antes de ítems, cofres o aliados, el juego necesita **una moneda interna de intercambio**.
El **Aliento del Umbral** es un recurso que representa el peso de haber descendido con valentía.

```
Rango:     0–10 (no se pierde entre niveles, sí al morir)
Se gana:   Ganar 2/3 rondas de combate   (+1)
           Elegir la opción "peligrosa"   (+1)
           Explorar callejones sin salida (+1)
           Sobrevivir un nivel sin huir   (+1)
Se gasta:  Activar cofres del Umbral
           Convocar aliados
           Pagar memorias (ver sección "La Memoria como Moneda")
           Usar la acción "Descanso" entre combates
```

**Nota de implementación:** Agregar `aliento` a `Player.__init__()` y a `save_system.py`.

---

## Sistema de Ítems

Inventario limitado a **3 ítems**. El límite fuerza decisiones.
Cada ítem tiene un costo secundario (mecánico o narrativo) además de su efecto principal.

| Ítem | Efecto principal | Costo oculto |
|------|-----------------|--------------|
| **Antorcha** | −10 miedo al usarla en un nivel | +5 lucidez (la luz revela lo que preferirías no ver) |
| **Sal Consagrada** | −15 corrupción, 1 uso | +8 culpa (purgar tiene precio moral) |
| **Vendas Viejas** | +25 HP, 1 por run | Sin costo — pero solo 1 en toda la partida |
| **Fragmento de Espejo** | Revela psique dominante actual | +5 miedo (saber duele) |
| **Tinta del Abismo** | Hechicero: recarga 1 hechizo gastado | +10 corrupción |
| **Sangre Seca** | +15 HP, reutilizable | +5 culpa por cada uso |
| **Piedra de Eco** | Guerrero: siguiente Defender siempre exitoso | −10 stamina máximo de forma permanente |
| **Mapa Roto** | Revela si el siguiente nivel tiene enemigo secreto | Sin costo |
| **Elixir del Olvido** | Borra 1 entrada del historial | −10 lucidez |

**Fuentes de ítems:** cofres, recompensa por crítico en ronda final, compra a aliados.

**Nota de implementación:** Agregar `inventario: list[str]` a `Player`. Máximo 3 elementos.
Cada ítem es una cadena ID (`"antorcha"`, `"sal"`, etc.). Los efectos se aplican al usarlos.

---

## Cofres y Llaves

Tres tipos de cofre con condiciones de apertura distintas:

### Cofre de Piedra
- **Condición:** tener la `Llave de Piedra` (se encuentra en el nivel anterior, siempre visible)
- **Contenido:** 1 ítem del tier básico (Vendas, Antorcha, Sangre Seca)
- **Dónde:** Level 2, 4, 8

### Cofre de Eco
- **Condición:** ganar las 3 rondas del combate anterior (2/3 no alcanza)
- **Contenido:** 1 ítem del tier medio + fragmento de lore del enemigo
- **Sin llave** — recompensa de maestría táctica
- **Dónde:** Level 1, 3, 5, 7, 9

### Cofre del Umbral
- **Condición:** ≥ 5 Aliento del Umbral al llegar
- **Contenido:** ítem del tier alto (Tinta del Abismo, Piedra de Eco) + fragmento del ending actual
- **1 por run**, aparece en Level 6 o Level 8
- **Nota de narrativa:** el cofre "sabe" qué ending proyecta el jugador y el fragmento es coherente con él

---

## Laberintos y Callejones sin Salida

Tres niveles tienen una **fase de exploración** previa al combate: Level 3, Level 7, Level 9.

### Mecánica (texto puro)
```
"El corredor se divide ante vos."
  1. Izquierda (oscuro, sin sonido)
  2. Derecha (hay algo que brilla levemente)
  3. Volver atrás
```

**Callejones sin salida:**
- Algunos dan lore (`"Encontrás marcas en la pared. Alguien pasó antes."`)
- Algunos dan ítems pequeños o Aliento del Umbral (+1)
- Algunos modifican psique sin advertencia
- **Uno específico** (callejón del espejo roto en Level 7) contiene el enemigo secreto **El Otro**

**Regla de exploración:** cada callejón explorado suma +1 Aliento del Umbral.
La valentía de mirar donde no tenías que mirar tiene peso en el Umbral.

---

## Enemigos Secretos

Tres enemigos ocultos con condiciones de activación específicas:

### El Otro — psique en equilibrio
- **Condición:** todos los valores de psique dentro de un rango de 10 puntos entre sí al llegar a Level 5
- **Dónde:** reemplaza la transición entre Level 4 y Level 5
- **Mecánica especial:** sus ataques no modifican psique. Combate puro.
- **Reward:** +2 Aliento del Umbral + opción de "Fusionarte" con él → **ending secreto**
- **Dificultad:** 7, 3 rondas

### El Hambre — consecuencia de la violencia acumulada
- **Condición:** usar Furia Ciega (Guerrero) o Apuñalar (Ladrón) más de 4 veces en la run
- **Dónde:** aparece sin intro al inicio de Level 6 o Level 9
- **Sin pantalla de presentación** — aparece de golpe en el encabezado de combate
- **Reward si ganás:** +20 HP máximo permanente hasta el final del run
- **Dificultad:** 9, 3 rondas

### El Doble — exclusivo de New Game+
- **Condición:** solo en runs con psique heredada (ng_plus.json presente)
- **Dónde:** Level 4, reemplaza una transición
- **Mecánica:** usa los valores de psique heredados para escalar sus stats
- Sus textos de ataque citan elecciones del historial de la partida anterior
- **Reward:** ítem del tier alto + fragmento de lore del run anterior
- **Dificultad:** 7 + modificador heredado, 3 rondas

---

## Aliados

Dos aliados posibles, **mutuamente excluyentes** (solo uno por run):

### El Viajero Perdido — aliado de combate
- **Dónde encontrarlo:** callejón sin salida de Level 2, solo si Aliento ≥ 3
- **Qué hace:** en el próximo combate actúa como acción adicional gratuita en Ronda 1 (daño fijo medio)
- **Costo:** 3 Aliento del Umbral para "convencerlo de que venga"
- **Narrative:** no habla mucho. Solo dice que también está bajando.
- **Limitación:** desaparece después de 1 combate

### La Voz del Umbral — aliado de información
- **Dónde encontrarlo:** Level 5, solo si lucidez ≥ 30 al llegar
- **Qué hace:** revela tu ending actual proyectado y el stat que tendrías que cambiar para alterarlo
- **Costo:** +10 culpa (saber tu destino pesa)
- **Narrative:** es la voz que habla en los niveles, pero ahora responde
- **Limitación:** solo informa, no actúa

---

## Formas adicionales de curación y recuperación

### HP

| Método | HP | Condición |
|--------|----|-----------|
| Entre niveles (ya existe) | 3–8 HP | Automático, decreciente |
| Vendas (ítem) | +25 HP | Consumible (1 por run) |
| Sangre Seca (ítem) | +15 HP | +5 culpa por uso |
| Ganar 2/3 rondas | +5 HP | Bonus automático de victoria |
| Descanso activo | +10 HP | Gasta 2 Aliento del Umbral |
| El Hambre (vencerlo) | +20 HP máx | Solo si ganás |

### Energía (MP / ST / IN)

| Método | Energía | Condición |
|--------|---------|-----------|
| Huir (Ladrón, ya existe) | 10–20 IN | Recibe daño a cambio |
| Entre niveles (ya existe) | 6–15 | Automático |
| Tinta del Abismo (ítem) | Recarga 1 hechizo | Solo Hechicero, +10 corrupción |
| Acción "Respirar" (nueva) | +10 ST/IN | Ocupa una ronda (ronda neutral) |
| Ganar sin usar especiales | +5 energía bonus | Solo si ningún recurso se gastó |

---

## La Memoria como Moneda

El `historial` de decisiones (ya implementado en `Player`) puede usarse como recurso de pago.

**Mechanic:** algunos eventos ofrecen `"¿Pagás con un recuerdo?"`

El jugador puede **eliminar una entrada del historial** a cambio de:
- Curación (+20 HP)
- Un ítem
- Abrir el Cofre del Umbral sin Aliento
- Resistir un efecto de psique

**Consecuencias:**
- Las memorias eliminadas no aparecen en el resumen final
- Si el historial queda vacío: *"No recordás nada de lo que hiciste. Eso también dice algo."*
- Si todas las memorias de culpa son eliminadas: puede alterar qué ending se activa

**Nota de implementación:** `Player.gastar_memoria(indice)` que elimina `historial[indice]`
y registra internamente cuántas se gastaron (para el ending de historial vacío).

---

## Plan de implementación — prioridad

| Complejidad | Feature | Archivo/s afectados |
|-------------|---------|---------------------|
| Baja | Aliento del Umbral en Player + save | `player.py`, `save_system.py` |
| Baja | 8 ítems con efectos + inventario max 3 | `player.py`, `game_engine.py` |
| Media | Cofres de Piedra (llave) y de Eco (victoria 3/3) | `levels/level1-4.py` |
| Media | Cofre del Umbral (Aliento ≥ 5) | `game_engine.py` |
| Media | Recuperación adicional (Descanso, Respirar) | `combat_system.py` |
| Media | Aliado: El Viajero Perdido | `levels/level2.py`, `combat_system.py` |
| Media | Aliado: La Voz del Umbral | `levels/level5.py`, `game_engine.py` |
| Media | Laberintos en Level 3, 7, 9 | `levels/level3.py`, `level7.py`, `level9.py` |
| Alta | Enemigo secreto: El Hambre | `player.py`, `enemies.py`, `game_engine.py` |
| Alta | Enemigo secreto: El Otro | `enemies.py`, `levels/level5.py` |
| Alta | Enemigo secreto: El Doble (New Game+) | `enemies.py`, `levels/level4.py`, `save_system.py` |
| Alta | Memoria como moneda | `player.py`, `levels/`, `game_engine.py` |
| Alta | Ending secreto (fusión con El Otro) | `game_engine.py`, `determinar_final()` |

---

## Assets de imagen requeridos para estas mecánicas

### Parámetros generales (aplicar a todos)
```
Sufijo fijo: dark fantasy illustration, vermis style, occult medieval manuscript,
             ink drawing, high detail, textured parchment, desaturated palette,
             muted colors, grim atmosphere, symbolic composition, eerie, unsettling,
             no modern elements
Ratio: 4:3 horizontal
```

---

### Enemigos secretos

| Archivo destino | Nombre | Prompt |
|---|---|---|
| `assets/enemy_otro.jpg` | El Otro | A nearly perfect symmetrical composition, two identical figures standing face to face in absolute equilibrium, neither dominant, their outlines beginning to dissolve at the edges where they almost touch, the surrounding space without ground or context, the unsettling calm of perfect balance between self and reflection, the mirror question made flesh, neither more real than the other `dark fantasy illustration, vermis style, occult medieval manuscript, ink drawing, high detail, textured parchment, desaturated palette, muted colors, grim atmosphere, symbolic composition, eerie, unsettling, no modern elements` |
| `assets/enemy_hambre.jpg` | El Hambre | A formless compression of darkness and sharp angles, all edges and no center, a being of pure appetite without recognizable form, the space around it warped and hungry, no distinguishable features, no eyes, no mouth, only the overwhelming spatial sensation of something that consumes without pause, ancient, mindless, absolute `dark fantasy illustration, vermis style, occult medieval manuscript, ink drawing, high detail, textured parchment, desaturated palette, muted colors, grim atmosphere, symbolic composition, eerie, unsettling, no modern elements` |
| `assets/enemy_doble.jpg` | El Doble | Two figures occupying the same space simultaneously, one slightly more solid than the other, shared fragments of memory visible as faint light bleeding between them, postures almost identical but diverging in subtle wrongness, the ghost of a previous self overlaid on the present, uncanny recognition and dread merged into a single form `dark fantasy illustration, vermis style, occult medieval manuscript, ink drawing, high detail, textured parchment, desaturated palette, muted colors, grim atmosphere, symbolic composition, eerie, unsettling, no modern elements` |

---

### NPCs / Aliados

| Archivo destino | Nombre | Prompt |
|---|---|---|
| `assets/npc_viajero.jpg` | El Viajero Perdido | A wandering figure in worn traveling clothes, pausing at a fork in a stone corridor, back partially turned, carrying too little for such a deep journey, the light uncertain and sourceless, the posture of someone who has forgotten the destination but continues moving, neither threatening nor safe, simply present and going down `dark fantasy illustration, vermis style, occult medieval manuscript, ink drawing, high detail, textured parchment, desaturated palette, muted colors, grim atmosphere, symbolic composition, eerie, unsettling, no modern elements` |
| `assets/npc_voz.jpg` | La Voz del Umbral | An absence that has learned to gather, a void in the air where something accumulates without fully taking shape, surrounded by faint radiating lines like frozen sound, neither face nor body visible, only the sense of a presence that has always been listening and now chooses to reply, intimate and impersonal at once, the space between silence and speech made visible `dark fantasy illustration, vermis style, occult medieval manuscript, ink drawing, high detail, textured parchment, desaturated palette, muted colors, grim atmosphere, symbolic composition, eerie, unsettling, no modern elements` |

---

### Objetos / Cofres

| Archivo destino | Nombre | Prompt |
|---|---|---|
| `assets/chest_stone.jpg` | Cofre de Piedra | An ancient stone chest sealed with worn carved symbols, partially buried in narrow underground rubble, the lock shaped like a closed eye, waiting in absolute silence, the stone around it darker as if the chest absorbs the ambient light, a composition of patience and sealed secrets `dark fantasy illustration, vermis style, occult medieval manuscript, ink drawing, high detail, textured parchment, desaturated palette, muted colors, grim atmosphere, symbolic composition, eerie, unsettling, no modern elements` |
| `assets/chest_umbral.jpg` | Cofre del Umbral | A chest that is also a threshold, its lid the boundary of something else, covered in layered ritual engravings that overlap and contradict each other, the surrounding space subtly distorted, an object that should not exist in this form, an invitation that is also a warning, the seams glowing faintly with contained energy `dark fantasy illustration, vermis style, occult medieval manuscript, ink drawing, high detail, textured parchment, desaturated palette, muted colors, grim atmosphere, symbolic composition, eerie, unsettling, no modern elements` |

---

### Exploración / Laberintos

| Archivo destino | Nombre | Prompt |
|---|---|---|
| `assets/maze.jpg` | Laberinto | A network of identical stone corridors stretching in every direction, each intersection the same as the last, each torch at the same height casting the same shadows, perspective repeating and folding infinitely, the subtle architecture of a space designed to disorient, the corridors narrowing almost imperceptibly toward an unseen center that cannot be reached `dark fantasy illustration, vermis style, occult medieval manuscript, ink drawing, high detail, textured parchment, desaturated palette, muted colors, grim atmosphere, symbolic composition, eerie, unsettling, no modern elements` |
| `assets/dead_end.jpg` | Callejón sin salida | A corridor that ends in a blank stone wall, marks left by previous travelers barely visible, a candle stub on the floor still lit, the atmosphere of accumulated wrong turns, the sense that this was not always a dead end, something carved into the stone that takes a moment to read and longer to understand `dark fantasy illustration, vermis style, occult medieval manuscript, ink drawing, high detail, textured parchment, desaturated palette, muted colors, grim atmosphere, symbolic composition, eerie, unsettling, no modern elements` |

---

## Prompts en inglés para assets ya generados (transformación de los originales)

> Todos los prompts originales en español fueron transformados a la estructura analizada:
> **[escena descriptiva en sintagma nominal extendido] + [sufijo estilístico fijo]**

### Análisis de la estructura usada como referencia

Los seis prompts de referencia comparten:
1. Comienzo con artículo indefinido + sustantivo que sitúa la escena (`A lone figure...`, `A circular stone chamber...`)
2. Enumeración de elementos visuales, espaciales y atmosféricos sin verbos principales
3. Relación entre figura y entorno, escala, ausencia de luz definida, sensaciones de vacío o juicio
4. Tono evocador, simbólico, sin instrucciones explícitas
5. Sufijo estilístico idéntico y fijo que define medio, estilo, paleta y atmósfera

---

### Enemigos nuevos

**`assets/enemy5.jpg` — The Echo**
A translucent human figure formed of suspended voice fragments like shattered glass, mouthless, eyes two absolute black holes, standing in an obsidian cavern where silence has weight, the walls jagged and unreflective, the air thick with broken whispers, no visible light source, the figure both present and absent, a ghost of spoken memory dark fantasy illustration, vermis style, occult medieval manuscript, ink drawing, high detail, textured parchment, desaturated palette, muted colors, grim atmosphere, symbolic composition, eerie, unsettling, no modern elements

**`assets/enemy6.jpg` — The Archivist**
An ancient being with hundreds of thin arms, each hand clutching a book or a rolled parchment, skin entirely covered in handwritten text, eyes blinded and perhaps sealed by knowledge, surrounded by drifting dust and a sickly yellow glow, the chamber silent like a forgotten tomb, overwhelming presence of recorded memory and catalogued sin dark fantasy illustration, vermis style, occult medieval manuscript, ink drawing, high detail, textured parchment, desaturated palette, muted colors, grim atmosphere, symbolic composition, eerie, unsettling, no modern elements

**`assets/enemy7.jpg` — The Living Rift**
A shapeless fissure in reality, a wound in the world with stone edges that pulse slowly like breathing flesh, from within seeps a black light that absorbs rather than illuminates, set against absolute void, no ground, no sky, only the sensation of something watching through the tear, the aperture both wound and invitation, cosmic and intimate horror merged dark fantasy illustration, vermis style, occult medieval manuscript, ink drawing, high detail, textured parchment, desaturated palette, muted colors, grim atmosphere, symbolic composition, eerie, unsettling, no modern elements

**`assets/enemy8.jpg` — The Witness**
A hooded figure without a visible body, a mask of countless overlapping eyes where the face should be, seated in the posture of a judge, cold diffuse light falling from nowhere, the space around it undefined and silent, the overwhelming sensation of being observed and catalogued, immutable and patient presence, neither hostile nor compassionate, absolute dark fantasy illustration, vermis style, occult medieval manuscript, ink drawing, high detail, textured parchment, desaturated palette, muted colors, grim atmosphere, symbolic composition, eerie, unsettling, no modern elements

**`assets/enemy_boss.jpg` — The Incarnate Threshold**
An entity shaped like a humanoid doorway, half ancient stone and half living darkness, where the face belongs a smaller threshold opens inward toward deeper void, a recursive passage of dread, the surface carved with worn ritual marks, the atmosphere ceremonial and final, a being that does not attack but is itself the obstacle, the last door before everything dark fantasy illustration, vermis style, occult medieval manuscript, ink drawing, high detail, textured parchment, desaturated palette, muted colors, grim atmosphere, symbolic composition, eerie, unsettling, no modern elements

---

### Imágenes de niveles nuevos

**`assets/lvl7.jpg` — The Judgment Hall**
A vast empty circular chamber with stone seats for thousands of absent judges, a single illuminated chair at the center beneath a shaft of moonlight, decaying gothic arches stretching into shadow above, the air heavy with deferred verdicts and inherited silence, absolute stillness, the weight of countless unseen gazes concentrated on one empty point dark fantasy illustration, vermis style, occult medieval manuscript, ink drawing, high detail, textured parchment, desaturated palette, muted colors, grim atmosphere, symbolic composition, eerie, unsettling, no modern elements

**`assets/lvl8.jpg` — The River of Memories**
A subterranean river of black water that reflects images of the past like mirrors, shores of fine ash on both banks, a ghostly blue radiance rising from beneath the surface, the current slow and silent, reflections that do not match what stands above them, the atmosphere of irrevocable loss and things that cannot be recovered, a path through what remains when time has finished dark fantasy illustration, vermis style, occult medieval manuscript, ink drawing, high detail, textured parchment, desaturated palette, muted colors, grim atmosphere, symbolic composition, eerie, unsettling, no modern elements

**`assets/lvl9.jpg` — The Library of Oblivion**
An infinite library vanishing into absolute darkness, shelves filled with blank books whose pages hold no ink, stairways ascending and descending in every impossible direction, the architecture a labyrinth of forgotten thoughts, isolated candle flames the only light sources, the smell of cold stone and unwritten memory, a place where knowledge goes to disappear and where forgetting is the only catalog dark fantasy illustration, vermis style, occult medieval manuscript, ink drawing, high detail, textured parchment, desaturated palette, muted colors, grim atmosphere, symbolic composition, eerie, unsettling, no modern elements

**`assets/lvl10.jpg` — The Final Mirror**
A chamber dominated by a single giant mirror covering one entire wall, its reflection showing a different world of warm light and joyful figures going about ordinary life, stark contrast to the cold darkness of the room on this side of the glass, the surface unnaturally clear, the silent promise of an unreachable elsewhere, a test of desire made architectural dark fantasy illustration, vermis style, occult medieval manuscript, ink drawing, high detail, textured parchment, desaturated palette, muted colors, grim atmosphere, symbolic composition, eerie, unsettling, no modern elements

---

### Pantallas de UI y menú

**`assets/menu_alt.jpg` — Alternative Menu**
A cave interior seen from behind a lone silhouette facing a distant and uncertain light, mist curling along the stone floor, the sense of a final and irreversible decision hovering in the air, the entrance a dark memory fading behind, a composition of departure and unknown futures, the light ahead too distant to offer certainty dark fantasy illustration, vermis style, occult medieval manuscript, ink drawing, high detail, textured parchment, desaturated palette, muted colors, grim atmosphere, symbolic composition, eerie, unsettling, no modern elements

**`assets/game_over.jpg` — Game Over Screen**
A deep penumbra of indefinite shifting shapes, no human figure present, only visual silence, an aftermath without motion or resolution, void as ending, absolute stillness, the composition ready to receive written words of finality, darkness that has already swallowed everything that was here dark fantasy illustration, vermis style, occult medieval manuscript, ink drawing, high detail, textured parchment, desaturated palette, muted colors, grim atmosphere, symbolic composition, eerie, unsettling, no modern elements

**`assets/intro4.jpg` — Intro Screen 4**
The view from inside a cave looking outward toward an exterior world, the only light source the outside beyond the entrance, the silhouette of the character already inside the darkness facing outward, the entrance a diminishing frame of pale light, the moment of no return already passed, the threshold crossed before the decision was made dark fantasy illustration, vermis style, occult medieval manuscript, ink drawing, high detail, textured parchment, desaturated palette, muted colors, grim atmosphere, symbolic composition, eerie, unsettling, no modern elements

---

### Retratos de personaje

**`assets/portrait_warrior.jpg` — Warrior**
A bust portrait of a warrior in eroded emblemless armor, face deeply marked by years rather than battle, expression carrying more internal weight than physical strength, harsh sidelight carving the features into relief, dark background swallowing the edges of the figure, a study of burden sustained long past the point of choice dark fantasy illustration, vermis style, occult medieval manuscript, ink drawing, high detail, textured parchment, desaturated palette, muted colors, grim atmosphere, symbolic composition, eerie, unsettling, no modern elements

**`assets/portrait_mage.jpg` — Mage**
A hooded figure with face partially visible beneath the shadow of the cowl, eyes glowing with a faint inner blue-violet light almost extinguished, hands bearing runes that have nearly faded, the expression heavy with forbidden knowledge and the cost of carrying it, the air around cold and still, a portrait of wisdom that has become indistinguishable from sorrow dark fantasy illustration, vermis style, occult medieval manuscript, ink drawing, high detail, textured parchment, desaturated palette, muted colors, grim atmosphere, symbolic composition, eerie, unsettling, no modern elements

**`assets/portrait_rogue.jpg` — Thief**
A face divided precisely between shadow and light, a sidelong appraising gaze directed at something just out of frame, no weapons visible and yet the posture suggests complete readiness, the tension between what is concealed and what is permitted to show defining the entire portrait, an atmospheric study of duplicity made into a way of surviving dark fantasy illustration, vermis style, occult medieval manuscript, ink drawing, high detail, textured parchment, desaturated palette, muted colors, grim atmosphere, symbolic composition, eerie, unsettling, no modern elements
