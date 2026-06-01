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


def crear_eco():
    """
    Nivel 7 — El Eco
    Dificultad: 6. Repite las palabras del jugador distorsionadas.
    Especialidad: presencia psíquica y ataques que reflejan lo que el
    jugador ya hizo en el combate.
    """
    return Enemy(
        nombre="El Eco",
        id_enemigo="eco",
        imagen="assets/enemy5.jpg",
        vida=95,
        dificultad=6,

        texto_intro="""
La Sala del Juicio no tiene jueces.

Solo un espacio vacío
y algo que repite lo que decís
antes de que lo digas.

El Eco.

No es una criatura.
Es lo que queda cuando
una mente repite demasiado
sus propias palabras.

No tiene intención.
Solo resonancia.


[ ESPACIO para continuar ]
""",

        textos_ataque={
            "default": {
                "Guerrero":  "Devuelve el sonido de tu armadura golpeando.\nComo si ya hubiera pasado.\nComo si ya lo supieras.",
                "Hechicero": "Las palabras de tu hechizo vuelven en eco.\nLigeramente distintas.\nSuficientemente distintas para dañar.",
                "Ladrón":    "Repite el sonido de tus pasos.\nDesde todos los ángulos a la vez.\nNo hay silencio donde esconderse.",
                "_":         "Lo que decís vuelve distorsionado.\nNi tuyo ni ajeno.\nSolo una versión peor de lo mismo.",
            },
            "presencia_psiquica": {
                "Guerrero":  "No te golpea.\nRepite cada derrota que tuviste en voz alta.\nCon tu propia voz.",
                "Hechicero": "No te golpea.\nRecita los hechizos que fallaron.\nUno por uno. En orden.",
                "Ladrón":    "No te golpea.\nRepite cada vez que te descubrieron.\nComo lista de evidencias.",
                "_":         "El eco de tus propias dudas\nvuelve amplificado.\nMás real que el original.",
            },
            "ataque_pesado": (
                "El Eco toma todo lo que dijiste\n"
                "y lo convierte en un solo golpe.\n"
                "El peso de tus propias palabras."
            ),
            "desesperado": (
                "Fragmentado, el Eco se multiplica.\n"
                "Ahora hay versiones de él\n"
                "repitiendo cosas que nunca dijiste.\n"
                "Pero que podrías haber dicho."
            ),
        },

        textos_derrota="""
El Eco se apaga.

No con un grito.
Con una pregunta sin respuesta.

El silencio que queda
es más honesto que cualquier cosa
que hayas dicho aquí.

Seguís.
""",

        textos_victoria="""
El Eco encontró algo tuyo
que no podías ignorar.

Lo repitió hasta que dolió.
Hasta que dejó de sonar como vos.

Seguís igual.
Pero con eso pegado adentro.
""",

        texto_empate="""
Tres rondas de resonancia mutua.

No ganaste.
No perdiste.

Solo aprendiste cómo sonás
desde afuera.

No es información que pediste.
""",

        psique_victoria_jugador={"lucidez": 8, "miedo": 3},
        psique_derrota_jugador={"miedo": 10, "culpa": 6},
    )


