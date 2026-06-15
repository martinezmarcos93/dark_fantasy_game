extends BaseLevel
## Level 8 — El Rio de Recuerdos.
## Port directo de game/levels/level8.py. Textos sagrados — no modificar.
## Flujo estándar (combate → psicológica): usa jugar() de BaseLevel.


func _init() -> void:
	nombre = "El Rio de Recuerdos"


func fase_combate(_player: Player, engine) -> String:
	var enemy := EnemyFactory.crear_archivista()
	return await engine.combate_narrativo(enemy)


func fase_psicologica(player: Player, engine) -> void:
	player.recuperar(4, 8)

	# Cofre de Piedra si tiene llave (del Level 7)
	await engine.ofrecer_cofre_piedra("res://assets/images/chest_stone.jpg")

	var texto := """
El río no tiene corriente.

Sus aguas reflejan momentos
que reconocés sin querer recordar.

Hay algo flotando.
Un objeto.
No sabés qué es hasta que lo ves.

Es algo que perdiste.
O que abandonaste.
La diferencia importa
y no la sabés.

La voz del río:
"¿Lo tomás?"

¿Qué hacés?
"""

	var eleccion: int = await engine.mostrar_nivel(
		"res://assets/images/lvl8.jpg",
		texto,
		[
			"Entrar al rio y tomarlo.",
			"Observarlo desde la orilla sin tocarlo.",
			"Hundirlo deliberadamente.",
		]
	)

	if eleccion == 0:
		player.registrar_decision("Entraste al rio de recuerdos y recuperaste lo que estaba flotando.")
		player.psique["lucidez"] += 10
		player.psique["culpa"] += 10
		await engine.mostrar_nivel(
			"res://assets/images/lvl8.jpg",
			"""
Entrás.

El agua es fría pero no duele.

Tomás el objeto.
Al sostenerlo recordás
no solo qué era
sino quién eras cuando lo tenías.

No es el mismo.
No sos el mismo.

Pero ahora ambos están en el mismo lugar.
""",
			[]
		)

	elif eleccion == 1:
		player.registrar_decision("Observaste desde la orilla lo que flotaba en el rio.")
		player.psique["miedo"] += 8
		player.psique["lucidez"] += 8
		await engine.mostrar_nivel(
			"res://assets/images/lvl8.jpg",
			"""
Te quedás en la orilla.

Lo mirás.

El objeto flota sin alejarse.
Como si esperara.

No tomarlo también es una decisión.
Una que entendés
solo parcialmente.

El río sigue.
El objeto también.
""",
			[]
		)

	elif eleccion == 2:
		player.registrar_decision("Hundiste deliberadamente lo que flotaba en el rio.")
		player.psique["violencia"] += 10
		player.psique["corrupcion"] += 8
		player.ganar_aliento(1)  # Elección peligrosa
		await engine.mostrar_nivel(
			"res://assets/images/lvl8.jpg",
			"""
Lo hundís.

Con intención.

El objeto desaparece bajo el agua.
El reflejo no.

Sigue ahí.
Mirándote desde abajo.

Algunas cosas no se hunden.
Solo se profundizan.

[ +1 Aliento del Umbral ]
""",
			[]
		)
