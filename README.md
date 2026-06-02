# 🜏 Descenso al Umbral
### Aventura de Texto Psicológica en Fantasía Oscura

---

## 🧠 Descripción

**Descenso al Umbral** es una aventura narrativa desarrollada en Python con Pygame que combina fantasía oscura con exploración psicológica. El jugador cree estar ingresando a un calabozo para cumplir una misión heroica. Pero a medida que avanza… descubre que el verdadero recorrido es hacia su propia mente.

No se trata de ganar. Se trata de revelarse.

---

## 🌑 Características

- Sistema de decisiones con consecuencias psicológicas acumulativas y diferidas
- Cinco variables psicológicas ocultas que moldean el mundo y los endings
- **Aliento del Umbral**: recurso de intercambio que se acumula por valentía y decisiones
- **Sistema de ítems** con inventario limitado a 3 piezas; cada ítem tiene costo secundario
- **Tres tipos de cofre**: Piedra (llave), Eco (victoria perfecta), Umbral (aliento ≥ 5)
- **Laberintos** con callejones sin salida explorables en los niveles 3, 7 y 9
- **Enemigos secretos** con condiciones de activación específicas (El Otro, El Hambre, El Doble)
- **Aliados** mutuamente excluyentes por run (El Viajero Perdido, La Voz del Umbral)
- **Memoria como moneda**: borrar recuerdos del historial a cambio de beneficios
- **15 finales narrativos** incluyendo un ending secreto por fusión psíquica
- Historial de decisiones: resumen de cada elección antes del final
- Pantalla de psique con barras visuales y Aliento del Umbral entre cada nivel
- Filtro de color progresivo en la imagen según el estado psíquico dominante
- Texto con distorsión progresiva en los niveles profundos según la psique acumulada
- Combate narrativo en 3 rondas diferenciado por clase y por enemigo
- Sistema de críticos: tiradas excepcionales hacen daño doble
- Enemigos adaptativos: detectan acciones repetidas y cambian de patrón
- Textos de ataque diferenciados por clase del jugador en todos los enemigos
- Sistema de energía integrado: Magia, Stamina e Ingenio con costos reales
- Acción "Respirar" disponible en combate cuando la energía está baja
- Bonificaciones por victoria limpia: HP, Aliento y energía según el estilo de pelea
- Texto narrativo con efecto typewriter (salteable)
- Interfaz gráfica con Pygame: HUD, fade in/out, fuente gótica, letterbox
- 3 slots de guardado independientes con menú de selección
- New Game+: la psique de la partida anterior deja eco en la siguiente
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
| `corrupción` | Avanzar sin luz, ofrecer sangre | Fragmento del Abismo |

La imagen del juego adquiere un tinte progresivo según el vector dominante: rojo oscuro (violencia), azul profundo (miedo), marrón cálido (culpa), verde frío (lucidez), púrpura (corrupción).

---

## 💨 Aliento del Umbral

Recurso de intercambio (0–10) que representa el peso de haber descendido con valentía. **No se pierde entre niveles** — sí al morir.

| Se gana | Condición |
|---|---|
| +1 | Ganar 2/3+ rondas de combate |
| +1 | Elegir una opción "peligrosa" en la fase narrativa |
| +1 | Explorar un callejón sin salida en los laberintos |
| +1 | Completar un nivel sin usar la acción "Huir" |

| Se gasta | Efecto |
|---|---|
| −2 | Descanso entre niveles (+10 HP) |
| −3 | Convencer al Viajero Perdido para que te acompañe |
| −5 | Abrir el Cofre del Umbral |

---

## 🎒 Sistema de Ítems

Inventario limitado a **3 ítems**. El límite fuerza decisiones. Cada ítem tiene costo secundario.

