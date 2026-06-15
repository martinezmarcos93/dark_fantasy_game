extends BaseLevel
## Level 3 — El Ritual de la Entrega.
## Port directo de game/levels/level3.py. Textos sagrados — no modificar.


func _init() -> void:
	nombre = "El Ritual de la Entrega"


# ── LABERINTO ─────────────────────────────────────────────
func fase_laberinto(player: Player, engine) -> void:
	var explorado := {"izquierda": false, "derecha": false}

	while true:
		var ids: Array = []
		var labels: Array = []
		if not explorado["izquierda"]:
			ids.append("izq"); labels.append("Explorar la izquierda  [oscuro, sin sonido]")
		if not explorado["derecha"]:
			ids.append("der"); labels.append("Explorar la derecha  [hay algo que brilla]")
		ids.append("cont"); labels.append("Continuar hacia el altar")

		var texto := (
			"\nEl pasaje se bifurca antes de llegar al altar.\n\n"
			+ "El corredor de la izquierda está en silencio absoluto.\n"
			+ "El de la derecha tiene un brillo apenas visible.\n\n"
			+ "Aliento del Umbral: %d/10\n\n" % player.aliento
			+ "¿Qué explorás?\n"
		)

		var idx: int = await engine.mostrar_nivel("res://assets/images/maze.jpg", texto, labels)
		var id_elegido: String = ids[idx] if idx >= 0 and idx < ids.size() else "cont"

		if id_elegido == "cont":
			break

		player.ganar_aliento(1)

		if id_elegido == "izq":
			explorado["izquierda"] = true
			await engine.mostrar_nivel(
				"res://assets/images/dead_end.jpg",
				"""
Un callejón estrecho termina en pared.

Encontrás marcas en la piedra.
Alguien pasó antes que vos.
Las marcas son recientes.
Las manos que las hicieron conocían este lugar.

No hay nadie ahora.

[ +1 Aliento del Umbral ]
""",
				[]
			)

		elif id_elegido == "der":
			explorado["derecha"] = true
			player.modificar_psique({"corrupcion": 5})
			await engine.mostrar_nivel(
				"res://assets/images/dead_end.jpg",
				"""
El brillo no tiene fuente visible.

Seguís el corredor hasta que termina en nada.
No hay objeto. No hay criatura.
Solo un brillo que no debería existir.

Al darte vuelta sentís que algo cambió.
No sabés qué.
Eso es parte del problema.

[ +1 Aliento del Umbral   Corrupción +5 ]
""",
				[]
			)


func fase_combate(_player: Player, engine) -> String:
	var enemy := EnemyFactory.crear_sacerdote()
	return await engine.combate_narrativo(enemy)


func fase_psicologica(player: Player, engine) -> void:
	player.recuperar(6, 12)

	# Cofre de Eco si combate perfecto
	await engine.ofrecer_cofre_eco("res://assets/images/lvl3.jpg")

	var texto := """
La cueva se abre en una sala amplia.
El aire es pesado.
Antiguo.
En el centro hay un altar de piedra.
Encima… un libro.
Sus páginas están en blanco.
Pero algo se escribe lentamente.
No con tinta.
Con algo más denso.

La voz susurra:
"Para comprender… tenés que entregar."

¿Qué hacés?
"""

	var eleccion: int = await engine.mostrar_nivel(
		"res://assets/images/lvl3.jpg",
		texto,
		[
			"Leer el libro",
			"Ofrecer tu sangre",
			"Ignorar el altar y seguir",
		]
	)

	if eleccion == 0:
		player.registrar_decision("Leíste el libro. Las palabras hablaban de vos.")
		player.psique["lucidez"] += 15
		player.psique["corrupcion"] += 5
		await engine.mostrar_nivel(
			"res://assets/images/lvl3.jpg",
			"""
Leés.
Las palabras no están escritas.
Se forman mientras las mirás.
Y hablan de vos.
De cosas que no recordabas…
pero que son ciertas.
Cada línea te revela.
Pero también te cambia.
""",
			[]
		)

	elif eleccion == 1:
		player.registrar_decision("Ofreciste tu sangre al altar. Algo en vos ya había elegido.")
		player.psique["corrupcion"] += 20
		player.ganar_aliento(1)  # Elección peligrosa
		await engine.mostrar_nivel(
			"res://assets/images/lvl3.jpg",
			"""
Apoyás tu mano.
La piedra está tibia.
La sangre fluye.
El libro responde.
Las páginas se llenan.
Pero no con conocimiento.
Con aceptación.
Algo en vos… ya eligió.

[ +1 Aliento del Umbral ]
""",
			[]
		)

	elif eleccion == 2:
		player.registrar_decision("Ignoraste el altar. La decisión pendiente te siguió.")
		player.psique["miedo"] += 10
		await engine.mostrar_nivel(
			"res://assets/images/lvl3.jpg",
			"""
Te alejás.
Pero el altar no desaparece.
Lo sentís.
Como una decisión no tomada.
Como algo pendiente.
Y sabés…
que lo vas a volver a ver.
""",
			[]
		)

	# Llave de piedra para el Nivel 4
	player.llave_piedra = true
	await engine.mostrar_nivel(
		"res://assets/images/key_stone.jpg",
		"""
Al salir del altar encontrás algo grabado en el umbral.

Una llave de piedra, pequeña, casi decorativa.
Como si alguien la hubiera dejado a propósito.

O como si siempre hubiera estado esperando.

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
