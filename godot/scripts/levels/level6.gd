extends BaseLevel
## Level 6 — El Umbral Final.
## Port directo de game/levels/level6.py. Textos sagrados — no modificar.
## NOTA: distorsionar_texto() como transformación de texto (Fase 5 → shader).


func _init() -> void:
	nombre = "El Umbral Final"


## La distorsión visual del texto la hace ahora GameScreen vía RichTextEffect
## según la psique (ver GameScreen._aplicar_distorsion_bbcode). Pasa el texto tal cual.
func distorsionar_texto(texto: String, _player: Player) -> String:
	return texto


# El Hambre — si furia/apuñalar se usaron >4 veces. Devuelve "muerte" o "".
func _chequear_hambre(player: Player, engine) -> String:
	var usos_violentos := (
		player.contar_usos_accion("furia")
		+ player.contar_usos_accion("apuñalar")
	)
	if usos_violentos <= 4:
		return ""

	# Aparece sin pantalla de intro — directamente en el encabezado de combate
	var enemy := EnemyFactory.crear_hambre()
	# Sobreescribir texto_intro para que sea mínimo
	enemy.texto_intro = (
		"\nNo hubo aviso.\n"
		+ "No hubo transición.\n"
		+ "\nEl Hambre ya estaba acá.\n"
		+ "\n\n[ ESPACIO para continuar ]\n"
	)

	var resultado: String = await engine.combate_narrativo(enemy)

	if resultado == "muerte":
		return "muerte"

	# Reward: +20 HP máximo permanente
	player.vida_max += 20
	player.recuperar(20)
	player.registrar_decision("Venciste al Hambre. Algo en vos aprendió a contenerlo.")
	await engine.mostrar_nivel(
		"res://assets/images/enemy_hambre.jpg",
		"""
El Hambre retrocedió.

No porque hayas ganado.
Sino porque, por ahora,
está satisfecho.

Algo en vos absorbe lo que dejó.

[ HP máximo +20 — permanente hasta el fin del run ]
""",
		[]
	)
	return ""


func jugar(player: Player, engine) -> String:
	# El Hambre (consecuencia de violencia acumulada)
	var resultado_hambre: String = await _chequear_hambre(player, engine)
	if resultado_hambre == "muerte":
		return "muerte"

	# Cofre del Umbral (si aliento >= 5 y aún disponible)
	await engine.ofrecer_cofre_umbral("res://assets/images/lvl6.jpg")

	var texto := """
No hay más puertas.
No hay más caminos.
No hay cueva.
No hay voz.
Solo vos.
O lo que queda de %s.

Frente a vos…
hay algo.
Tiene tu forma.
Pero no te copia.
Respira con vos.
Piensa con vos.
Sabe todo lo que hiciste.

Sabe que sos %s.
Y no te juzga.
Solo espera.

¿Qué hacés?
""" % [player.name_jugador, player.name_jugador]

	var eleccion: int = await engine.mostrar_nivel(
		"res://assets/images/lvl6.jpg",
		distorsionar_texto(texto, player),
		[
			"Aceptar lo que sos",
			"Negarlo",
			"Destruirlo",
		]
	)

	if eleccion == 0:
		player.registrar_decision("Aceptaste lo que sos. Todo. Sin condiciones.")
		player.psique["lucidez"] += 20

		var texto_resultado := """
No resistís.
No luchás.
Lo mirás.
Y lo aceptás.

No desaparece.
Se integra.

Por primera vez…
no hay conflicto.

Solo totalidad.
"""
		await engine.mostrar_nivel(
			"res://assets/images/lvl6.jpg",
			distorsionar_texto(texto_resultado, player),
			[]
		)
		return "continuar"

	elif eleccion == 1:
		player.registrar_decision("Negaste lo que sos. Se volvió más presente.")
		player.psique["miedo"] += 20
		player.psique["culpa"] += 10

		var texto_resultado := """
Negás.
Intentás separarte.
Decir que eso no sos vos.

Pero no se va.
Se distorsiona.
Se vuelve más presente.
Más inevitable.

Porque no podés negar lo que sos.
"""
		await engine.mostrar_nivel(
			"res://assets/images/lvl6.jpg",
			distorsionar_texto(texto_resultado, player),
			[]
		)
		return "continuar"

	elif eleccion == 2:
		player.registrar_decision("Intentaste destruirlo. Cada golpe fue interno.")
		player.psique["violencia"] += 20
		player.psique["corrupcion"] += 15
		player.ganar_aliento(1)  # Elección peligrosa

		var texto_resultado := """
Atacás.
Sin dudar.
Con todo.

Pero no hay impacto.
Porque no hay distancia.

Cada golpe…
es interno.

Y algo empieza a romperse.
Pero no es eso.

Sos vos.

[ +1 Aliento del Umbral ]
"""
		await engine.mostrar_nivel(
			"res://assets/images/lvl6.jpg",
			distorsionar_texto(texto_resultado, player),
			[]
		)
		return "continuar"

	return "muerte"
