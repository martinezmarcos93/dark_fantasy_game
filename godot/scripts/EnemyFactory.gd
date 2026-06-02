## EnemyFactory — crea instancias de Enemy con todos sus textos.
## Port directo de enemies.py. Textos sagrados — no modificar.
## Uso: var e := EnemyFactory.crear_guardian()

class_name EnemyFactory


static func _nuevo(
	nombre: String, id: String, imagen: String, vida: int, dif: int,
	intro: String, ataques: Dictionary,
	derrota: String, victoria: String, empate: String,
	pv: Dictionary, pd: Dictionary,
	inmunes: Array = [], rondas: int = 3
) -> Enemy:
	var e := Enemy.new()
	e.inicializar(nombre, id, imagen, vida, dif, intro, ataques,
	              derrota, victoria, empate, pv, pd, inmunes, rondas)
	return e


# ═══════════════════════════════════════════════════════════════
# NIVEL 1 — El Guardián de Piedra
# ═══════════════════════════════════════════════════════════════
static func crear_guardian() -> Enemy:
	return _nuevo(
		"El Guardián de Piedra", "guardian", "res://assets/images/enemy1.jpg",
		80, 4,
		"""
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
		{
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
			"detectar_sigilo": "La piedra vibra.\nAlgo en ella percibió tu presencia antes de que te movieras.\nTe encuentra aunque no te vea.",
			"desesperado": "Fracturado pero en pie.\nGolpea con lo que le queda.\nSin cálculo. Solo peso.",
		},
		"""
La piedra cede.

No con un grito.
No con un colapso dramático.
Solo se detiene.

Como si alguien hubiera apagado
la única instrucción que tenía.

El camino está libre.
Pero la cueva notó que pasaste.
""",
		"""
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
		"""
Ninguno derribó al otro.

Tres rondas.
Daño en ambas direcciones.
Y al final… un impasse.

El guardián te deja pasar.
No por derrota.
Por algo parecido al reconocimiento.

Eso también tiene un precio.
""",
		{"lucidez": 5}, {"miedo": 8}
	)


# ═══════════════════════════════════════════════════════════════
# NIVEL 2 — El Reflejo Armado
# ═══════════════════════════════════════════════════════════════
static func crear_reflejo() -> Enemy:
	return _nuevo(
		"El Reflejo Armado", "reflejo", "res://assets/images/enemy2.jpg",
		90, 5,
		"""
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
		{
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
			"detectar_sigilo": "El reflejo no necesita verte.\nSabe adónde vas porque ya fue ahí antes.\nTu posición queda expuesta.",
			"desesperado": "Fragmentado pero presente.\nCada pedazo del reflejo sigue copiándote.\nAhora hay más de uno.",
		},
		"""
El reflejo se fragmenta.

No desaparece.
Se quiebra en pedazos más pequeños
que siguen teniendo tu cara.

Pero ya no se mueven.

Pasás entre los fragmentos.
Sin mirarte en ninguno.
Eso también es una decisión.
""",
		"""
Te copió demasiado bien.

Cada intento tuyo, anticipado.
Cada golpe, devuelto con interés.

No estás muerto.
Pero el reflejo te mostró algo
que preferirías no haber visto:

Lo que hacés cuando te desesperás.
Y no es bonito.
""",
		"""
Ninguno pudo con el otro.

Tenía sentido.
Era vos.

Al final, el reflejo da un paso atrás.
No porque perdió.
Porque entendió que empatar con vos
ya es ganar.

Seguís. Con esa idea pegada.
""",
		{"lucidez": 8}, {"miedo": 10, "culpa": 5}
	)


# ═══════════════════════════════════════════════════════════════
# NIVEL 3 — El Sacerdote Sin Rostro
# ═══════════════════════════════════════════════════════════════
static func crear_sacerdote() -> Enemy:
	return _nuevo(
		"El Sacerdote Sin Rostro", "sacerdote", "res://assets/images/enemy3.jpg",
		85, 5,
		"""
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
		{
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
			"ataque_pesado": "El aire espeso se condensa.\nUna ola de nada que pesa como todo.\nGolpea antes de que puedas nombrarlo.",
			"detectar_sigilo": "No tiene ojos.\nPero siente la intención antes de que se materialice.\nTu sigilo se deshace en el aire espeso.",
			"desesperado": "La superficie lisa donde debería haber un rostro\ncomienza a mostrar algo.\nNo querés verlo.\nPero ya es tarde.",
		},
		"""
El Sacerdote baja las manos.

No cayó.
No huyó.
Simplemente… dejó de interponerse.

Como si hubiera obtenido
lo que vino a obtener.

Eso no te da alivio.
Te da otra pregunta.
""",
		"""
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
		"""
Tres rondas de extracción mutua.

Vos intentaste nombrarlo.
Él intentó vaciarte.

Ninguno terminó lo que empezó.

El sacerdote se hace a un lado.
La superficie donde debería estar su cara
no revela nada.

Nunca lo hizo.
""",
		{"lucidez": 5, "corrupcion": 5}, {"culpa": 10, "miedo": 5}
	)


# ═══════════════════════════════════════════════════════════════
# NIVEL 4 — La Sombra Soberana
# ═══════════════════════════════════════════════════════════════
static func crear_sombra() -> Enemy:
	return _nuevo(
		"La Sombra Soberana", "sombra", "res://assets/images/enemy4.jpg",
		110, 6,
		"""
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
		{
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
			"ataque_pesado": "Todas las derrotas que absorbió\nse concentran en un solo movimiento.\nEl peso de todo lo que falló antes que vos.",
			"detectar_sigilo": "La sombra no necesita verte.\nVos sos parte de ella desde que empezaste a descender.\nNo hay posición que no conozca.",
			"desesperado": "Herida pero no derrotada.\nLas sombras absorbidas empiezan a salir.\nFragmentos de otras personas.\nTodas atacando con vos en mente.",
		},
		"""
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
		"""
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
		"""
Tres rondas contra vos mismo.

Al final, la sombra da un paso atrás.
No porque la hayas vencido.
Sino porque un empate con ella
ya dice demasiado sobre vos.

Lo que sos y lo que negás.
Lo que avanzás y lo que arrastrás.

La grieta está adelante.
La sombra se queda atrás.
Por ahora.
""",
		{"lucidez": 10, "corrupcion": 5}, {"miedo": 12, "violencia": 8}
	)