def crear_archivista():
    """
    Nivel 8 — El Archivista
    Dificultad: 6. Custodio de memorias. Ataca con recuerdos.
    Tiene texto diferenciado que alude al pasado de cada clase.
    """
    return Enemy(
        nombre="El Archivista",
        id_enemigo="archivista",
        imagen="assets/enemy6.jpg",
        vida=100,
        dificultad=6,

        texto_intro="""
El Río de Recuerdos tiene un custodio.

El Archivista.

Cientos de brazos.
Cada uno con un libro.
Cada libro con un nombre.
Uno de ellos es el tuyo.

No te ataca porque sea
tu enemigo.
Te ataca porque es su trabajo.

Todo lo que viviste
está registrado aquí.
Y él decide qué mostrarte.


[ ESPACIO para continuar ]
""",

        textos_ataque={
            "default": {
                "Guerrero":  "Abre un libro.\nLee en voz alta algo que hiciste.\nAlgo de lo que no estás orgulloso.",
                "Hechicero": "Abre un libro.\nLista cada vez que usaste el conocimiento\nde forma incorrecta.",
                "Ladrón":    "Abre un libro.\nNombra a alguien a quien le fallaste.\nCon nombre y fecha.",
                "_":         "Abre un libro.\nLee.\nLas palabras no necesitan ser nuevas para doler.",
            },
            "presencia_psiquica": {
                "Guerrero":  "No te golpea.\nSolo sostiene el libro abierto\nhasta que lo lees por tu cuenta.",
                "Hechicero": "No te golpea.\nPone el libro frente a vos\ny espera que lo tomes.",
                "Ladrón":    "No te golpea.\nCierra el libro.\nLo peor es no saber qué había adentro.",
                "_":         "No te golpea.\nSolo recuerda por vos.\nY eso es suficiente.",
            },
            "ataque_pesado": (
                "Todos los brazos al mismo tiempo.\n"
                "Todos los libros abiertos.\n"
                "Demasiado para procesar.\n"
                "Demasiado para negar."
            ),
            "desesperado": (
                "Los libros empiezan a quemarse.\n"
                "El Archivista no lo permite.\n"
                "Ataca con lo que puede salvar.\n"
                "Con lo más pesado."
            ),
        },

        textos_derrota="""
El Archivista cierra el libro.

No porque hayas ganado.
Sino porque llegaste a una página
que él no puede leer.

Eso te pertenece a vos.
Al menos eso.
""",

        textos_victoria="""
El libro sigue abierto.

El Archivista no necesita cerrarlo.
Ya lo tiene todo.

Seguís adelante
con menos de lo que creías tener
y más de lo que querías saber.
""",

        texto_empate="""
Tres rondas.
Ninguno cedió.

El Archivista te deja pasar
con una condición implícita:

Lo que está en el libro
ya no se puede deshacer.
""",

        psique_victoria_jugador={"lucidez": 10, "culpa": 4},
        psique_derrota_jugador={"culpa": 12, "miedo": 6},
    )


def crear_grieta():
    """
    Nivel 9 — La Grieta Viviente
    Dificultad: 7. No tiene forma. Es una fisura en la realidad.
    Inmune a Nombre Verdadero (no tiene nombre).
    Sus ataques son desorientadores, no físicos.
    """
    return Enemy(
        nombre="La Grieta Viviente",
        id_enemigo="grieta",
        imagen="assets/enemy7.jpg",
        vida=105,
        dificultad=7,

        texto_intro="""
No es un ser.

Es un lugar que decidió moverse.

La Grieta Viviente.

Una fisura en lo que debería ser
sólido e invariable.

Por ella se filtra algo
que no tiene nombre en ningún idioma.
No porque sea antiguo.
Sino porque nombrarlo
implicaría que existe.

Y si existe,
entonces vos también existís
dentro de algo que tiene grietas.


[ ESPACIO para continuar ]
""",

        textos_ataque={
            "default": {
                "Guerrero":  "La grieta se expande hacia vos.\nNo hay nada que golpear.\nSolo el borde afilado de lo que separa.",
                "Hechicero": "La grieta absorbe tu hechizo.\nNo lo rebota.\nSolo lo hace desaparecer.",
                "Ladrón":    "La grieta aparece donde ibas a estar.\nNo donde estás.\nAnticipación perfecta.",
                "_":         "La grieta se mueve.\nNo hacia vos.\nSino hacia donde vas a estar.",
            },
            "presencia_psiquica": {
                "Guerrero":  "No te toca.\nPero la grieta pasa cerca.\nY ves algo del otro lado.\nNo querés verlo.",
                "Hechicero": "No te toca.\nPero la grieta abre justo donde\nterminaba tu certeza.",
                "Ladrón":    "No te toca.\nSolo muestra el espacio entre\nlo que sos y lo que mostrás.",
                "_":         "La grieta se abre cerca.\nDel otro lado hay algo familiar.\nDemasiado familiar.",
            },
            "ataque_pesado": (
                "La grieta se expande.\n"
                "Por un instante, el mundo\n"
                "tiene un agujero con tu forma.\n"
                "Eso duele de una manera nueva."
            ),
            "desesperado": (
                "Fragmentada pero activa.\n"
                "Hay grietas más pequeñas ahora.\n"
                "Cada una moviéndose independiente.\n"
                "Todas hacia el mismo lugar."
            ),
        },

        textos_derrota="""
La grieta se cierra.

No desaparece.
Se vuelve invisible.

Sigue ahí.
En el mismo lugar.

Pero ya no se mueve.
Por ahora.
""",

        textos_victoria="""
La grieta no te venció.

Te demostró que el suelo
sobre el que caminabas
siempre tuvo fisuras.

Eso no es derrota.
Es geografía.

Igual duele.
""",

        texto_empate="""
Ninguno avanzó.
Ninguno cedió.

La grieta te deja pasar
por su propio centro.

No es victoria.
Es atravesar algo
sin entender qué era.
""",

        psique_victoria_jugador={"lucidez": 12, "corrupcion": 6},
        psique_derrota_jugador={"miedo": 14, "corrupcion": 5},
        inmunidades=["nombre"],
    )