| Ítem | Efecto | Costo oculto | Uso |
|---|---|---|---|
| Antorcha | Miedo −10 | Lucidez +5 (la luz delata) | Entre niveles |
| Sal Consagrada | Corrupción −15 | Culpa +8 | Entre niveles (1 uso) |
| Vendas Viejas | HP +25 | — | Entre niveles (1 uso) |
| Fragmento de Espejo | Revela psique dominante | Miedo +5 (saber duele) | Entre niveles (1 uso) |
| Tinta del Abismo | Restaura 1 hechizo gastado | Corrupción +10 | En combate (Hechicero, 1 uso) |
| Sangre Seca | HP +15 | Culpa +5 por uso | Entre niveles (reutilizable) |
| Piedra de Eco | Próximo Defender garantizado | — | En combate (Guerrero, 1 uso) |
| Mapa Roto | Revela si el próximo nivel tiene enemigo secreto | — | Entre niveles (1 uso) |
| Elixir del Olvido | Borra 1 entrada del historial | Lucidez −10 | Entre niveles (1 uso) |

**Fuentes de ítems:** Cofre de Piedra (tier básico), Cofre de Eco (tier medio), Cofre del Umbral (tier alto), recompensa del Doble.

---

## 📦 Sistema de Cofres

| Cofre | Condición | Contenido | Aparece en |
|---|---|---|---|
| **Cofre de Piedra** | Tener la Llave de Piedra (cae en el nivel anterior) | Ítem tier básico | Level 2, 4, 8 |
| **Cofre de Eco** | Ganar las 3 rondas del combate anterior (2/3 no alcanza) | Ítem tier medio | Level 1, 3, 5, 7, 9 |
| **Cofre del Umbral** | Aliento ≥ 5 (1 por run) | Ítem tier alto + fragmento del ending | Level 6 |

---

## 🗺️ Estructura del Descenso

| Nivel | Nombre | Enemigo principal | Contenido especial |
|---|---|---|---|
| 1 | La Cueva del Origen | El Guardián de Piedra | Cofre de Eco — Llave de Piedra |
| 2 | El Espejo de las Formas | El Reflejo Armado | Callejón del Viajero — Cofre de Eco — Cofre de Piedra |
| 3 | El Ritual de la Entrega | El Sacerdote Sin Rostro | Laberinto (2 callejones) — Cofre de Eco — Llave de Piedra |
| 4 | El Rey de las Sombras | La Sombra Soberana | El Doble (NG+) — Cofre de Piedra |
| 5 | Las Moradas de los Muertos | — | El Otro (psique equilibrada) — La Voz del Umbral — Cofre de Eco |
| 6 | El Umbral Final | — | El Hambre (violencia acumulada) — Cofre del Umbral |
| 7 | La Sala del Juicio | El Eco | Laberinto (2 callejones) — Cofre de Eco — Llave de Piedra |
| 8 | El Río de Recuerdos | El Archivista | Cofre de Piedra |
| 9 | La Biblioteca del Olvido | La Grieta Viviente | Laberinto + Memoria como Moneda — Cofre de Eco — El Hambre (violencia extrema) |
| 10 | El Espejo Final | El Testigo + El Umbral Encarnado (boss) | Combate en dos fases — 5 rondas en el boss |

---

## ⚔️ Clases

| Clase | Stat principal | Recurso | Mecánica distintiva |
|---|---|---|---|
| Guerrero | Fuerza | Stamina 40 | Golpe Cargado (−15 ST), Furia Ciega (−20 ST, daño masivo), Contraataque Total tras 2 Defenders, Piedra de Eco |
| Hechicero | Mente | Magia 100 | 5 hechizos de un solo uso (10–40 MP), Tinta del Abismo para restaurar uno |
| Ladrón | Resistencia | Ingenio 70 | Setup "Observar" → Apuñalar/Estrangular; Huir para recuperar Ingenio; Improvisar sin energía |

### Hechizos del Hechicero

