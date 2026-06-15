extends BaseLevel
## Level 10 — El Espejo Final.
## Port directo de game/levels/level10.py. Textos sagrados — no modificar.
## Dos combates: El Testigo (3 rondas) y El Umbral Encarnado (5 rondas).


func _init() -> void:
	nombre = "El Espejo Final"


func fase_combate_testigo(_player: Player, engine) -> String:
	# Primera fase: El Testigo. Combate normal de 3 rondas.
	var enemy := EnemyFactory.crear_testigo()
	return await engine.combate_narrativo(enemy)


func fase_combate_boss(player: Player, engine) -> String:
	# Segunda fase: El Umbral Encarnado. 5 rondas. Solo si el jugador sigue vivo.
	player.recuperar(20, 20)

	await engine.mostrar_nivel(
		"res://assets/images/lvl10.jpg",
		"""
%s.

Pasaste al Testigo.

Pero lo que el Testigo guardaba
ahora esta frente a vos.

No es una recompensa.
No es un castigo.

Es lo que siempre estuvo
al final de este camino.

El Umbral Encarnado.

Cinco rondas.
No porque sean necesarias.
Sino porque esto
no termina rapido.


[ ESPACIO para continuar ]
""" % player.name_jugador,
		[]
	)

	var enemy := EnemyFactory.crear_umbral_encarnado()
	return await engine.combate_narrativo(enemy)


func jugar(player: Player, engine) -> String:
	# Fase 1: El Testigo
	var resultado: String = await fase_combate_testigo(player, engine)
	if resultado == "muerte":
		return "muerte"

	# Si sobrevivio al Testigo: El Espejo
	await engine.mostrar_nivel(
		"res://assets/images/lvl10.jpg",
		"""
El Testigo se hace a un lado.

Frente a vos hay un espejo.

No refleja la caverna.
Refleja un mundo con luz natural.
Con gente.
Con ruido de fondo.
Con el olor de algo cocinandose.

Todo lo que dejaste afuera.

Y en el centro del reflejo
hay algo que tiene tu forma
pero que no sos vos.

O si lo es.
""",
		[]
	)

	# Fase 2: El boss
	resultado = await fase_combate_boss(player, engine)
	if resultado == "muerte":
		return "muerte"

	# Escena final despues del boss
	await engine.mostrar_nivel(
		"res://assets/images/lvl10.jpg",
		"""
%s.

El Umbral Encarnado no desaparecio.

Nunca iba a desaparecer.

Pero ya no bloquea el camino.

No porque lo hayas vencido.
Sino porque algo en el reconocio
que llegaste hasta aca.

Y eso es suficiente para pasar.

Por ahora.
""" % player.name_jugador,
		[]
	)

	return "continuar"
