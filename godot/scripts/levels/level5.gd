extends BaseLevel
## Level 5 — Las Moradas de los Muertos.
## Port directo de game/levels/level5.py. Textos sagrados — no modificar.
## NOTA: distorsionar_texto() se porta como transformación de texto (igual al
## Python). La versión shader equivalente queda para Fase 5.


func _init() -> void:
	nombre = "Las Moradas de los Muertos"


func _traducir_vocales(p: String) -> String:
	var mapa := {"a": "á", "e": "ë", "i": "ï", "o": "ø", "u": "ù"}
	var out := ""
	for ch in p:
		out += mapa.get(ch, ch)
	return out


func distorsionar_texto(texto: String, player: Player) -> String:
	var psique: Dictionary = player.psique

	if psique["miedo"] > 30:
		texto = texto.to_lower()
		var lineas: Array = []
		for l in texto.split("\n"):
			if l.strip_edges() != "":
				lineas.append("  ".join(l.split(" ", false)))
			else:
				lineas.append(l)
		texto = "\n".join(lineas)

	if psique["corrupcion"] > 40:
		var lineas: Array = []
		for linea in texto.split("\n"):
			var palabras := linea.split(" ")
			var nueva: Array = []
			for i in range(palabras.size()):
				var p: String = palabras[i]
				if p.length() > 5 and i % 3 == 0:
					p = _traducir_vocales(p)
				nueva.append(p)
			lineas.append(" ".join(nueva))
		texto = "\n".join(lineas)

	if psique["lucidez"] > 40:
		texto = "[ " + texto.strip_edges() + " ]"

	return texto


# El Otro — aparece si la psique está equilibrada. Devuelve "muerte" o "".
func _chequear_otro(player: Player, engine) -> String:
	if not player.psique_equilibrada():
		return ""

	await engine.mostrar_nivel(
		"res://assets/images/enemy_otro.jpg",
		"""
Antes de que te adentres en las moradas…

algo te espera en el umbral.

No es una criatura.
No es un guardián.

Es lo que ocurre cuando
todas las partes de vos
están, por primera vez,
en equilibrio.

El Otro.

No podés ignorarlo.
Viene de adentro.
""",
		[]
	)

	var enemy := EnemyFactory.crear_otro()
	var resultado: String = await engine.combate_narrativo(enemy)

	if resultado == "muerte":
		return "muerte"

	# Ofrecer fusión (ending secreto)
	await engine.ofrecer_fusion_con_otro("res://assets/images/enemy_otro.jpg")

	return ""  # Continuar con el nivel


func _chequear_voz_umbral(_player: Player, engine) -> void:
	# La Voz del Umbral — aliado de información. Requiere lucidez >= 30.
	await engine.encuentro_voz_umbral("res://assets/images/npc_voz.jpg")


func jugar(player: Player, engine) -> String:
	# Chequear El Otro (psique equilibrada)
	var resultado_otro: String = await _chequear_otro(player, engine)
	if resultado_otro == "muerte":
		return "muerte"

	# La Voz del Umbral (si lucidez >= 30 y sin aliado)
	await _chequear_voz_umbral(player, engine)

	# Cofre de Eco: basado en si el último combate (Level 4) fue perfecto
	await engine.ofrecer_cofre_eco("res://assets/images/lvl5.jpg")

	var texto := """
El espacio se abre.
Pero no es una sala.
Es… algo indefinido.
No hay suelo.
No hay techo.
Solo puertas.
Decenas.
Cada una distinta.
Algunas rotas.
Otras selladas.
Algunas… respiran.

Sentís que cada una lleva a algo distinto.
Pero también sabés algo más:
No estás eligiendo libremente.
Algo en vos ya decidió.

La voz, por última vez:
"No elegís la puerta. La reconocés."

¿Qué hacés?
"""

	var eleccion: int = await engine.mostrar_nivel(
		"res://assets/images/lvl5.jpg",
		distorsionar_texto(texto, player),
		[
			"Elegir una puerta al azar",
			"Intentar analizar las puertas",
			"No elegir ninguna",
		]
	)

	if eleccion == 0:
		player.registrar_decision("Elegiste una puerta al azar. Siempre estuviste ahí.")
		player.psique["corrupcion"] += 10
		var texto_resultado := """
Elegís.
Sin pensar.
La puerta cede.
Pero al cruzar…
no sentís cambio.
Porque no cruzaste.
Siempre estuviste ahí.
"""
		await engine.mostrar_nivel(
			"res://assets/images/lvl5.jpg",
			distorsionar_texto(texto_resultado, player),
			[]
		)

	elif eleccion == 1:
		player.registrar_decision("Intentaste analizar las puertas. La lógica no aplicaba.")
		player.psique["lucidez"] += 10
		player.psique["culpa"] += 5
		var texto_resultado := """
Observás.
Comparás.
Intentás entender.
Pero las puertas cambian.
Se reconfiguran.
No hay lógica estable.

Entonces entendés:
No es el entorno.
Sos vos.
"""
		await engine.mostrar_nivel(
			"res://assets/images/lvl5.jpg",
			distorsionar_texto(texto_resultado, player),
			[]
		)

	elif eleccion == 2:
		player.registrar_decision("No elegiste ninguna puerta. Las puertas esperaron.")
		player.psique["miedo"] += 15
		var texto_resultado := """
No elegís.
Te quedás.
El tiempo no pasa.
O pasa demasiado.

Las puertas siguen ahí.
Esperando.
Como si supieran…
que eventualmente vas a ceder.
"""
		await engine.mostrar_nivel(
			"res://assets/images/lvl5.jpg",
			distorsionar_texto(texto_resultado, player),
			[]
		)

	return "continuar"