# ═══════════════════════════════════════════════════════════════
# NIVEL 7 — El Eco
# ═══════════════════════════════════════════════════════════════
static func crear_eco() -> Enemy:
	return _nuevo(
		"El Eco", "eco", "res://assets/images/enemy5.jpg",
		95, 6,
		"""
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
		{
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
			"ataque_pesado": "El Eco toma todo lo que dijiste\ny lo convierte en un solo golpe.\nEl peso de tus propias palabras.",
			"desesperado": "Fragmentado, el Eco se multiplica.\nAhora hay versiones de él\nrepitiendo cosas que nunca dijiste.\nPero que podrías haber dicho.",
		},
		"""
El Eco se apaga.

No con un grito.
Con una pregunta sin respuesta.

El silencio que queda
es más honesto que cualquier cosa
que hayas dicho aquí.

Seguís.
""",
		"""
El Eco encontró algo tuyo
que no podías ignorar.

Lo repitió hasta que dolió.
Hasta que dejó de sonar como vos.

Seguís igual.
Pero con eso pegado adentro.
""",
		"""
Tres rondas de resonancia mutua.

No ganaste.
No perdiste.

Solo aprendiste cómo sonás
desde afuera.

No es información que pediste.
""",
		{"lucidez": 8, "miedo": 3}, {"miedo": 10, "culpa": 6}
	)


# ═══════════════════════════════════════════════════════════════
# NIVEL 8 — El Archivista
# ═══════════════════════════════════════════════════════════════
static func crear_archivista() -> Enemy:
	return _nuevo(
		"El Archivista", "archivista", "res://assets/images/enemy6.jpg",
		100, 6,
		"""
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
		{
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
			"ataque_pesado": "Todos los brazos al mismo tiempo.\nTodos los libros abiertos.\nDemasiado para procesar.\nDemasiado para negar.",
			"desesperado": "Los libros empiezan a quemarse.\nEl Archivista no lo permite.\nAtaca con lo que puede salvar.\nCon lo más pesado.",
		},
		"""
El Archivista cierra el libro.

No porque hayas ganado.
Sino porque llegaste a una página
que él no puede leer.

Eso te pertenece a vos.
Al menos eso.
""",
		"""
El libro sigue abierto.

El Archivista no necesita cerrarlo.
Ya lo tiene todo.

Seguís adelante
con menos de lo que creías tener
y más de lo que querías saber.
""",
		"""
Tres rondas.
Ninguno cedió.

El Archivista te deja pasar
con una condición implícita:

Lo que está en el libro
ya no se puede deshacer.
""",
		{"lucidez": 10, "culpa": 4}, {"culpa": 12, "miedo": 6}
	)


