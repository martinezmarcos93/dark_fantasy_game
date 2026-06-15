extends BaseLevel
## Level 1 — La Cueva del Origen.
## Port directo de game/levels/level1.py. Textos sagrados — no modificar.


func _init() -> void:
	nombre = "La Cueva del Origen"


func fase_combate(_player: Player, engine) -> String:
	var enemy := EnemyFactory.crear_guardian()
	return await engine.combate_narrativo(enemy)


func fase_psicologica(player: Player, engine) -> void:
	player.recuperar(8, 15)

	var texto := """
Te adentras en la cueva.
No hay antorchas. No hay sonido.
Solo oscuridad.
Algo… respira en la profundidad.
No lo ves, pero lo sentís.
Una voz, o tal vez un pensamiento que no es tuyo, susurra:
"Antes de la luz… ya estabas aquí."

¿Qué hacés?
"""

	var eleccion: int = await engine.mostrar_nivel(
		"res://assets/images/lvl1.jpg",
		texto,
		[
			"Avanzar hacia la oscuridad",
			"Encender una antorcha",
			"Llamar para saber quién está ahí",
		]
	)

	if eleccion == 0:
		player.registrar_decision("Avanzaste hacia la oscuridad sin dudar.")
		player.psique["corrupcion"] += 10
		player.ganar_aliento(1)  # Elección peligrosa
		await engine.mostrar_nivel(
			"res://assets/images/lvl1.jpg",
			"""
Caminás sin ver.
Cada paso se siente… correcto.
Como si ya hubieras estado ahí antes.
La oscuridad no te rechaza.
Te envuelve.

La voz vuelve:
"Recordar es descender."

[ +1 Aliento del Umbral ]
""",
			[]
		)

	elif eleccion == 1:
		player.registrar_decision("Encendiste una antorcha para ver lo que había.")
		player.psique["lucidez"] += 10
		await engine.mostrar_nivel(
			"res://assets/images/lvl1.jpg",
			"""
La antorcha enciende.
La luz revela paredes húmedas…
y marcas.
No son naturales.
Son manos.
Cientos de ellas.
Marcadas desde adentro.

La voz susurra:
"La luz no revela. Delata."
""",
			[]
		)

	elif eleccion == 2:
		player.registrar_decision("Llamaste hacia la oscuridad, aunque sabías que algo respondería.")
		player.psique["miedo"] += 15
		await engine.mostrar_nivel(
			"res://assets/images/lvl1.jpg",
			"""
Tu voz se pierde.
Pero algo responde.
No con sonido.
Con presencia.
Ahora sabés que no estás solo.
Y nunca lo estuviste.
""",
			[]
		)

	# Cofre de Eco si el combate fue perfecto
	await engine.ofrecer_cofre_eco("res://assets/images/lvl1.jpg")

	# Al final del nivel, el jugador encuentra la llave de piedra para el nivel 2
	player.llave_piedra = true
	await engine.mostrar_nivel(
		"res://assets/images/key_stone.jpg",
		"""
Antes de continuar encontrás algo en el suelo.

Una llave de piedra.
Pulida por manos que ya no están.

No sabés qué abre.
Pero la tomás igual.

[ Llave de Piedra obtenida ]
""",
		[]
	)