| Hechizo | Desbloqueado | Costo | Efecto |
|---|---|---|---|
| Palabra de Fuego | Nivel 1 | 15 MP | Daño alto directo |
| Velo de Sombra | Nivel 1 | 10 MP | Reduce daño enemigo esta ronda |
| Resonancia Mental | Nivel 1 | 10 MP | Ventaja en la siguiente tirada |
| Nombre Verdadero | Nivel 3 | 20 MP | Paraliza al enemigo una ronda |
| Fragmento del Abismo | Nivel 4 | 40 MP | Daño masivo, también te daña |

---

## 👹 Enemigos

### Enemigos regulares

| Enemigo | Nivel | Dificultad | Rasgo distintivo |
|---|---|---|---|
| El Guardián de Piedra | 1 | 4 | Introduce el sistema de combate |
| El Reflejo Armado | 2 | 5 | Devuelve el estilo de pelea del jugador |
| El Sacerdote Sin Rostro | 3 | 5 | Presencia psíquica, inmune a Nombre Verdadero |
| La Sombra Soberana | 4 | 6 | Acumula derrotas previas del jugador |
| El Eco | 7 | 6 | Repite acciones pasadas del jugador amplificadas |
| El Archivista | 8 | 6 | Ataca con memorias del historial |
| La Grieta Viviente | 9 | 7 | Sin forma, inmune a Nombre Verdadero |
| El Testigo | 10 | 7 | Solo observa; la observación hace daño psíquico |
| El Umbral Encarnado | 10 (boss) | 8 | 5 rondas, inmune a nombre y paralización |

### Enemigos secretos

| Enemigo | Condición de aparición | Nivel | Reward |
|---|---|---|---|
| **El Otro** | Todos los valores de psique dentro de un rango de 10 puntos | 5 | +2 Aliento — opción de fusión (ending secreto) |
| **El Hambre** | Furia + Apuñalar usados > 4 veces en el run | 6 y 9 | +20 HP máximo permanente |
| **El Doble** | New Game+ activo (psique heredada) | 4 | Ítem tier alto + fragmento de lore |

---

## 🤝 Aliados

Solo uno por run. Son mutuamente excluyentes.

| Aliado | Dónde encontrarlo | Condición | Efecto | Costo |
|---|---|---|---|---|
| **El Viajero Perdido** | Callejón de Level 2 | Aliento ≥ 3 | Ataque libre en Ronda 1 del próximo combate | 3 Aliento |
| **La Voz del Umbral** | Level 5 | Lucidez ≥ 30 | Revela el ending proyectado y el stat a cambiar | Culpa +10 |

---

## 🗝️ Laberintos

Los niveles 3, 7 y 9 tienen una **fase de exploración** previa al combate. Los callejones sin salida ofrecen:
- Lore sobre quienes pasaron antes
- Efectos de psique sin advertencia
- **+1 Aliento del Umbral** por cada callejón explorado

**Level 9** tiene además el evento **Memoria como Moneda**: un libro ofrece borrar una entrada del historial a cambio de +20 HP.

---

## 🔮 Sistema de Finales (15 endings)

El ending se determina al terminar Level 10 según la psique acumulada. Hay un ending secreto accesible desde Level 5.

### Ending secreto
| Ending | Condición |
|---|---|
| **La Fusión** | Fusionarse con El Otro tras derrotarlo en Level 5 |

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

### Finales por combinación doble (ambos ≥ 35)
| Ending | Condición |
|---|---|
| Suspensión | Miedo + Culpa |
| Ataque por Miedo | Violencia + Miedo |
| Cómplice Lúcido | Culpa + Lucidez |
| Sufrimiento Preciso | Miedo + Lucidez |
| Ciclo de Daño | Violencia + Culpa |
| Voluntad Pura | Corrupción + Lucidez |

Ningún final es explícitamente "bueno" o "malo".

---

## ⚔️ Sistema de Combate