# ═══════════════════════════════════════════════════════════════
# NIVEL 9 — La Grieta Viviente
# ═══════════════════════════════════════════════════════════════
static func crear_grieta() -> Enemy:
	return _nuevo(
		"La Grieta Viviente", "grieta", "res://assets/images/enemy7.jpg",
		105, 7,
		"""
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
		{
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
			"ataque_pesado": "La grieta se expande.\nPor un instante, el mundo\ntiene un agujero con tu forma.\nEso duele de una manera nueva.",
			"desesperado": "Fragmentada pero activa.\nHay grietas más pequeñas ahora.\nCada una moviéndose independiente.\nTodas hacia el mismo lugar.",
		},
		"""
La grieta se cierra.

No desaparece.
Se vuelve invisible.

Sigue ahí.
En el mismo lugar.

Pero ya no se mueve.
Por ahora.
""",
		"""
La grieta no te venció.

Te demostró que el suelo
sobre el que caminabas
siempre tuvo fisuras.

Eso no es derrota.
Es geografía.

Igual duele.
""",
		"""
Ninguno avanzó.
Ninguno cedió.

La grieta te deja pasar
por su propio centro.

No es victoria.
Es atravesar algo
sin entender qué era.
""",
		{"lucidez": 12, "corrupcion": 6}, {"miedo": 14, "corrupcion": 5},
		["nombre"]
	)


# ═══════════════════════════════════════════════════════════════
# NIVEL 10 — El Testigo
# ═══════════════════════════════════════════════════════════════
static func crear_testigo() -> Enemy:
	return _nuevo(
		"El Testigo", "testigo", "res://assets/images/enemy8.jpg",
		110, 7,
		"""
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
		{
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
			"ataque_pesado": "El Testigo finalmente se mueve.\nUn paso.\nSolo un paso hacia vos.\nY ese paso tiene el peso\nde todo lo que observó.",
			"desesperado": "La máscara de muchos ojos\nempieza a mostrar algo detrás.\nNo querés saber qué es.\nPero ya lo estás viendo.",
		},
		"""
El Testigo baja la cabeza.

No en señal de derrota.
En señal de que terminó
de observar.

Tiene suficiente.

Lo que hará con esa información
es algo que nunca sabrás.
""",
		"""
El Testigo no se rinde.

No puede rendirse.
No es esa clase de cosa.

Simplemente… deja de mirar.

Y eso es peor.
Porque ya tiene todo lo que necesitaba.
""",
		"""
Ninguno terminó lo que empezó.

El Testigo acumula sus observaciones.
Vos acumulás tus marcas.

Pasan.
Mutuamente saturados
de lo que cada uno es.
""",
		{"lucidez": 15, "culpa": 5}, {"culpa": 15, "miedo": 8}
	)


