# 🜏 Descenso al Umbral
### Aventura de Texto Psicológica en Fantasía Oscura

---

## 🧠 Descripción

**Descenso al Umbral** es una aventura narrativa desarrollada en Python con Pygame que combina fantasía oscura con exploración psicológica. El jugador cree estar ingresando a un calabozo para cumplir una misión heroica. Pero a medida que avanza… descubre que el verdadero recorrido es hacia su propia mente.

No se trata de ganar. Se trata de revelarse.

---

## 🌑 Características

- Sistema de decisiones con consecuencias psicológicas acumulativas y diferidas
- Cinco variables psicológicas ocultas que moldean el mundo y el ending
- Historial de decisiones: resumen de cada elección antes del final
- Pantalla de psique con barras visuales entre cada nivel
- Filtro de color progresivo en la imagen según el estado psíquico dominante
- Narrativa simbólica y esotérica inspirada en psicología junguiana
- 14 finales narrativos determinados por la combinación de variables psíquicas
- Combate narrativo en 3 rondas diferenciado por clase y por enemigo
- Sistema de críticos: tiradas excepcionales hacen daño doble
- Acciones de combate con impacto psicológico (Furia → violencia, Abismo → corrupción)
- Enemigos adaptativos: detectan acciones repetidas y cambian de patrón
- Textos de ataque diferenciados por clase del jugador en los 4 enemigos
- Sistema de energía integrado: Magia, Stamina e Ingenio con costos reales
- Acción de emergencia "Improvisar" para Ladrón sin Ingenio
- Texto narrativo con efecto typewriter (salteable)
- Interfaz gráfica con Pygame: HUD, fade in/out, fuente gótica, letterbox
- 3 slots de guardado independientes con menú de selección
- Ventana redimensionable con escalado proporcional
- Música de fondo aleatoria y sonidos de tecla al escribir el nombre

---

## 🧬 Sistema de Psique

El juego registra cinco vectores ocultos que se acumulan a lo largo de la partida (rango 0–100). Cambian por decisiones narrativas **y** por acciones en combate:

| Variable | Fuente narrativa | Fuente en combate |
|---|---|---|
| `violencia` | Romper el espejo, atacar las versiones | Furia Ciega, Apuñalar |
| `miedo` | Llamar en la oscuridad, negar las versiones | Huir |
| `culpa` | Rechazar las versiones, ignorar el altar | — |
| `lucidez` | Mirar el espejo, aceptar las versiones | Nombre Verdadero |
| `corrupción` | Avanzar sin luz, ofrecer sangre, destruir | Fragmento del Abismo |

La pantalla de psique al final de cada nivel muestra el estado actual con barras visuales. La imagen del juego adquiere un tinte de color progresivo según el vector dominante:

- **Violencia** → rojo oscuro
- **Miedo** → azul profundo
- **Culpa** → marrón cálido
- **Lucidez** → verde frío
- **Corrupción** → púrpura

---

## 🗺️ Estructura del Descenso

| Nivel | Nombre | Enemigo |
|---|---|---|
| 1 | La Cueva del Origen | El Guardián de Piedra |
| 2 | El Espejo de las Formas | El Reflejo Armado |
| 3 | El Ritual de la Entrega | El Sacerdote Sin Rostro |
| 4 | El Rey de las Sombras | La Sombra Soberana |
| 5 | Las Moradas de los Muertos | — |
| 6 | El Umbral Final | — |

Cada nivel con combate tiene dos fases: **combate narrativo** (3 rondas, diferenciado por clase) y **decisión psicológica** (con consecuencias acumuladas). Los niveles 5 y 6 son puramente psicológicos, con texto distorsionado según el estado mental del personaje.

---

## ⚔️ Clases

| Clase | Stat principal | Recurso | Mecánica distintiva |
|---|---|---|---|
| Guerrero | Fuerza | Stamina (40) | Golpe Cargado (−15 ST) y Furia Ciega (−20 ST, daño masivo) |
| Hechicero | Mente | Magia (100) | 5 hechizos de un solo uso con costos de 10–40 MP |
| Ladrón | Resistencia | Ingenio (70) | Setup de posición → ataques especiales; Improvisar sin Ingenio |

### Hechizos del Hechicero

| Hechizo | Costo | Efecto |
|---|---|---|
| Palabra de Fuego | 15 MP | Daño alto directo |
| Velo de Sombra | 10 MP | Reduce daño enemigo esta ronda |
| Resonancia Mental | 10 MP | Ventaja en la siguiente tirada |
| Nombre Verdadero | 20 MP | Paraliza al enemigo una ronda (+lucidez) |
| Fragmento del Abismo | 40 MP | Daño masivo, también te daña (+corrupción) |

---

## 🔮 Sistema de Finales (14 endings)

El ending se determina por el vector **dominante** y, si hay un segundo vector también elevado (≥35), por la **combinación**.

