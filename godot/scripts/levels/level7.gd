extends BaseLevel
## Level 7 — La Sala del Juicio.
## Port directo de game/levels/level7.py. Textos sagrados — no modificar.


func _init() -> void:
	nombre = "La Sala del Juicio"


# ── LABERINTO ─────────────────────────────────────────────
func fase_laberinto(player: Player, engine) -> void:
	var explorado := {"izquierda": false, "espejo_roto": false}

	while true:
		var ids: Array = []
		var labels: Array = []
		if not explorado["izquierda"]:
			ids.append("izq"); labels.append("Explorar el pasillo izquierdo  [silencio, asientos vacíos]")
		if not explorado["espejo_roto"]:
			ids.append("espejo"); labels.append("Explorar el callejón del fondo  [brilla algo roto]")
		ids.append("cont"); labels.append("Entrar a la Sala del Juicio")

		var texto := (
			"\nAntes de entrar a la Sala del Juicio\nhay corredores laterales.\n\n"
			+ "El pasillo izquierdo está lleno de asientos de piedra vacíos.\n"
			+ "Al fondo se ve algo roto que capta la luz.\n\n"
			+ "Aliento del Umbral: %d/10\n\n" % player.aliento
			+ "¿Explorás?\n"
		)

		var idx: int = await engine.mostrar_nivel("res://assets/images/maze.jpg", texto, labels)
		var id_elegido: String = ids[idx] if idx >= 0 and idx < ids.size() else "cont"

		if id_elegido == "cont":
			break

		player.ganar_aliento(1)

		if id_elegido == "izq":
			explorado["izquierda"] = true
			player.modificar_psique({"miedo": 5})
			await engine.mostrar_nivel(
				"res://assets/images/dead_end.jpg",
				"""
Miles de asientos de piedra.

Todos vacíos.

Pero el polvo en cada uno está asentado
de formas que sugieren que alguien estuvo ahí.

No recientemente.
Pero estuvo.

El silencio aquí no es ausencia de sonido.
Es la acumulación de todos los veredictos
que nunca se pronunciaron.

[ +1 Aliento del Umbral   Miedo +5 ]
""",
				[]
			)

		elif id_elegido == "espejo":
			explorado["espejo_roto"] = true
			player.modificar_psique({"lucidez": 8, "miedo": 5})
			await engine.mostrar_nivel(
				"res://assets/images/dead_end.jpg",
				"""
Un espejo roto en el suelo.

Grande. De alguna sala que ya no existe.

Los fragmentos reflejan algo.
Pero la imagen que muestran
no es exactamente la tuya.

Es vos.
Pero desde un ángulo que no existe.
Como si el espejo te recordara
de una vez que todavía no pasó.

[ +1 Aliento del Umbral   Lucidez +8   Miedo +5 ]
""",
				[]
			)


func fase_combate(_player: Player, engine) -> String:
	var enemy := EnemyFactory.crear_eco()
	return await engine.combate_narrativo(enemy)


func fase_psicologica(player: Player, engine) -> void:
	player.recuperar(5, 10)

	# Cofre de Eco si combate perfecto
	await engine.ofrecer_cofre_eco("res://assets/images/lvl7.jpg")

	var texto := """
La Sala del Juicio está vacía.

Miles de asientos de piedra.
Ningún juez.
Solo vos en el centro.

El silencio no es ausencia de sonido.
Es la acumulación de todo lo que
dijiste y deberías haber callado.
Y de todo lo que callaste
y deberías haber dicho.

Una voz que es tu voz pero no es tu voz:
"¿Qué testimonio darías de vos mismo?"

¿Qué hacés?
"""

	var eleccion: int = await engine.mostrar_nivel(
		"res://assets/images/lvl7.jpg",
		texto,
		[
			"Hablar. Decir todo.",
			"Guardar silencio.",
			"Negar que haya algo que decir.",
		]
	)

	if eleccion == 0:
		player.registrar_decision("Hablaste. Dijiste todo en la Sala del Juicio.")
		player.psique["lucidez"] += 12
		player.psique["culpa"] += 8
		await engine.mostrar_nivel(
			"res://assets/images/lvl7.jpg",
			"""
Hablás.

Todo.
Sin orden.
Sin filtro.

Las palabras llenan la sala
y rebotan en el vacío.

No hay nadie para escucharte.
Pero el acto de decirlo
cambia algo.

No te absuelve.
Solo te hace más real.
""",
			[]
		)

	elif eleccion == 1:
		player.registrar_decision("Guardaste silencio ante el juicio.")
		player.psique["miedo"] += 10
		player.psique["lucidez"] += 5
		await engine.mostrar_nivel(
			"res://assets/images/lvl7.jpg",
			"""
No decís nada.

El silencio se asienta.

La sala no te juzga por callarte.
No tiene capacidad de juzgar nada.

Pero vos te juzgás a vos mismo.
Y eso ocupa más espacio
que cualquier veredicto externo.
""",
			[]
		)

	elif eleccion == 2:
		player.registrar_decision("Negaste tener algo que decir en el juicio.")
		player.psique["corrupcion"] += 12
		player.psique["violencia"] += 5
		player.ganar_aliento(1)  # Elección peligrosa
		await engine.mostrar_nivel(
			"res://assets/images/lvl7.jpg",
			"""
Decís que no hay nada.

La sala no responde.

Pero algo en el aire
cambia de temperatura.

Lo que negas
no desaparece.
Solo deja de tener nombre.
Y lo sin nombre
es más peligroso.

[ +1 Aliento del Umbral ]
""",
			[]
		)

	# Llave de piedra para el Nivel 8
	player.llave_piedra = true
	await engine.mostrar_nivel(
		"res://assets/images/key_stone.jpg",
		"""
Al salir de la Sala encontrás algo en la silla central.

Una llave de piedra.
Pequeña.
Como si el juicio hubiera dejado algo para vos.

[ Llave de Piedra obtenida ]
""",
		[]
	)


func jugar(player: Player, engine) -> String:
	await fase_laberinto(player, engine)

	var resultado: String = await fase_combate(player, engine)
	if resultado == "muerte":
		return "muerte"

	await fase_psicologica(player, engine)
	return "continuar"