# ═══════════════════════════════════════════════════════════════
# BOSS — El Umbral Encarnado
# ═══════════════════════════════════════════════════════════════
static func crear_umbral_encarnado() -> Enemy:
	return _nuevo(
		"El Umbral Encarnado", "umbral", "res://assets/images/enemy_boss.jpg",
		160, 8,
		"""
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
		{
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
			"ataque_pesado": "El Umbral se abre completamente.\nPor un instante, ves lo que hay del otro lado.\nEl golpe viene de ahí.\nDe algo que no debería poder golpear.",
			"desesperado": "Herido pero sin límite.\nEl Umbral empieza a absorber\ntodo lo que hay alrededor.\nIncluyendo partes de vos.",
		},
		"""
El Umbral Encarnado retrocede.

No porque lo hayas vencido.
Sino porque reconoció algo en vos
que merece pasar.

No sabés qué es.
Nunca lo sabrás.

Pero algo en vos sí lo sabe.
Y eso es suficiente.
""",
		"""
El Umbral Encarnado no ganó.

Simplemente es.

Y vos sos menos de lo que eras
antes de enfrentarlo.

Eso tampoco es derrota.
Es el precio de llegar hasta aquí.

Pocos lo pagan.
""",
		"""
Cinco rondas.
Ninguno terminó lo que empezó.

El Umbral te deja pasar
porque un empate con él
ya dice todo lo que necesita saber.

Entraste diferente.
Salís diferente.

El Umbral queda igual.
""",
		{"lucidez": 20, "corrupcion": 10}, {"miedo": 15, "corrupcion": 10, "culpa": 5},
		["nombre", "paralizar"], 5
	)


# ═══════════════════════════════════════════════════════════════
# ENEMIGOS SECRETOS
# ═══════════════════════════════════════════════════════════════
static func crear_otro() -> Enemy:
	return _nuevo(
		"El Otro", "otro", "res://assets/images/enemy_otro.jpg",
		100, 7,
		"""
No te esperabas esto.

El Otro.

No es un enemigo.
No es un aliado.
Es lo que ocurre cuando
todas las partes de vos
están, por primera vez,
en el mismo lugar al mismo tiempo.

Perfectamente equilibrado.
Igual de incómodo.

Te mira.
Sos vos.
Y también es todo lo demás.


[ ESPACIO para continuar ]
""",
		{
			"default": {
				"Guerrero":  "El Otro adopta tu postura.\nSin drama. Sin anticipación.\nEs simplemente tan fuerte como vos.",
				"Hechicero": "El Otro levanta la mano.\nNo conjura nada nuevo.\nUsa exactamente lo que sabés vos.",
				"Ladrón":    "El Otro ya estaba en tu posición.\nNo como amenaza.\nComo espejo.",
				"_":         "El Otro avanza.\nCon la misma calma con que vos llegaste hasta acá.",
			},
			"ataque_pesado": {
				"Guerrero":  "Golpea con tu fuerza máxima.\nLa que no sabías que tenías.\nLa que él sí sabía.",
				"Hechicero": "Combina todos tus hechizos en un solo movimiento.\nSin costo.\nSin grieta.",
				"Ladrón":    "Estaba en todos tus puntos ciegos al mismo tiempo.\nNo porque sea mejor.\nSino porque es la versión completa.",
				"_":         "Un golpe que no tiene nombre.\nTuyo y no tuyo a la vez.",
			},
			"desesperado": "Dañado pero simétrico.\nEl Otro no entra en pánico.\nNo tiene pánico.\nSolo la serenidad de lo que es completo.",
		},
		"""
El Otro da un paso atrás.

No cayó.
No huyó.

Simplemente...
ya no está en tu camino.

Sigue existiendo.
En algún lugar sin nombre
dentro de vos.

Eso no va a cambiar.
""",
		"""
El Otro no ganó nada con esto.

Ya lo tenía todo.

Lo que te falta...
no se pierde cuando perdés una pelea.

Solo se nota más.
""",
		"""
Ninguno pudo con el otro.

Tenía sentido.

En el equilibrio exacto...
ninguna fuerza puede prevalecer.

El Otro se hace a un lado.
No porque hayas ganado.
Sino porque el empate ya dijo todo.
""",
		{"lucidez": 15}, {"miedo": 8, "culpa": 5}
	)


static func crear_hambre() -> Enemy:
	return _nuevo(
		"El Hambre", "hambre", "res://assets/images/enemy_hambre.jpg",
		130, 9,
		"""
Sin aviso.
Sin introducción.
Sin texto que lo anuncie.

El Hambre ya estaba acá
cuando llegaste.

No tiene forma.
Solo bordes.
Solo la certeza
de que consume
sin pausa
sin razón
sin fin.

No vino por vos.
Vino porque lo llamaste.


[ ESPACIO para continuar ]
""",
		{
			"default": {
				"Guerrero":  "No tiene técnica.\nTiene impulso.\nEl mismo que usaste vos.\nSolo más.",
				"Hechicero": "No absorbe el hechizo.\nLo ignora.\nY avanza igual.",
				"Ladrón":    "No estaba donde ibas.\nEstaba en todos lados.\nNo hay posición que lo evite.",
				"_":         "Se mueve sin dirección.\nSin plan.\nSolo el movimiento del que no puede detenerse.",
			},
			"ataque_pesado": {
				"Guerrero":  "Todo el peso del impulso acumulado.\nToda la violencia que invocaste.\nDevuelta de una vez.",
				"Hechicero": "Una presión que no tiene nombre en ningún hechizo.\nAnterior a las palabras.",
				"Ladrón":    "No hay ángulo.\nNo hay sombra.\nSolo el hambre que llenás cuando atacás.",
				"_":         "El peso de todo lo que consumiste\nconvertido en un solo movimiento.",
			},
			"desesperado": "Herido, el Hambre se intensifica.\nDaño lo vuelve más urgente.\nNo más débil.\nSolo más hambriento.",
		},
		"""
El Hambre no desaparece.

No puede desaparecer.
Pero retrocede.

No porque lo hayas vencido.
Sino porque, por ahora,
está satisfecho.

Con lo que hiciste.
Con lo que costó.

Eso es tuyo.
""",
		"""
No te venció.

El Hambre nunca vence.
Solo acumula.

Lo que acumuló de vos
en estas rondas...
ya forma parte de él.

Y vos seguís adelante
con un poco menos
de lo que no sabías que tenías.
""",
		"""
Ninguno terminó lo que empezó.

El Hambre acepta el empate
porque para él todo es alimento.
Incluso un empate.

Especialmente un empate.
""",
		{"lucidez": 10, "violencia": 5}, {"miedo": 12, "violencia": 8},
		["nombre"]
	)


static func crear_doble(psique_heredada: Dictionary = {}) -> Enemy:
	var modificador := 0
	if not psique_heredada.is_empty():
		var max_val: int = psique_heredada.values().max()
		modificador = min(3, max_val / 30)

	return _nuevo(
		"El Doble", "doble", "res://assets/images/enemy_doble.jpg",
		100 + modificador * 10, 7 + modificador,
		"""
Lo que dejaste atrás
nunca se quedó quieto.

El Doble.

No es una copia.
Es una acumulación.
Todo lo que sentiste en el descenso anterior
aprendió a moverse.

Comparte fragmentos de tu historia.
Los usa como argumentos.
Como armas.

No te conoce.
Es vos que te conocés a vos mismo.


[ ESPACIO para continuar ]
""",
		{
			"default": {
				"Guerrero":  "Usa tu fuerza de antes.\nLa que creías haber dejado atrás.\nMejorada por todo lo que aprendió.",
				"Hechicero": "Recita tus propios hechizos.\nLos del run anterior.\nCon más precisión de la que los usaste vos.",
				"Ladrón":    "Recuerda cada posición que elegiste.\nCada movimiento que funcionó.\nY los anticipa todos.",
				"_":         "El Doble avanza con la memoria de lo que fuiste.\nContra lo que sos.",
			},
			"ataque_pesado": {
				"Guerrero":  "El golpe más fuerte que diste la vez anterior.\nAhora viene hacia vos.",
				"Hechicero": "El hechizo que usaste cuando más lo necesitabas.\nUsado contra vos cuando más lo necesitás.",
				"Ladrón":    "La emboscada perfecta que ejecutaste.\nAhora ejecutada contra vos.",
				"_":         "Un movimiento de tu historial.\nElegido específicamente para vos.",
			},
			"desesperado": "Dañado, el Doble se fragmenta.\nPero los fragmentos siguen siendo vos.\nY siguen recordando.",
		},
		"""
El Doble se desintegra
en los fragmentos de memoria
que lo componían.

Lo que quedó del run anterior
ya pasó.

Seguís.
Con eso acumulado también.
""",
		"""
El Doble tiene todo lo que vos tenías.

Y usó todo lo que sabía.

Lo que lo venció
fue lo que no sabía:
lo que cambiaste
desde la última vez.

Eso es tuyo.
""",
		"""
Empate con vos mismo.

No hay forma más precisa
de describir lo que quedaste.

El Doble se hace a un lado.
Lo que llevan en común
pesa demasiado para seguir peleando.
""",
		{"lucidez": 12}, {"culpa": 10, "miedo": 8}
	)