- **3 rondas** por enemigo (5 para el boss final). Quien gana más rondas gana el combate.
- Mecánica de dados: **2d6 + stat vs dificultad × 2**. Con ventaja: 3d6 mejores 2.
- **Críticos**: superar el umbral por 4+ hace daño ×2.
- Los **enemigos se adaptan**: si repetís la misma acción dos veces seguidas, cambian de patrón.
- Cada enemigo tiene textos de ataque diferentes según tu clase.

### Bonificaciones de victoria
| Condición | Bonus |
|---|---|
| Ganar el combate | HP +5, Aliento +1 |
| Ganar 3/3 rondas | Cofre de Eco disponible |
| Ganar sin usar especiales | Energía +5 |
| Completar nivel sin Huir | Aliento +1 adicional |

### Acciones universales
| Acción | Efecto | Disponible cuando |
|---|---|---|
| **Respirar** | Energía +10, ronda neutral | Energía ≤ 30% |

---

## 🏗️ Estructura del Proyecto

```
descenso_al_umbral/
├── main.py              # Entrada — único archivo en la raíz
├── README.md
├── requirements.txt     # pygame>=2.1.0
├── test_game.py         # Suite de 96 tests automatizados
│
├── game/
│   ├── game_engine.py   # Director: loop principal, cofres, aliados, finales
│   ├── ui.py            # Pygame: render, typewriter, filtro psique, audio
│   ├── player.py        # Jugador: stats, psique, aliento, inventario, historial
│   ├── combat_system.py # Combate: dados, críticos, ítems, El Viajero
│   ├── enemies.py       # 9 enemigos + boss + 3 enemigos secretos
│   ├── menu.py          # Menú principal y créditos animados
│   ├── intro.py         # 5 pantallas de introducción narrativa
│   ├── save_system.py   # 3 slots de guardado + New Game+
│   └── levels/
│       ├── level1.py   →  La Cueva del Origen
│       ├── level2.py   →  El Espejo de las Formas (Viajero Perdido)
│       ├── level3.py   →  El Ritual de la Entrega (laberinto)
│       ├── level4.py   →  El Rey de las Sombras (El Doble NG+)
│       ├── level5.py   →  Las Moradas (El Otro, La Voz del Umbral)
│       ├── level6.py   →  El Umbral Final (El Hambre, Cofre del Umbral)
│       ├── level7.py   →  La Sala del Juicio (laberinto)
│       ├── level8.py   →  El Río de Recuerdos
│       ├── level9.py   →  La Biblioteca del Olvido (laberinto, Memoria)
│       └── level10.py  →  El Espejo Final (Testigo + boss Umbral Encarnado)
│
├── assets/              # 33 imágenes: niveles, enemigos, cofres, NPCs, retratos
├── fonts/               # Fuente gótica (Goth.ttf, Deutsch.ttf, Faith.ttf)
├── music/               # Música de fondo — sistema por nivel (nivel_N.mp3)
├── docs/                # Documentación de diseño y roadmap
└── saves/               # Slots de guardado (runtime, en .gitignore)
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

**Tests:**
```bash
python test_game.py
```

**Controles:**

| Tecla / Acción | Efecto |
|---|---|
| `ESPACIO` | Continuar pantalla narrativa / saltar typewriter |
| `1` `2` `3` `4` | Elegir opción |
| `↑` `↓` | Scroll de texto |
| `ESC` | Volver al menú (guarda automáticamente) |
| Clic izquierdo | Seleccionar opción / saltar typewriter |

---

## 🖥️ Tecnologías

- Python 3.11
- Pygame (gráficos, audio, input)
- JSON (sistema de guardado por slots)

---

## 🔮 Roadmap

- [ ] `assets/chest_eco.jpg` — imagen dedicada para el Cofre de Eco (actualmente usa el fondo del nivel)
- [ ] `assets/key_stone.jpg` — imagen visual al encontrar la Llave de Piedra
- [ ] Música diferente por nivel (renombrar archivos en `music/` a `nivel_N.mp3`)
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
