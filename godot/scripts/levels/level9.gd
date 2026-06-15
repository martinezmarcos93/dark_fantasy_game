extends BaseLevel
## Level 9 — La Biblioteca del Olvido.
## Port directo de game/levels/level9.py. Textos sagrados — no modificar.
## NOTA: distorsionar_texto() como transformación de texto (Fase 5 → shader).


func _init() -> void:
	nombre = "La Biblioteca del Olvido"


## La distorsión visual del texto la hace ahora GameScreen vía RichTextEffect
## según la psique (ver GameScreen._aplicar_distorsion_bbcode). Pasa el texto tal cual.
func distorsionar_texto(texto: String, _player: Player) -> String:
	return texto


# ── LABERINTO ─────────────────────────────────────────────
func fase_laberinto(player: Player, engine) -> void:
	var explorado := {"libros": false, "vacio": false}

	while true:
		var ids: Array = []
		var labels: Array = []
		if not explorado["libros"]:
			ids.append("libros"); labels.append("Explorar la sección de libros que se escriben solos")
		if not explorado["vacio"]:
			ids.append("vacio"); labels.append("Explorar el pasillo vacío al fondo")
		ids.append("cont"); labels.append("Continuar hacia el interior")

		var texto := distorsionar_texto(
			"\nLa biblioteca se extiende en todas las direcciones.\n\n"
			+ "Hay libros que se escriben solos a la izquierda.\n"
			+ "Un pasillo completamente vacío al fondo.\n\n"
			+ "Aliento del Umbral: %d/10\n\n" % player.aliento
			+ "¿Qué explorás?\n",
			player
		)

		var idx: int = await engine.mostrar_nivel("res://assets/images/maze.jpg", texto, labels)
		var id_elegido: String = ids[idx] if idx >= 0 and idx < ids.size() else "cont"

		if id_elegido == "cont":
			break

		player.ganar_aliento(1)

		if id_elegido == "libros":
			explorado["libros"] = true
			player.modificar_psique({"lucidez": 5})

			# Evento: Memoria como moneda
			if not player.historial.is_empty():
				await engine.mostrar_nivel(
					"res://assets/images/dead_end.jpg",
					distorsionar_texto(
						"\nLibros que escriben solos.\n"
						+ "Ninguno tiene tu nombre.\n"
						+ "Todavía.\n\n"
						+ "Uno de ellos se detiene.\n"
						+ "Te mira.\n"
						+ "Ofrece una página en blanco.\n\n"
						+ "\"¿Pagás con un recuerdo?\"\n"
						+ "A cambio: curación.\n",
						player
					),
					[]
				)

				var ultima: String = player.historial[-1]
				var preview: String = (ultima.substr(0, 60) + "…") if ultima.length() > 60 else ultima
				var elec2: int = await engine.mostrar_nivel(
					"res://assets/images/dead_end.jpg",
					distorsionar_texto(
						"\nEl libro ofrece borrar:\n\"%s\"\n\n" % preview
						+ "A cambio: +20 HP\n\n"
						+ "[ Lucidez +5   +1 Aliento del Umbral ]\n",
						player
					),
					["Pagar con el recuerdo  [+20 HP]", "Rechazar"]
				)

				if elec2 == 0:
					player.gastar_memoria(player.historial.size() - 1)
					player.recuperar(20)
					var msg := "\nEl recuerdo desaparece.\nEl libro lo absorbe.\nHP +20.\n"
					if player.historial.is_empty():
						msg += "\nNo recordás nada de lo que hiciste.\nEso también dice algo.\n"
					await engine.mostrar_nivel(
						"res://assets/images/dead_end.jpg",
						distorsionar_texto(msg, player),
						[]
					)
				else:
					await engine.mostrar_nivel(
						"res://assets/images/dead_end.jpg",
						distorsionar_texto("\nRechazás.\nEl libro cierra solo.\n", player),
						[]
					)
			else:
				await engine.mostrar_nivel(
					"res://assets/images/dead_end.jpg",
					distorsionar_texto(
						"\nLibros que escriben solos.\nNinguno tiene tu nombre.\n"
						+ "Todavía.\n\n[ Lucidez +5   +1 Aliento del Umbral ]\n",
						player
					),
					[]
				)

		elif id_elegido == "vacio":
			explorado["vacio"] = true
			player.modificar_psique({"corrupcion": 8})
			await engine.mostrar_nivel(
				"res://assets/images/dead_end.jpg",
				distorsionar_texto(
					"\nEl pasillo no tiene fin visible.\n\n"
					+ "Caminás.\nCaminás.\nCaminás.\n\n"
					+ "En algún punto te detenés.\n"
					+ "No porque hayas llegado a algún lado.\n"
					+ "Sino porque algo te hace detenerte.\n\n"
					+ "No sabés qué.\nEso también cambia algo.\n\n"
					+ "[ Corrupción +8   +1 Aliento del Umbral ]\n",
					player
				),
				[]
			)


