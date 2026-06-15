extends BaseLevel
## Level 2 — El Espejo de las Formas.
## Port directo de game/levels/level2.py. Textos sagrados — no modificar.


func _init() -> void:
	nombre = "El Espejo de las Formas"


# ── CALLEJÓN: El Viajero Perdido ─────────────────────────
func fase_callejon(player: Player, engine) -> void:
	var texto := """
Antes de llegar al espejo notan un pasadizo lateral.
Estrecho. Apenas visible.

¿Explorás?
"""
	var eleccion: int = await engine.mostrar_nivel(
		"res://assets/images/dead_end.jpg",
		texto,
		["Explorar el pasadizo", "Ignorarlo y continuar"]
	)

	if eleccion != 0:
		return

	player.ganar_aliento(1)  # Explorar callejón

	if player.aliento >= 3 and player.aliado_tipo == "":
		# El Viajero Perdido
		await engine.mostrar_nivel(
			"res://assets/images/npc_viajero.jpg",
			"""
Al final del pasadizo hay una figura.

Ropa de viaje desgastada.
Equipo demasiado ligero para este lugar.
No habla mucho.

Solo dice:
"También estoy bajando."

Te mira. Calcula algo.
Después dice:
"Puedo acompañarte una vez. Si me convencés."

Costo: 3 Aliento del Umbral.

[ +1 Aliento del Umbral por explorar ]
""",
			[]
		)

		if player.aliento >= 3:
			var eleccion2: int = await engine.mostrar_nivel(
				"res://assets/images/npc_viajero.jpg",
				"\nAliento actual: %d/10\n\n¿Convencés al Viajero para que te acompañe?\n" % player.aliento,
				[
					"Convencerlo  [−3 Aliento]",
					"Dejarlo ir",
				]
			)
			if eleccion2 == 0 and player.gastar_aliento(3):
				player.aliado_tipo    = "viajero"
				player.viajero_activo = true
				player.registrar_decision("Convenciste al Viajero Perdido de acompañarte.")
				await engine.mostrar_nivel(
					"res://assets/images/npc_viajero.jpg",
					"""
Asiente.

Sin palabras.
Te sigue hacia la sala del espejo.

Aparecerá al inicio del próximo combate.
Una sola vez.
Después se irá.

[ −3 Aliento del Umbral — El Viajero te acompaña ]
""",
					[]
				)
		else:
			await engine.mostrar_nivel(
				"res://assets/images/npc_viajero.jpg",
				"\nNo tenés suficiente Aliento del Umbral para convencerlo.\nSe queda donde está.\n",
				[]
			)
	else:
		# Callejón sin El Viajero: solo lore
		await engine.mostrar_nivel(
			"res://assets/images/dead_end.jpg",
			"""
El pasadizo termina en pared.

Marcas en la piedra.
Alguien estuvo acá antes.
Las marcas dicen que siguió.

No hay nada más aquí.

[ +1 Aliento del Umbral por explorar ]
""",
			[]
		)


func fase_combate(_player: Player, engine) -> String:
	var enemy := EnemyFactory.crear_reflejo()
	return await engine.combate_narrativo(enemy)


func fase_psicologica(player: Player, engine) -> void:
	player.recuperar(8, 15)

	# Cofre de Eco si combate perfecto
	await engine.ofrecer_cofre_eco("res://assets/images/lvl2.jpg")

	# Cofre de Piedra si tiene la llave (del Level 1)
	await engine.ofrecer_cofre_piedra("res://assets/images/chest_stone.jpg")

	var texto := """
Avanzás más profundo en la cueva.
El aire cambia. Es más denso.
Llegás a una cámara circular.
En el centro… hay un espejo.
Pero no refleja tu cuerpo.
Refleja… algo más.
La voz regresa:
"No sos lo que creés. Mirá."

¿Qué hacés?
"""

	var eleccion: int = await engine.mostrar_nivel(
		"res://assets/images/lvl2.jpg",
		texto,
		[
			"Mirar fijamente el espejo",
			"Romper el espejo",
			"Dar la espalda y seguir",
		]
	)

	if eleccion == 0:
		player.registrar_decision("Miraste fijamente el espejo aunque el reflejo se adelantara.")
		player.psique["lucidez"] += 15
		await engine.mostrar_nivel(
			"res://assets/images/lvl2.jpg",
			"""
Te acercás.
Tu reflejo no te copia.
Se adelanta.
Sonríe antes que vos.
Y entonces entendés…
No estás mirando.
Estás siendo observado.
""",
			[]
		)

	elif eleccion == 1:
		player.registrar_decision("Rompiste el espejo. Las versiones peores siguen ahí.")
		player.psique["violencia"] += 15
		player.ganar_aliento(1)  # Elección peligrosa
		await engine.mostrar_nivel(
			"res://assets/images/lvl2.jpg",
			"""
Golpeás el espejo.
Se rompe.
Pero no desaparece.
Cada fragmento sigue reflejando.
Versiones tuyas.
Peores.
Más sinceras.

La voz:
"Romper no elimina."

[ +1 Aliento del Umbral ]
""",
			[]
		)

	elif eleccion == 2:
		player.registrar_decision("Le diste la espalda al espejo. El reflejo no necesitó verlo.")
		player.psique["miedo"] += 10
		await engine.mostrar_nivel(
			"res://assets/images/lvl2.jpg",
			"""
Das la espalda.
Pero sentís la mirada.
El reflejo no depende del espejo.
Ahora está en vos.
Y no podés dejar de sentirlo.
""",
			[]
		)


func jugar(player: Player, engine) -> String:
	await fase_callejon(player, engine)

	var resultado: String = await fase_combate(player, engine)
	if resultado == "muerte":
		return "muerte"

	await fase_psicologica(player, engine)
	return "continuar"
