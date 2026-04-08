# 🜏 PROYECTO: Aventura de Texto Psicológica (Fantasia Oscura)

---

## 🧠 1. VISIÓN GENERAL

Este proyecto es un juego de aventura de texto con elementos visuales (a futuro), centrado en una experiencia psicológica y esotérica.

El jugador cree estar atravesando un calabozo para cumplir una misión heroica, pero en realidad está descendiendo en su propia psique.

El objetivo no es “ganar”, sino revelar la naturaleza interna del jugador.

---

## 🌑 2. FILOSOFÍA NARRATIVA

Inspiraciones principales:

- La oscuridad como origen (no como mal)
- La luz como ilusión o interrupción
- El conocimiento como fuerza corruptora
- El descenso como proceso de autodescubrimiento
- El enemigo final como reflejo del jugador

Principios clave:

- No hay decisiones correctas
- Toda elección revela algo del jugador
- El dungeon es una extensión de la mente
- El juego “observa” y responde

---

## 🧬 3. SISTEMAS PRINCIPALES

### 🔹 Sistema de Psique (oculto)

Variables internas del jugador:

- violencia
- miedo
- culpa
- lucidez
- corrupcion

Estas variables:
- NO son visibles directamente
- determinan eventos, muertes y finales

---

### 🔹 Stats visibles

- fuerza
- mente
- resistencia

Función:
- dar sensación de control al jugador
- pero NO son lo más importante

---

### 🔹 Sistema de decisiones

Cada nivel presenta:
- una situación narrativa
- 2–3 decisiones posibles

Cada decisión:
- modifica la psique
- puede causar muerte
- puede tener efectos acumulativos

---

### 🔹 Sistema de finales

Ejemplo:

- Alta corrupción → se convierte en entidad del dungeon
- Alta lucidez → sacrificio consciente
- Alto miedo → locura
- Otros → olvido

---

## 🏗️ 4. ARQUITECTURA DEL CÓDIGO

Estructura actual:
main.py
game_engine.py
player.py
levels/
init.py
level1.py
level2.py
level3.py

---

### 🔹 main.py
- Punto de entrada
- Ejecuta el juego

---

### 🔹 game_engine.py
Responsabilidades:
- Crear jugador
- Cargar niveles
- Controlar el loop principal
- Determinar el final

---

### 🔹 player.py
Contiene:
- nombre
- clase
- stats
- psique
- funciones de modificación

---

### 🔹 levels/

Cada nivel es una clase independiente con:
def jugar(self, player):
return "continuar" o "muerte"

Esto permite:
- escalabilidad
- modularidad
- facilidad para agregar contenido

---

## 🧩 5. NIVELES ACTUALES

---

### 🕯️ Level 1 — La Cueva del Origen

Concepto:
- Introducción a la oscuridad como estado natural

Decisiones:
- avanzar en la oscuridad
- usar luz
- llamar

Efecto:
- introduce sistema de psique
- rompe expectativas del jugador

---

### 🪞 Level 2 — El Espejo de las Formas

Concepto:
- confrontación con el yo

Decisiones:
- mirar
- romper
- evitar

Efecto:
- introduce culpa
- refleja decisiones pasadas

---

### 🜁 Level 3 — El Ritual de la Entrega

Concepto:
- sacrificio necesario para avanzar

Decisiones:
- sangre (cuerpo)
- recuerdo (mente)
- rechazo

Efecto:
- decisiones irreversibles
- primeras pérdidas reales
- aparición de entidad simbólica (el libro)

---

## 🔮 6. ROADMAP (PRÓXIMOS PASOS)

### Nivel 4
- Entidad tipo “Rey”
- revela deseos ocultos

### Nivel 5
- Sistema de muerte / destinos múltiples
- inspirado en diferentes “moradas”

### Nivel 6 (final)
- confrontación con el yo
- resolución final

---

## 🧠 7. REGLAS DE DISEÑO

Estas reglas NO deben romperse:

1. No hay elecciones “buenas”
2. Toda acción tiene costo
3. El jugador nunca tiene control total
4. El juego debe generar duda
5. El lenguaje puede volverse inestable
6. El sistema psicológico es más importante que el físico

---

## 🖥️ 8. FUTURO: INTERFAZ GRÁFICA

Objetivo:

