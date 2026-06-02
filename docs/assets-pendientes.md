# Assets pendientes — Descenso al Umbral

Imágenes a generar para completar la cobertura visual del juego.
Todas en ratio **4:3 horizontal**.

---

## Parámetros generales (aplicar a todos los prompts)

```
Sufijo fijo: dark fantasy illustration, vermis style, occult medieval manuscript,
             ink drawing, high detail, textured parchment, desaturated palette,
             muted colors, grim atmosphere, symbolic composition, eerie, unsettling,
             no modern elements
Ratio: 4:3 horizontal
```

---

## Assets pendientes (2 imágenes)

Estas son las únicas imágenes que faltan para completar la cobertura visual de todas las mecánicas implementadas.

| Archivo destino | Nombre | Prompt | Dónde se usa |
|---|---|---|---|
| `assets/chest_eco.jpg` | Cofre de Eco | A chest made of compressed echoes and crystallized sound, its surface etched with recursive wave patterns that repeat inward forever, the lock a spiral of frozen resonance, surrounded by faint reverberation lines in the air, the suggestion of past voices trapped inside seeking release, an object that rewards those who listened rather than those who struck `dark fantasy illustration, vermis style, occult medieval manuscript, ink drawing, high detail, textured parchment, desaturated palette, muted colors, grim atmosphere, symbolic composition, eerie, unsettling, no modern elements` | `ofrecer_cofre_eco()` — actualmente usa imagen del nivel como fondo |
| `assets/key_stone.jpg` | Llave de Piedra | A single ancient stone key on bare ground, worn smooth by centuries of handling, carved from the same material as the walls around it, its teeth irregular as if grown rather than cut, a relic that opened something important for someone who no longer exists, the sense of an object passed from hand to hand through depths that should not have been reached `dark fantasy illustration, vermis style, occult medieval manuscript, ink drawing, high detail, textured parchment, desaturated palette, muted colors, grim atmosphere, symbolic composition, eerie, unsettling, no modern elements` | Al encontrar la llave de piedra en levels 1, 3 y 7 |

---

## Estado de todos los assets del juego

### ✅ Completados e integrados en el código

| Archivo | Uso |
|---|---|
| `assets/lvl1.jpg` — `lvl10.jpg` | Imágenes de los 10 niveles |
| `assets/enemy1.jpg` — `enemy8.jpg` | Los 8 enemigos regulares + El Eco/Archivista/Grieta/Testigo |
| `assets/enemy_boss.jpg` | El Umbral Encarnado |
| `assets/enemy_otro.jpg` | El Otro (enemigo secreto) |
| `assets/enemy_hambre.jpg` | El Hambre (enemigo secreto) |
| `assets/enemy_doble.jpg` | El Doble (enemigo secreto NG+) |
| `assets/npc_viajero.jpg` | El Viajero Perdido (aliado) |
| `assets/npc_voz.jpg` | La Voz del Umbral (aliado) |
| `assets/chest_stone.jpg` | Cofre de Piedra |
| `assets/chest_umbral.jpg` | Cofre del Umbral |
| `assets/maze.jpg` | Fases de laberinto (levels 3, 7, 9) |
| `assets/dead_end.jpg` | Callejones sin salida |
| `assets/portrait_warrior.jpg` | Retrato clase Guerrero |
| `assets/portrait_mage.jpg` | Retrato clase Hechicero |
| `assets/portrait_rogue.jpg` | Retrato clase Ladrón |
| `assets/death_warrior.jpg` | Pantalla de muerte Guerrero |
| `assets/death_mage.jpg` | Pantalla de muerte Hechicero |
| `assets/death_rogue.jpg` | Pantalla de muerte Ladrón |
| `assets/menu.jpg` | Menú principal |
| `assets/menu_alt.jpg` | Menú alternativo (créditos) |
| `assets/game_over.jpg` | Fallback pantalla de muerte |
| `assets/intro1.jpg` — `intro4.jpg` | Pantallas de introducción narrativa |
| `assets/pentagram.jpg` | Icono de la ventana |

### ⏳ Pendientes

| Archivo | Uso | Prioridad |
|---|---|---|
| `assets/chest_eco.jpg` | Cofre de Eco | Media — actualmente usa fondo del nivel |
| `assets/key_stone.jpg` | Llave de Piedra al ser encontrada | Media — actualmente solo texto |

---

## Nota sobre la música

Los archivos en `music/` tienen nombres ilegibles (`. (N).mp3`).
Renombrarlos activa el sistema de música por nivel ya implementado en `ui.py`:

| Nombre destino | Uso |
|---|---|
| `menu.mp3` | Menú principal |
| `nivel_0.mp3` | Nivel 1 — La Cueva del Origen |
| `nivel_1.mp3` | Nivel 2 — El Espejo de las Formas |
| `nivel_2.mp3` | Nivel 3 — El Ritual de la Entrega |
| `nivel_3.mp3` | Nivel 4 — El Rey de las Sombras |
| `nivel_4.mp3` | Nivel 5 — Las Moradas de los Muertos |
| `nivel_5.mp3` | Nivel 6 — El Umbral Final |
| `nivel_6.mp3` | Nivel 7 — La Sala del Juicio |
| `nivel_7.mp3` | Nivel 8 — El Río de Recuerdos |
| `nivel_8.mp3` | Nivel 9 — La Biblioteca del Olvido |
| `nivel_9.mp3` | Nivel 10 — El Espejo Final |
| `boss.mp3` | Combate El Umbral Encarnado (ya buscado por el código) |
| `ambiente.mp3` | Pantallas de muerte y créditos |

> El código busca `nivel_N.mp3` automáticamente. Sin renombrar, usa aleatorio.
