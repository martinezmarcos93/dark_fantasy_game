from game.combat_system import Enemy

# ═══════════════════════════════════════════════════════════════
# ENEMIES — Descenso al Umbral
#
# Cada enemigo define:
#   - Sus textos de ataque por situación
#   - Textos de victoria/derrota/empate para el cierre narrativo
#   - Modificadores de psique según resultado
# ═══════════════════════════════════════════════════════════════


def crear_guardian():
    """
    Nivel 1 — El Guardián de Piedra
    Dificultad: 4. Patrón simple, introduce al jugador al sistema.
    Enemigo físico puro. No tiene presencia psíquica.
    """
    return Enemy(
        nombre="El Guardián de Piedra",
        id_enemigo="guardian",
        imagen="assets/enemy1.jpg",
        vida=80,
        dificultad=4,

        texto_intro="""
Antes de que la oscuridad te reciba…
algo la bloquea.

El Guardián de Piedra.

No fue puesto aquí por nadie.
Creció solo.
Del mismo material que la cueva.
De la misma necesidad de no dejar pasar.

No tiene ojos.
Pero te ve.


[ ESPACIO para continuar ]
""",

        textos_ataque={
            "default": {
                "Guerrero":  "Un brazo de piedra avanza.\nSabés que viene. No podés detenerlo.\nSolo aguantar.",
                "Hechicero": "La piedra no entiende de hechizos.\nAvanza igual.\nTu magia no cambia su peso.",
                "Ladrón":    "Un brazo de piedra avanza.\nLento. Inevitable.\nNo hay ángulo que esquivar.",
                "_":         "Un brazo de piedra avanza.\nLento. Inevitable.\nSin intención de parar.",
            },
            "ataque_pesado": {
                "Guerrero":  "Levanta ambos brazos.\nReconocés el movimiento.\nNo es suficiente para bloquearlo.",
                "Hechicero": "Levanta ambos brazos.\nEl impacto viene antes de que puedas canalizar nada.",
                "Ladrón":    "Levanta ambos brazos.\nEl suelo tiembla. No hay sombra donde esconderse.",
                "_":         "Levanta ambos brazos.\nEl suelo tiembla antes del impacto.\nNo hay dónde cubrirse.",
            },
            "detectar_sigilo": (
                "La piedra vibra.\n"
                "Algo en ella percibió tu presencia antes de que te movieras.\n"
                "Te encuentra aunque no te vea."
            ),
            "desesperado": (
                "Fracturado pero en pie.\n"
                "Golpea con lo que le queda.\n"
                "Sin cálculo. Solo peso."
            ),
        },

        textos_derrota="""
La piedra cede.

No con un grito.
No con un colapso dramático.
Solo se detiene.

Como si alguien hubiera apagado
la única instrucción que tenía.

El camino está libre.
Pero la cueva notó que pasaste.
""",

        textos_victoria="""
No pudiste derribarlo.

Pero tampoco te mató.
O eso creés.

El guardián retrocedió un paso.
Solo uno.
Como si hubiera evaluado
cuánto quedaba de vos
y decidido que no valía la pena terminar.

Seguís adelante.
Con menos de lo que tenías.
""",

        texto_empate="""
Ninguno derribó al otro.

Tres rondas.
Daño en ambas direcciones.
Y al final… un impasse.

El guardián te deja pasar.
No por derrota.
Por algo parecido al reconocimiento.

Eso también tiene un precio.
""",

        psique_victoria_jugador={"lucidez": 5},
        psique_derrota_jugador={"miedo": 8},
    )


