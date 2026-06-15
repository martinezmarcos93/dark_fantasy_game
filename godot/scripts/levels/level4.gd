extends BaseLevel
## Level 4 — El Rey de las Sombras.
## Port directo de game/levels/level4.py. Textos sagrados — no modificar.


func _init() -> void:
	nombre = "El Rey de las Sombras"


# El Doble — solo en New Game+. Devuelve "muerte" o "" (continuar).
func _chequear_doble(player: Player, engine) -> String:
	if not SaveSystem.existe_ng_plus():
		return ""

	var psique_heredada := SaveSystem.cargar_ng_plus()
	if psique_heredada.is_empty():
		return ""

	await engine.mostrar_nivel(
		"res://assets/images/enemy_doble.jpg",
		"""
%s.

Algo llega desde la dirección equivocada.

No es la Sombra.

Es algo que lleva fragmentos de tu historial anterior.
Fragmentos de lo que fuiste.
Usados contra lo que sos.

El Doble.
""" % player.name_jugador,
		[]
	)

	var enemy := EnemyFactory.crear_doble(psique_heredada)
	var resultado: String = await engine.combate_narrativo(enemy)

	if resultado == "muerte":
		return resultado

	# Recompensa: ítem del tier alto + fragmento de lore
	await engine.mostrar_nivel(
		"res://assets/images/enemy_doble.jpg",
		"""
El Doble se deshace.

Los fragmentos de memoria que lo componían
se dispersan en el aire.

Queda algo atrás.
Un objeto que perteneció a quien fuiste.
""",
		[]
	)

	var item: String = Player.TIER_ALTO.pick_random()
	await engine._dar_item(
		"res://assets/images/enemy_doble.jpg", item,
		"El Doble dejó atrás: %s\n" % Player.NOMBRES_ITEMS.get(item, item)
	)

	return ""  # Continuar con el nivel normal


func fase_combate(_player: Player, engine) -> String:
	var enemy := EnemyFactory.crear_sombra()
	return await engine.combate_narrativo(enemy)


func fase_psicologica(player: Player, engine) -> void:
	player.recuperar(5, 10)

	# Cofre de Piedra si tiene llave (del Level 3)
	await engine.ofrecer_cofre_piedra("res://assets/images/chest_stone.jpg")

	var texto := """
El camino se estrecha.
Las paredes ya no son piedra.
Son… carne.
Respiran.
Late algo dentro.
Avanzás igual.
Llegás a una grieta.
Y ahí… los ves.
Versiones tuyas.
Distintas.
Una llora.
Otra sonríe.
Otra te observa con desprecio.

La voz dice:
"%s. No sos uno. Elegí."

¿Qué hacés?
""" % player.name_jugador

	var eleccion: int = await engine.mostrar_nivel(
		"res://assets/images/lvl4.jpg",
		texto,
		[
			"Aceptar todas las versiones",
			"Rechazar las versiones",
			"Atacar a las versiones",
		]
	)

	if eleccion == 0:
		player.registrar_decision("Aceptaste todas las versiones de vos mismo. Las que dolían también.")
		player.psique["lucidez"] += 20
		await engine.mostrar_nivel(
			"res://assets/images/lvl4.jpg",
			"""
No elegís.
Las aceptás.
Todas.
Las que duelen.
Las que avergüenzan.
Las que ocultabas.
No desaparecen.
Se alinean.
Y por un instante…
sos completo.
""",
			[]
		)

	elif eleccion == 1:
		player.registrar_decision("Rechazaste las versiones. Se volvieron más intensas.")
		player.psique["culpa"] += 15
		player.psique["miedo"] += 10
		await engine.mostrar_nivel(
			"res://assets/images/lvl4.jpg",
			"""
Negás.
Una por una.
Intentás borrar lo que no te gusta.
Pero no se van.
Se deforman.
Se vuelven más intensas.
Más presentes.

La voz susurra:
"Negar es alimentar."
""",
			[]
		)

	elif eleccion == 2:
		player.registrar_decision("Atacaste a las versiones. Se multiplicaron.")
		player.psique["violencia"] += 20
		player.psique["corrupcion"] += 10
		player.ganar_aliento(1)  # Elección peligrosa
		await engine.mostrar_nivel(
			"res://assets/images/lvl4.jpg",
			"""
Atacás.
Golpeás.
Destruís.
Pero cada versión rota…
se multiplica.
Ahora son más.
Más agresivas.
Más reales.
Y ya no esperan.

[ +1 Aliento del Umbral ]
""",
			[]
		)


func jugar(player: Player, engine) -> String:
	# Chequear El Doble (NG+)
	var resultado_doble: String = await _chequear_doble(player, engine)
	if resultado_doble == "muerte":
		return "muerte"

	var resultado: String = await fase_combate(player, engine)
	if resultado == "muerte":
		return "muerte"

	await fase_psicologica(player, engine)
	return "continuar"