Pantalla dividida:

| Imagen | Texto |
|--------|------|

Tecnología sugerida:
- pygame

Elementos:
- imágenes por nivel
- música ambiental
- efectos visuales según psique

---

## 🧠 9. DIRECCIÓN NARRATIVA

El tono debe ser:

- simbólico
- ambiguo
- introspectivo
- inquietante

Inspiración estilística:
- textos tipo versículos
- voz no confiable
- entidades que no se explican completamente

---

## ⚠️ 10. NOTAS IMPORTANTES

- El juego NO es sobre el dungeon → es sobre el jugador
- El sistema psicológico es el núcleo real
- La narrativa debe evolucionar con las decisiones

---

## 🚀 ESTADO ACTUAL

✔ Motor funcional  
✔ 3 niveles jugables  
✔ Sistema de psique activo  
✔ Múltiples caminos posibles  

El proyecto está listo para expansión de contenido.

---
---

# 📓 11. BITÁCORA DE DESARROLLO

---

## 🗓️ Fase 2 — Expansión Narrativa y Sistemas

### 🔹 Nuevos niveles implementados

Se agregaron tres niveles adicionales, completando la experiencia base del juego:

---

### 🜃 Level 4 — El Rey de las Sombras

- Introduce una entidad consciente dentro del dungeon
- El juego analiza la psique del jugador en tiempo real
- Se identifica el rasgo dominante (violencia, miedo, culpa, etc.)
- La entidad responde con diálogo personalizado

**Impacto:**
- El jugador percibe que el juego “lo entiende”
- Se rompe la separación entre jugador y sistema

---

### 🜄 Level 5 — Las Moradas de los Muertos

- Se introduce un sistema de destinos intermedios
- El jugador NO elige libremente → el sistema asigna una “morada”
- Se implementa distorsión del texto según estado psicológico

**Sistema de distorsión:**
- Miedo → texto fragmentado / espacios alterados
- Corrupción → caracteres deformados
- Lucidez → encapsulamiento críptico

**Impacto:**
- El lenguaje deja de ser confiable
- El juego refleja el estado mental del jugador

---

### 🜏 Level 6 — El Umbral Final

- Eliminación total de elementos externos (no hay entorno)
- Confrontación directa con la psique del jugador
- No hay enemigo físico → el jugador se enfrenta a sí mismo

**Decisiones finales:**
- Aceptar
- Negar
- Destruir

**Impacto:**
- Resolución filosófica del juego
- Define la inclinación del final, no el final en sí

---

## 🔹 Evolución del sistema narrativo

Se introduce un cambio clave:

- El juego deja de ser descriptivo
- El juego pasa a ser interpretativo

Ahora:
- analiza al jugador
- responde dinámicamente
- altera su propio lenguaje

---

## 🔹 Sistema de finales expandido

Se reemplaza el sistema simple por uno narrativo complejo.

### ✔ Se implementan 8 finales distintos:

1. Entidad del Abismo (alta corrupción)
2. Lucidez Total
3. Locura por Miedo
4. Autodestrucción
5. Culpa Eterna
6. Entidad Consciente (corrupción + lucidez)
7. Disolución
8. Olvido

**Características:**
- Basados en combinaciones de psique
- Narrativos (no descriptivos simples)
- Coherentes con todo el recorrido del jugador

---

## 🔹 Estado actual del proyecto

El juego ahora incluye:

✔ 6 niveles completos  
✔ Sistema psicológico funcional  
✔ Entidades narrativas  
✔ Distorsión dinámica del texto  
✔ Decisiones irreversibles  
✔ Sistema de finales avanzado  

---

## 🔹 Próximas direcciones posibles

### Opción A — Interfaz gráfica
- Implementación con pygame
- Pantalla dividida (imagen + texto)

### Opción B — Persistencia
- Guardado de partida
- Continuación de sesiones

### Opción C — Expansión narrativa
- Más niveles opcionales
- Rutas alternativas
- Eventos ocultos

### Opción D — Audio
- Música ambiental
- efectos sonoros dinámicos

---

## 🧠 Nota de diseño (crítica)

A partir de esta fase, el proyecto deja de ser:

“un juego de aventura”

y pasa a ser:

“una experiencia psicológica interactiva”

Esto debe guiar todas las decisiones futuras.

---