def crear_reflejo():
    """
    Nivel 2 — El Reflejo Armado
    Dificultad: 5. Copia los patrones del jugador.
    Tiene respuesta específica al hechicero (amplifica hechizos).
    """
    return Enemy(
        nombre="El Reflejo Armado",
        id_enemigo="reflejo",
        imagen="assets/enemy2.jpg",
        vida=90,
        dificultad=5,

        texto_intro="""
Antes de llegar al espejo…
el espejo viene a vos.

El Reflejo Armado.

Tiene tu cara.
Tu postura.
Tus movimientos, un instante antes de que los hagas.

No es un eco.
Es una anticipación.

Y viene hacia vos.


[ ESPACIO para continuar ]
""",

        textos_ataque={
            "default": {
                "Guerrero":  "Devuelve tu golpe.\nMisma fuerza.\nMejor posición.",
                "Hechicero": "Refleja tu hechizo.\nSabe la frecuencia.\nLo aprendió mientras lo lanzabas.",
                "Ladrón":    "Estaba donde ibas.\nNo donde estabas.\nTe conoce mejor que vos.",
                "_":         "Te devuelve lo que le diste.\nMismo movimiento.\nMejor ejecutado.",
            },
            "ataque_pesado": {
                "Guerrero":  "Copió tu golpe cargado.\nY lo ejecutó más rápido.\nComo si hubiera esperado esta ronda.",
                "Hechicero": "Tomó prestada tu magia.\nLa devuelve amplificada.\nCon tu misma voz.",
                "Ladrón":    "Ya estaba en tu espalda.\nAntes de que lo pensaras.\nTu táctica favorita, usada contra vos.",
                "_":         "Aprendió de tus últimas rondas.\nEl golpe que viene es una versión mejorada tuya.",
            },
            "detectar_sigilo": (
                "El reflejo no necesita verte.\n"
                "Sabe adónde vas porque ya fue ahí antes.\n"
                "Tu posición queda expuesta."
            ),
            "desesperado": (
                "Fragmentado pero presente.\n"
                "Cada pedazo del reflejo sigue copiándote.\n"
                "Ahora hay más de uno."
            ),
        },

        textos_derrota="""
El reflejo se fragmenta.

No desaparece.
Se quiebra en pedazos más pequeños
que siguen teniendo tu cara.

Pero ya no se mueven.

Pasás entre los fragmentos.
Sin mirarte en ninguno.
Eso también es una decisión.
""",

        textos_victoria="""
Te copió demasiado bien.

Cada intento tuyo, anticipado.
Cada golpe, devuelto con interés.

No estás muerto.
Pero el reflejo te mostró algo
que preferirías no haber visto:

Lo que hacés cuando te desesperás.
Y no es bonito.
""",

        texto_empate="""
Ninguno pudo con el otro.

Tenía sentido.
Era vos.

Al final, el reflejo da un paso atrás.
No porque perdió.
Porque entendió que empatar con vos
ya es ganar.

Seguís. Con esa idea pegada.
""",

        psique_victoria_jugador={"lucidez": 8},
        psique_derrota_jugador={"miedo": 10, "culpa": 5},
    )


def crear_sacerdote():
    """
    Nivel 3 — El Sacerdote Sin Rostro
    Dificultad: 5. Usa presencia psíquica además de daño físico.
    INMUNE a Nombre Verdadero — no tiene nombre que nombrar.
    """
    return Enemy(
        nombre="El Sacerdote Sin Rostro",
        id_enemigo="sacerdote",
        imagen="assets/enemy3.jpg",
        vida=85,
        dificultad=5,

        texto_intro="""
El altar no estaba vacío.

El Sacerdote Sin Rostro lo custodia.

No tiene facciones.
Solo una superficie lisa donde debería haber una cara.
Como si algo hubiera borrado todo
antes de que pudiera formarse.

No ataca.
Pero tampoco deja pasar.
Extiende las manos.
Y el aire se vuelve espeso.


[ ESPACIO para continuar ]
""",

        textos_ataque={
            "default": {
                "Guerrero":  "Las manos se extienden.\nTu fuerza no sirve aquí.\nNo hay nada que golpear.",
                "Hechicero": "Las manos se extienden.\nSaben tu nombre arcano.\nSe lo llevan antes de que lo digas.",
                "Ladrón":    "Las manos se extienden.\nNo buscan tu cuerpo.\nBuscan lo que ocultás.",
                "_":         "Las manos sin dedos se extienden hacia vos.\nNo es un golpe.\nEs una extracción.",
            },
            "presencia_psiquica": {
                "Guerrero":  "No te golpea.\nTe hace dudar de cada golpe que diste.\n¿Para qué?",
                "Hechicero": "No te golpea.\nEntra en la frecuencia de tu magia.\nLa enturbia.",
                "Ladrón":    "No te golpea.\nHace que tu posición se sienta expuesta.\nAunque no estés visible.",
                "_":         "No te toca.\nPero algo en el aire cambia.\nUna presión que viene de adentro.",
            },
            "ataque_pesado": (
                "El aire espeso se condensa.\n"
                "Una ola de nada que pesa como todo.\n"
                "Golpea antes de que puedas nombrarlo."
            ),
            "detectar_sigilo": (
                "No tiene ojos.\n"
                "Pero siente la intención antes de que se materialice.\n"
                "Tu sigilo se deshace en el aire espeso."
            ),
            "desesperado": (
                "La superficie lisa donde debería haber un rostro\n"
                "comienza a mostrar algo.\n"
                "No querés verlo.\n"
                "Pero ya es tarde."
            ),
        },

        textos_derrota="""
El Sacerdote baja las manos.

No cayó.
No huyó.
Simplemente… dejó de interponerse.

Como si hubiera obtenido
lo que vino a obtener.

Eso no te da alivio.
Te da otra pregunta.
""",

        textos_victoria="""
Tomó algo de vos.

No sabés qué.
No hay herida visible.
No hay memoria de cuándo ocurrió.

Solo la certeza de que
salís con menos
de lo que entraste.

Y que lo que falta
no va a volver.
""",

        texto_empate="""
Tres rondas de extracción mutua.

Vos intentaste nombrarlo.
Él intentó vaciarte.

Ninguno terminó lo que empezó.

El sacerdote se hace a un lado.
La superficie donde debería estar su cara
no revela nada.

Nunca lo hizo.
""",

        psique_victoria_jugador={"lucidez": 5, "corrupcion": 5},
        psique_derrota_jugador={"culpa": 10, "miedo": 5},
    )