def crear_testigo():
    """
    Nivel 10 — El Testigo
    Dificultad: 7. Juez silencioso. No ataca con fuerza, sino con
    observación que hace daño psíquico. Ataques basados en lo que
    vio del jugador durante todo el descenso.
    """
    return Enemy(
        nombre="El Testigo",
        id_enemigo="testigo",
        imagen="assets/enemy8.jpg",
        vida=110,
        dificultad=7,

        texto_intro="""
Al final de todo,
antes del Umbral mismo,
hay algo sentado.

El Testigo.

No pregunta.
No acusa.
No condena.

Solo mira.

Ha visto todo lo que hiciste
desde que entraste.
Cada decisión.
Cada omisión.
Cada momento en que elegiste
y cada momento en que no elegiste.

Lo sabe todo.
Y no va a decir nada.
Solo mirar.


[ ESPACIO para continuar ]
""",

        textos_ataque={
            "default": {
                "Guerrero":  "El Testigo no se mueve.\nSolo mira el momento en que usaste la fuerza\ncuando no era necesaria.",
                "Hechicero": "El Testigo no se mueve.\nSolo sostiene la mirada en el hechizo\nque lanzaste sin pensar en las consecuencias.",
                "Ladrón":    "El Testigo no se mueve.\nSolo observa el instante preciso\nen que elegiste el camino fácil.",
                "_":         "El Testigo no se mueve.\nSolo registra.\nY el registro pesa.",
            },
            "presencia_psiquica": {
                "Guerrero":  "No te toca.\nPero su mirada posa sobre algo que hiciste\nque preferirías que nadie viera.",
                "Hechicero": "No te toca.\nSolo inclina levemente la cabeza.\nComo si finalmente lo entendiera todo.",
                "Ladrón":    "No te toca.\nSolo señala, sin mover los brazos,\nel lugar exacto donde estás.",
                "_":         "No te toca.\nSu mirada es suficiente.\nSiempre lo fue.",
            },
            "ataque_pesado": (
                "El Testigo finalmente se mueve.\n"
                "Un paso.\n"
                "Solo un paso hacia vos.\n"
                "Y ese paso tiene el peso\n"
                "de todo lo que observó."
            ),
            "desesperado": (
                "La máscara de muchos ojos\n"
                "empieza a mostrar algo detrás.\n"
                "No querés saber qué es.\n"
                "Pero ya lo estás viendo."
            ),
        },

        textos_derrota="""
El Testigo baja la cabeza.

No en señal de derrota.
En señal de que terminó
de observar.

Tiene suficiente.

Lo que hará con esa información
es algo que nunca sabrás.
""",

        textos_victoria="""
El Testigo no se rinde.

No puede rendirse.
No es esa clase de cosa.

Simplemente… deja de mirar.

Y eso es peor.
Porque ya tiene todo lo que necesitaba.
""",

        texto_empate="""
Ninguno terminó lo que empezó.

El Testigo acumula sus observaciones.
Vos acumulás tus marcas.

Pasan.
Mutuamente saturados
de lo que cada uno es.
""",

        psique_victoria_jugador={"lucidez": 15, "culpa": 5},
        psique_derrota_jugador={"culpa": 15, "miedo": 8},
    )