# El Hambre puede aparecer también en Level 9 (>6 usos violentos). "muerte" o "".
func _chequear_hambre_aqui(player: Player, engine) -> String:
	var usos_violentos := (
		player.contar_usos_accion("furia")
		+ player.contar_usos_accion("apuñalar")
	)
	if usos_violentos <= 6:
		return ""

	var enemy := EnemyFactory.crear_hambre()
	enemy.texto_intro = (
		"\nOtra vez.\n\n"
		+ "No aprendiste.\n"
		+ "O aprendiste demasiado bien.\n\n"
		+ "El Hambre vuelve.\n"
		+ "Más hambriento.\n\n"
		+ "\n[ ESPACIO para continuar ]\n"
	)
	enemy.dificultad = min(enemy.dificultad + 1, 12)  # Un poco más difícil

	var resultado: String = await engine.combate_narrativo(enemy)

	if resultado == "muerte":
		return "muerte"

	player.vida_max += 20
	player.recuperar(20)
	await engine.mostrar_nivel(
		"res://assets/images/enemy_hambre.jpg",
		"\nOtra vez lo venciste.\nAlgo en vos aprende a contenerse.\nO a alimentarse diferente.\n\n[ HP máximo +20 ]\n",
		[]
	)
	return ""


func fase_combate(_player: Player, engine) -> String:
	var enemy := EnemyFactory.crear_grieta()
	return await engine.combate_narrativo(enemy)


func fase_psicologica(player: Player, engine) -> void:
	player.recuperar(3, 6)

	# Cofre de Eco si combate perfecto
	await engine.ofrecer_cofre_eco("res://assets/images/lvl9.jpg")

	var texto := """
Los libros no tienen titulos.

Las paginas estan en blanco.

Pero cuando los abris,
algo se escribe.
No con tinta.
Con ausencia.

Cada libro contiene
algo que olvidaste.
O que decidiste no recordar.

Hay uno que brilla mas que los otros.

¿Que hacés?
"""

	var eleccion: int = await engine.mostrar_nivel(
		"res://assets/images/lvl9.jpg",
		distorsionar_texto(texto, player),
		[
			"Abrir el libro que brilla.",
			"Leer un libro al azar.",
			"Cerrar los ojos y salir sin leer ninguno.",
		]
	)

	if eleccion == 0:
		player.registrar_decision("Abriste el libro que brillaba en la Biblioteca del Olvido.")
		player.psique["lucidez"] += 15
		player.psique["corrupcion"] += 8
		var texto_r := """
Lo abris.

El libro contiene
lo que elegiste no saber.

No porque no pudieras saberlo.
Sino porque saber
hubiera requerido cambiar.

Ahora lo sabes.

No cambia lo que hiciste.
Pero cambia lo que sos.
"""
		await engine.mostrar_nivel(
			"res://assets/images/lvl9.jpg",
			distorsionar_texto(texto_r, player),
			[]
		)

	elif eleccion == 1:
		player.registrar_decision("Leiste un libro al azar en la Biblioteca del Olvido.")
		player.psique["culpa"] += 10
		player.psique["miedo"] += 8
		var texto_r := """
Abris uno sin pensar.

El contenido no tiene sentido
en el orden en que aparece.

Pero tiene sentido
en un orden que no controlás.

No encontraste lo que buscabas.
Encontraste algo peor:
lo que no sabias que buscabas.
"""
		await engine.mostrar_nivel(
			"res://assets/images/lvl9.jpg",
			distorsionar_texto(texto_r, player),
			[]
		)

	elif eleccion == 2:
		player.registrar_decision("Saliste de la Biblioteca del Olvido sin leer nada.")
		player.psique["corrupcion"] += 15
		player.ganar_aliento(1)  # Elección peligrosa
		var texto_r := """
Cerrás los ojos.

Salis.

Lo que no leiste
no desaparece.
Solo pierde nombre.

Y lo sin nombre
crece en los espacios
donde no mirás.

La biblioteca sigue ahi.
Con todos sus libros.
Con el tuyo.

[ +1 Aliento del Umbral ]
"""
		await engine.mostrar_nivel(
			"res://assets/images/lvl9.jpg",
			distorsionar_texto(texto_r, player),
			[]
		)


func jugar(player: Player, engine) -> String:
	await fase_laberinto(player, engine)

	# El Hambre (segunda aparición si los usos superan el umbral)
	var resultado_hambre: String = await _chequear_hambre_aqui(player, engine)
	if resultado_hambre == "muerte":
		return "muerte"

	var resultado: String = await fase_combate(player, engine)
	if resultado == "muerte":
		return "muerte"

	await fase_psicologica(player, engine)
	return "continuar"