def crear_sombra():
    """
    Nivel 4 — La Sombra Soberana
    Dificultad: 6. El más difícil. Acumula las derrotas anteriores.
    Tiene el mayor repertorio de respuestas.
    """
    return Enemy(
        nombre="La Sombra Soberana",
        id_enemigo="sombra",
        imagen="assets/enemy4.jpg",
        vida=110,
        dificultad=6,

        texto_intro="""
Antes de que llegues a la grieta…
ella ya está ahí.

La Sombra Soberana.

No es tu sombra.
Es la de todos los que descendieron antes que vos
y no pudieron continuar.

Las absorbió.
Las hizo suyas.
Y ahora tiene el peso
de todas esas derrotas acumuladas.

Te mira.
Te conoce.
Sabe exactamente cuánto podés aguantar.


[ ESPACIO para continuar ]
""",

        textos_ataque={
            "default": {
                "Guerrero":  "La sombra adopta tu postura de combate.\nCada golpe que planeás, ella lo anticipa.\nTu fuerza es también la suya.",
                "Hechicero": "La sombra absorbe la resonancia de tus hechizos.\nY los convierte en presión.\nContra vos.",
                "Ladrón":    "La sombra ya estaba en tu posición de escape.\nTe esperaba ahí.\nNo hay ángulo tuyo que no conozca.",
                "_":         "La sombra cambia de forma.\nCada cambio, un golpe desde un ángulo distinto.\nComo si supiera cuál lado no cubrís.",
            },
            "presencia_psiquica": {
                "Guerrero":  "Se acerca.\nRecordás cada vez que la fuerza no alcanzó.\nEso pesa más que el golpe.",
                "Hechicero": "Se acerca.\nSusurra los nombres de los hechizos que fallaron.\nEn tu voz.",
                "Ladrón":    "Se acerca.\nY en ese momento sabés:\nnunca estuviste realmente escondido.",
                "_":         "No te toca.\nSe acerca lo suficiente para que la sientas.\nFrío. Reconocimiento.",
            },
            "ataque_pesado": (
                "Todas las derrotas que absorbió\n"
                "se concentran en un solo movimiento.\n"
                "El peso de todo lo que falló antes que vos."
            ),
            "detectar_sigilo": (
                "La sombra no necesita verte.\n"
                "Vos sos parte de ella desde que empezaste a descender.\n"
                "No hay posición que no conozca."
            ),
            "desesperado": (
                "Herida pero no derrotada.\n"
                "Las sombras absorbidas empiezan a salir.\n"
                "Fragmentos de otras personas.\n"
                "Todas atacando con vos en mente."
            ),
        },

        textos_derrota="""
La sombra se aplana.

No desaparece.
Nunca va a desaparecer.
Pero deja de tener volumen.

Se queda en el suelo,
donde siempre debería haber estado.

Pasás sobre ella.
Y ella te deja pasar.

Eso es lo más extraño de todo.
""",

        textos_victoria="""
Te conocía demasiado bien.

Cada movimiento tuyo, anticipado.
Cada derrota que tuviste en los niveles anteriores,
ya estaba en ella.

La sombra no se regodea.
Solo existe.

Seguís adelante.
Pero ahora sabés que
ella también sigue.
Adentro.
""",

        texto_empate="""
Tres rondas contra vos mismo.

Al final, la sombra da un paso atrás.
No porque la hayas vencido.
Sino porque un empate con ella
ya dice demasiado sobre vos.

Lo que sos y lo que nega.
Lo que avanzás y lo que arrastrás.

La grieta está adelante.
La sombra se queda atrás.
Por ahora.
""",

        psique_victoria_jugador={"lucidez": 10, "corrupcion": 5},
        psique_derrota_jugador={"miedo": 12, "violencia": 8},
    )
