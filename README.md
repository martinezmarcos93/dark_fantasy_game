# 🜏 Descenso al Umbral
### Aventura de Texto Psicológica en Fantasía Oscura

---

## 🧠 Descripción

**Descenso al Umbral** es una aventura narrativa desarrollada en Python con Pygame que combina fantasía oscura con exploración psicológica. El jugador cree estar ingresando a un calabozo para cumplir una misión heroica. Pero a medida que avanza… descubre que el verdadero recorrido es hacia su propia mente.

No se trata de ganar. Se trata de revelarse.

---

## 🌑 Características

- Sistema de decisiones con consecuencias acumulativas y diferidas
- Variables psicológicas ocultas que el jugador nunca ve directamente
- Narrativa simbólica y esotérica inspirada en psicología junguiana
- Múltiples finales determinados por el comportamiento acumulado
- Combate narrativo diferenciado por clase (mecánica 2d6 + stat)
- Texto que se distorsiona visualmente según el estado psíquico del personaje
- Interfaz gráfica con Pygame: HUD, fade in/out, fuente gótica
- Sonidos de teclas aleatorios al escribir el nombre del personaje
- Música de fondo aleatoria desde carpeta `music/`
- Sistema de guardado y carga de partida en JSON
- Ventana redimensionable con escalado letterbox (proporción preservada)

---

## 🧬 Sistema de Psique

El juego registra cinco vectores ocultos que se acumulan a lo largo de toda la partida:

| Variable | Descripción |
|---|---|
| `violencia` | Tendencia a resolver por la fuerza o destrucción |
| `miedo` | Evasión, parálisis, negación del riesgo |
| `culpa` | Peso de las omisiones y las decisiones no tomadas |
| `lucidez` | Comprensión lúcida de lo que ocurre |
| `corrupción` | Integración con la oscuridad del Umbral |

Estas variables determinan cómo reacciona el mundo, qué eventos se desencadenan y cuál será el destino final del personaje.

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

Cada nivel tiene dos fases: **combate narrativo** (diferenciado por clase) y **decisión psicológica** (con consecuencias ocultas).

---

## ⚔️ Clases

| Clase | Stat principal | Recurso |
|---|---|---|
| Guerrero | Fuerza | Stamina |
| Hechicero | Mente | Magia |
| Ladrón | Resistencia | Ingenio |

Cada clase enfrenta los mismos enemigos con mecánicas y textos distintos.

---

## 🜁 Finales

El juego tiene ocho finales narrativos posibles determinados por la combinación de variables psíquicas al terminar el descenso:

- **Entidad del Abismo** — corrupción extrema
- **Lucidez Total** — lucidez alta, corrupción moderada
- **Locura** — miedo dominante
- **Autodestrucción** — violencia y corrupción combinadas
- **Culpa Eterna** — culpa dominante
- **Voluntad Pura** — corrupción y lucidez en tensión
- **Disolución** — miedo sin lucidez
- **Olvido** — ningún vector dominante

Ningún final es explícitamente "bueno" o "malo".

---

## 🏗️ Estructura del Proyecto

```
aventura oscura/
├── main.py              # Entrada
├── game_engine.py       # Director: loop, combate, finales
├── ui.py                # Pygame: render, input, audio, escalado
├── player.py            # Objeto jugador: stats, psique, daño
├── menu.py              # Menú principal y créditos
├── intro.py             # Pantallas de introducción
├── save_system.py       # Guardado/carga JSON
├── levels/
│   ├── level1.py  →  La Cueva del Origen
│   ├── level2.py  →  El Espejo de las Formas
│   ├── level3.py  →  El Ritual de la Entrega
│   ├── level4.py  →  El Rey de las Sombras
│   ├── level5.py  →  Las Moradas de los Muertos
│   └── level6.py  →  El Umbral Final
├── assets/              # Imágenes de niveles y enemigos
├── fonts/               # Fuente gótica (Goth.ttf)
├── music/               # Música de fondo (.mp3)
└── sounds/              # Sonidos de teclas (.wav)
```

---

## ▶️ Cómo Ejecutar

**Requisitos:**
```
Python 3.11+
pygame
```

**Instalación:**
```bash
git clone https://github.com/martinezmarcos93/dark_fantasy_game.git
cd dark_fantasy_game
pip install pygame
python main.py
```

**Controles:**
| Tecla | Acción |
|---|---|
| `ESPACIO` | Continuar pantalla narrativa |
| `1` / `2` / `3` / `4` | Elegir opción |
| `↑` / `↓` | Scroll de texto |
| `ESC` | Volver al menú (guarda automáticamente) |
| Clic | Seleccionar opción con mouse |

---

## 🖥️ Tecnologías

- Python 3.11
- Pygame (gráficos, audio, input)
- JSON (sistema de guardado)

---

## 🔮 Roadmap

- [ ] Iconos de psique visibles (feedback sutil sin revelar valores)
- [ ] Más variaciones de texto en cartel de psique según variable afectada
- [ ] Niveles adicionales con bifurcaciones narrativas
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