def crear_umbral_encarnado():
    """
    BOSS — El Umbral Encarnado
    Dificultad: 8. El enemigo final. Tiene rondas_max=5.
    Inmune a paralización (no tiene nombre que nombrar,
    no tiene cuerpo que estrangular).
    """
    return Enemy(
        nombre="El Umbral Encarnado",
        id_enemigo="umbral",
        imagen="assets/enemy_boss.jpg",
        vida=160,
        dificultad=8,

        texto_intro="""
No llegaste al final del Umbral.

El Umbral llegó a vos.

El Umbral Encarnado.

Es una puerta.
Es un ser.
Es la suma de todo lo que
descendió antes que vos
y nunca salió.

Donde debería estar su cara
hay otra entrada.
Más profunda.
Más oscura.

No te pide que pases.
Solo existe.
Y eso es suficiente
para que todo cambie.


[ ESPACIO para continuar ]
""",

        textos_ataque={
            "default": {
                "Guerrero":  "El Umbral avanza.\nTu fuerza choca contra algo\nque no tiene resistencia porque no tiene límite.",
                "Hechicero": "El Umbral absorbe el hechizo.\nNo lo neutraliza.\nLo integra. Ahora es parte de él.",
                "Ladrón":    "El Umbral ya sabía dónde ibas.\nNo porque te leyera.\nSino porque es el lugar adonde van todos.",
                "_":         "El Umbral se mueve.\nNo hacia vos.\nSino alrededor.",
            },
            "presencia_psiquica": {
                "Guerrero":  "Sentís que la fuerza\nno tiene sentido aquí.\nNo porque seas débil.\nSino porque esto no es físico.",
                "Hechicero": "Sentís que el conocimiento\nque trajiste\nya no aplica.\nComo una llave en la cerradura equivocada.",
                "Ladrón":    "Sentís que no hay ángulo.\nNo hay sombra.\nNo hay posición.\nSolo esto.",
                "_":         "El Umbral te hace sentir\nque llegaste demasiado lejos.\nO no lo suficientemente lejos.",
            },
            "ataque_pesado": (
                "El Umbral se abre completamente.\n"
                "Por un instante, ves lo que hay del otro lado.\n"
                "El golpe viene de ahí.\n"
                "De algo que no debería poder golpear."
            ),
            "desesperado": (
                "Herido pero sin límite.\n"
                "El Umbral empieza a absorber\n"
                "todo lo que hay alrededor.\n"
                "Incluyendo partes de vos."
            ),
        },

        textos_derrota="""
El Umbral Encarnado retrocede.

No porque lo hayas vencido.
Sino porque reconoció algo en vos
que merece pasar.

No sabés qué es.
Nunca lo sabrás.

Pero algo en vos sí lo sabe.
Y eso es suficiente.
""",

        textos_victoria="""
El Umbral Encarnado no ganó.

Simplemente es.

Y vos sos menos de lo que eras
antes de enfrentarlo.

Eso tampoco es derrota.
Es el precio de llegar hasta aquí.

Pocos lo pagan.
""",

        texto_empate="""
Cinco rondas.
Ninguno terminó lo que empezó.

El Umbral te deja pasar
porque un empate con él
ya dice todo lo que necesita saber.

Entraste diferente.
Salís diferente.

El Umbral queda igual.
""",

        psique_victoria_jugador={"lucidez": 20, "corrupcion": 10},
        psique_derrota_jugador={"miedo": 15, "corrupcion": 10, "culpa": 5},
        inmunidades=["nombre", "paralizar"],
        rondas_max=5,
    )