### Finales por stat dominante
| Ending | Condición |
|---|---|
| Entidad del Umbral | Corrupción dominante ≥ 40 |
| Integración | Lucidez dominante, corrupción < 50 |
| Voluntad en el Abismo | Lucidez dominante, corrupción ≥ 50 |
| Fragmentación | Miedo dominante |
| Ruptura | Violencia dominante |
| El Juicio Eterno | Culpa dominante |
| Olvido | Psique equilibrada o baja |

### Finales por combinación doble
| Ending | Condición |
|---|---|
| Suspensión | Miedo + Culpa ambos altos |
| Ataque por Miedo | Violencia + Miedo ambos altos |
| Cómplice Lúcido | Culpa + Lucidez ambos altos |
| Sufrimiento Preciso | Miedo + Lucidez ambos altos |
| Ciclo de Daño | Violencia + Culpa ambos altos |
| Voluntad Pura | Corrupción + Lucidez ambos altos |

Ningún final es explícitamente "bueno" o "malo".

---

## ⚔️ Sistema de Combate

- **3 rondas** por enemigo. Quien gana 2 de 3 gana el combate.
- Mecánica de dados: **2d6 + stat vs dificultad × 2**. Con ventaja: 3d6 mejores 2.
- **Críticos**: superar el umbral por 4+ hace daño ×2.
- Acciones defensivas/utilitarias resultan en ronda neutral (ninguno suma).
- Los **enemigos se adaptan**: si repetís la misma acción dos veces seguidas, cambian de patrón.
- Cada enemigo tiene textos de ataque diferentes según tu clase.

---

## 🏗️ Estructura del Proyecto

```
dark_fantasy_game/
├── main.py              # Entrada
├── game_engine.py       # Director: loop, slots, finales, resúmenes
├── ui.py                # Pygame: render, typewriter, filtro psique, audio
├── player.py            # Objeto jugador: stats, psique, historial
├── combat_system.py     # Sistema de combate: dados, críticos, enemigos
├── enemies.py           # Definición de los 4 enemigos con textos por clase
├── menu.py              # Menú principal y créditos
├── intro.py             # Pantallas de introducción
├── save_system.py       # 3 slots de guardado en saves/
├── requirements.txt     # pygame>=2.1.0
├── levels/
│   ├── level1.py  →  La Cueva del Origen
│   ├── level2.py  →  El Espejo de las Formas
│   ├── level3.py  →  El Ritual de la Entrega
│   ├── level4.py  →  El Rey de las Sombras
│   ├── level5.py  →  Las Moradas de los Muertos (texto distorsionado)
│   └── level6.py  →  El Umbral Final (texto distorsionado)
├── assets/              # Imágenes de niveles, enemigos y muertes por clase
├── fonts/               # Fuente gótica (Goth.ttf)
├── music/               # Música de fondo (.mp3)
├── saves/               # Slots de guardado (generado automáticamente)
└── sounds/              # Sonidos de teclas (.wav / .ogg)
```

---

## ▶️ Cómo Ejecutar

**Requisitos:**
```
Python 3.11+
pygame >= 2.1.0
```

**Instalación:**
```bash
git clone https://github.com/martinezmarcos93/dark_fantasy_game.git
cd dark_fantasy_game
pip install -r requirements.txt
python main.py
```

**Controles:**

| Tecla / Acción | Efecto |
|---|---|
| `ESPACIO` | Continuar pantalla narrativa / saltar typewriter |
| `1` / `2` / `3` / `4` | Elegir opción |
| `↑` / `↓` | Scroll de texto |
| `ESC` | Volver al menú (guarda automáticamente) |
| Clic izquierdo | Seleccionar opción / saltar typewriter |

---

## 🖥️ Tecnologías

- Python 3.11
- Pygame (gráficos, audio, input)
- JSON (sistema de guardado por slots)

---

## 🔮 Roadmap

- [ ] Hechizos del Hechicero desbloqueables por nivel (no todos desde el inicio)
- [ ] Guerrero: stack de postura defensiva (dos Defender seguidos habilitan contraataque)
- [ ] Música diferente por nivel en lugar de selección aleatoria global
- [ ] Pantalla de estadísticas post-run (daño total, hechizos usados, rondas ganadas)
- [ ] Modo lectura — opción para jugar sin combate y explorar endings
- [ ] Dificultad configurable — multiplicador global de dificultad enemiga
- [ ] New Game+ — la psique de la partida anterior modifica la siguiente
- [ ] Efectos de partículas en transiciones
- [ ] Soporte para gamepad
- [ ] Versión empaquetada (.exe) para distribución sin Python

---

## 🧠 Filosofía

> *El dungeon no es un lugar. Es una proyección.*

Inspirado en la psicología junguiana, la tradición esotérica y el diseño de Soulsborne. La oscuridad no es el enemigo. La resistencia a conocerla, sí.

---

## ⚠️ Advertencia

Este juego contiene temas introspectivos, simbología oscura y narrativa perturbadora. No está diseñado como experiencia casual.

---

## 👤 Autor

Desarrollado por **Marcos Martínez**
