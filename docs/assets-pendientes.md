# Assets pendientes — Descenso al Umbral

Imágenes a generar con Leonardo.ai para expansión del juego.
Todas en ratio **4:3 horizontal** (referencia: 480×500px).

---

## Parámetros generales (aplicar a todos los prompts)

```
Estilo base:   dark fantasy, oil painting, cinematic lighting
Ratio:         4:3 horizontal
Paleta:        negros, grises, ocres + un único color de acento frío
NO incluir:    texto, UI, marcos, interfaces
Referencia:    Elden Ring concept art, Dark Souls key art, Zdzislaw Beksinski
```

---

## Enemigos nuevos

| Archivo destino | Nombre | Prompt |
|---|---|---|
| `assets/enemy5.jpg` | El Eco | Figura humana translúcida hecha de fragmentos de voces suspendidas en el aire como cristal roto. Sin boca. Ojos que son dos agujeros negros. Fondo de caverna de obsidiana. Dark fantasy, oil painting. |
| `assets/enemy6.jpg` | El Archivista | Ser anciano con cientos de brazos delgados, cada uno sosteniendo un libro o pergamino. Cubierto de texto escrito en su piel. Ciego. Rodeado de polvo y luz amarilla. Gothic horror, introspective. |
| `assets/enemy7.jpg` | La Grieta Viviente | No tiene forma definida — es una fisura en la realidad con bordes de piedra que pulsan como una herida. Del interior emerge luz negra. Fondo de vacío absoluto. Cosmic horror, abstract. |
| `assets/enemy8.jpg` | El Testigo | Figura encapuchada sin cuerpo visible, solo una máscara de muchos ojos superpuestos. Sentado como juez. Luz difusa fría. Psychological horror, dark fantasy. |
| `assets/enemy_boss.jpg` | El Umbral Encarnado | Entidad que parece una puerta con forma humanoide. Mitad piedra, mitad oscuridad. Donde debería estar la cara hay otro umbral más pequeño. Boss final alternativo. Surreal dark fantasy. |

---

## Imágenes de niveles nuevos

| Archivo destino | Nombre | Prompt |
|---|---|---|
| `assets/lvl7.jpg` | La Sala del Juicio | Sala circular enorme y vacía con sillas de piedra para miles de jueces ausentes. Una silla en el centro iluminada. Arquitectura gótica decadente. Luz cenital de luna. |
| `assets/lvl8.jpg` | El Río de Recuerdos | Río subterráneo de agua oscura que refleja imágenes del pasado como espejos. Orillas de ceniza. Luz azul fantasmal desde debajo del agua. Melancholic dark fantasy. |
| `assets/lvl9.jpg` | La Biblioteca del Olvido | Biblioteca infinita que se pierde en la oscuridad. Libros en blanco. Escaleras en todas direcciones. Inspirado en Borges y Escher. Luz de velas aisladas. |
| `assets/lvl10.jpg` | El Espejo Final | Sala con un único espejo gigante que ocupa toda una pared. El reflejo muestra un mundo diferente con luz cálida y gente feliz. Contraste total con la oscuridad de la sala. |

---

## Pantallas de UI y menú

| Archivo destino | Nombre | Prompt |
|---|---|---|
| `assets/menu_alt.jpg` | Menú alternativo | Cueva con una silueta de espaldas mirando hacia una luz lejana. Composición desde atrás. Niebla. Atmósfera de decisión final. Para reemplazar el menú actual si se desea. |
| `assets/game_over.jpg` | Pantalla Game Over | Penumbra con formas indefinidas, sin figura humana. Solo silencio visual. Sin texto. Fondo para superponerle el texto de muerte en pantalla. |
| `assets/intro4.jpg` | Intro — pantalla 4 | La entrada de una cueva desde adentro mirando hacia afuera. La luz exterior es la única fuente de luz. Silueta del personaje ya adentro. |

---

## Retratos de personaje

Para una futura pantalla de selección de clase con retrato visual.

| Archivo destino | Clase | Prompt |
|---|---|---|
| `assets/portrait_warrior.jpg` | Guerrero | Busto de guerrero con armadura erosionada sin emblemas. Cara marcada, expresión de carga interna más que de fuerza. Luz lateral dura. Fondo oscuro. Realismo oscuro. |
| `assets/portrait_mage.jpg` | Hechicero | Figura encapuchada, rostro parcialmente visible. Ojos con luz interior azul/violeta tenue. Manos con runas casi apagadas. Expresión de conocimiento pesado. Dark fantasy. |
| `assets/portrait_rogue.jpg` | Ladrón | Rostro con mitad en sombra y mitad iluminada. Mirada lateral, evaluativa. Sin armas visibles. La tensión entre lo que oculta y lo que muestra define la imagen. Atmosférico. |

---

## Música pendiente de renombrar

Los archivos en `music/` tienen nombres ilegibles (`. (N).mp3`).
Renombrarlos así activa el sistema de música por nivel ya implementado:

| Nombre actual | Nombre destino | Uso |
|---|---|---|
| `. (9).mp3` | `menu.mp3` | Menú principal |
| `. (10).mp3` | `nivel_0.mp3` | Nivel 1 — La Cueva del Origen |
| `. (11).mp3` | `nivel_1.mp3` | Nivel 2 — El Espejo de las Formas |
| `. (12).mp3` | `nivel_2.mp3` | Nivel 3 — El Ritual de la Entrega |
| `. (13).mp3` | `nivel_3.mp3` | Nivel 4 — El Rey de las Sombras |
| `. (14).mp3` | `nivel_4.mp3` | Nivel 5 — Las Moradas de los Muertos |
| `. (15).mp3` | `nivel_5.mp3` | Nivel 6 — El Umbral Final |
| `. (16).mp3` | `combate.mp3` | Reservado para música de combate (futuro) |
| Resto | — | Libres para nuevos niveles o ambient |

> El código busca `nivel_N.mp3` automáticamente. Sin renombrar, sigue usando aleatorio.
