class_name CombatSystem
extends RefCounted
## CombatSystem — lógica de combate por turnos.
## Port directo de game/combat_system.py (funciones de módulo).
##
## CombatState (datos) vive en CombatState.gd. Acá van las funciones puras
## de resolución + el loop orquestador combate_completo().
##
## IMPORTANTE: comportamiento idéntico al Python. Los textos son sagrados.
## Referencia: game/combat_system.py | Contrato: test_game.py (96 tests)


# ─────────────────────────────────────────
# HELPER: hechizo por id (sobre CombatState.HECHIZOS)
# ─────────────────────────────────────────
static func _hechizo_por_id(id: String) -> Dictionary:
	for h in CombatState.HECHIZOS:
		if h["id"] == id:
			return h
	return {}


# ─────────────────────────────────────────
# TIRADA: 2d6 + stat vs dificultad×2
# Port de tirar(). Con ventaja: 3 dados, suma los dos mayores.
# ─────────────────────────────────────────
static func tirar(stat: int, dificultad: int, ventaja: bool = false) -> Dictionary:
	var resultado: int
	if ventaja:
		var dados := [randi_range(1, 6), randi_range(1, 6), randi_range(1, 6)]
		dados.sort()
		resultado = dados[1] + dados[2] + stat
	else:
		resultado = randi_range(1, 6) + randi_range(1, 6) + stat

	var umbral := dificultad * 2
	return {
		"exito":   resultado >= umbral,
		"critico": resultado >= umbral + 4,
		"tirada":  resultado,
		"umbral":  umbral,
	}


# ─────────────────────────────────────────
# RESOLVER ACCIÓN DEL JUGADOR
# Port directo de resolver_accion_jugador().
# ─────────────────────────────────────────
static func resolver_accion_jugador(accion: String, player: Player, enemy: Enemy, state: CombatState) -> Dictionary:
	var clase: String = player.clase
	var stats: Dictionary = player.stats
	var result := {
		"texto": "", "daño_enemigo": 0, "daño_jugador": 0,
		"ronda_ganada": false, "critico": false, "nuevo_estado": {},
	}

	var ventaja: bool = state.ventaja_activa
	state.ventaja_activa = false

	# ── ACCIÓN UNIVERSAL: RESPIRAR ────────────────────────────
	if accion == "respirar":
		var recuperado := 10
		player.recuperar(0, recuperado)
		result["texto"] = (
			"Tomás distancia. Un momento de calma en medio del combate.\n"
			+ "[ %s +%d ]" % [player.energia_nombre, recuperado]
		)
		result["ronda_ganada"] = false  # Ronda neutral
		return result

	# ── GUERRERO ──────────────────────────────────────────────
	if clase == "Guerrero":

		if accion == "golpe_directo":
			state.defensas_consecutivas = 0
			var t := tirar(stats["fuerza"], enemy.dificultad, ventaja)
			if t["exito"]:
				var daño := randi_range(1, enemy.dificultad) * 4
				if t["critico"]:
					daño *= 2
					result["critico"] = true
					result["texto"] = "CRÍTICO — El golpe fue perfecto. Sin margen de error.\n[ Daño infligido: %d ]" % daño
				else:
					result["texto"] = "Tu golpe conecta. El guardián retrocede.\n[ Daño infligido: %d ]" % daño
				result["daño_enemigo"] = daño
				result["ronda_ganada"] = true
			else:
				var daño_recibido := randi_range(enemy.dificultad, enemy.dificultad * 2) * 2
				result["texto"] = "Fallaste la apertura. Te golpea antes de que puedas conectar.\n[ Daño recibido: %d ]" % daño_recibido
				result["daño_jugador"] = daño_recibido

		elif accion == "defender":
			# Piedra de Eco: éxito garantizado
			if state.proximo_defender_exito:
				state.proximo_defender_exito = false
				var daño_contra := randi_range(1, enemy.dificultad) * 3
				result["critico"] = true
				result["texto"] = (
					"La Piedra de Eco. El Defender es perfecto, inevitable.\n"
					+ "[ Contraataque: %d ]" % daño_contra
				)
				result["daño_enemigo"] = daño_contra
				result["nuevo_estado"]["defensa_activa"] = true
				state.defensas_consecutivas += 1
				if state.defensas_consecutivas >= 2:
					result["nuevo_estado"]["contraataque_disponible"] = true
					result["texto"] += "\n[ Postura: Contraataque Total disponible ]"
			else:
				var t := tirar(stats["resistencia"], enemy.dificultad, ventaja)
				var daño_bloqueado := randi_range(2, 6) * 2
				if t["exito"]:
					var daño_contra := randi_range(1, enemy.dificultad) * 2
					if t["critico"]:
						daño_contra *= 2
						result["critico"] = true
						result["texto"] = "CRÍTICO — Absorbés todo el impacto y contraatacás con fuerza.\n[ Daño bloqueado: %d — Contraataque: %d ]" % [daño_bloqueado, daño_contra]
					else:
						result["texto"] = "Absorbés el golpe y contraatacás.\n[ Daño bloqueado: %d — Contraataque: %d ]" % [daño_bloqueado, daño_contra]
					result["daño_enemigo"] = daño_contra
					result["nuevo_estado"]["defensa_activa"] = true
					state.defensas_consecutivas += 1
					if state.defensas_consecutivas >= 2:
						result["nuevo_estado"]["contraataque_disponible"] = true
						result["texto"] += "\n[ Postura: Contraataque Total disponible ]"
				else:
					state.defensas_consecutivas = 0
					result["nuevo_estado"]["contraataque_disponible"] = false
					var daño_parcial := randi_range(1, enemy.dificultad) * 2
					result["texto"] = "Intentás cubrirte pero el impacto pasa igual.\n[ Daño parcial recibido: %d ]" % daño_parcial
					result["daño_jugador"] = daño_parcial

		elif accion == "contraataque_total":
			state.contraataque_disponible = false
			state.defensas_consecutivas   = 0
			state.uso_especiales = true
			var t := tirar(stats["fuerza"], enemy.dificultad, ventaja)
			var daño := randi_range(enemy.dificultad, enemy.dificultad * 2) * 6
			if t["exito"]:
				if t["critico"]:
					daño *= 2
					result["critico"] = true
					result["texto"] = "CRÍTICO — Contraataque Total. La postura se convierte en devastación.\n[ Daño infligido: %d ]" % daño
				else:
					result["texto"] = "Contraataque Total. Dos rondas de aguante convertidas en un golpe.\n[ Daño infligido: %d ]" % daño
				result["daño_enemigo"] = daño
				result["ronda_ganada"] = true
			else:
				var daño_recibido := randi_range(enemy.dificultad, enemy.dificultad * 2) * 2
				result["texto"] = "El contraataque no salió. La postura se rompió antes de tiempo.\n[ Daño recibido: %d ]" % daño_recibido
				result["daño_jugador"] = daño_recibido

		elif accion == "golpe_cargado":
			state.golpe_cargado_disponible = false
			state.uso_especiales = true
			player.gastar_energia(15)
			var t := tirar(stats["fuerza"], enemy.dificultad, ventaja)
			if t["exito"]:
				var daño := randi_range(enemy.dificultad, enemy.dificultad * 2) * 5
				if t["critico"]:
					daño *= 2
					result["critico"] = true
					result["texto"] = "CRÍTICO — El golpe cargado destruye cualquier defensa.\n[ Daño infligido: %d — Stamina: -%d ]" % [daño, 15]
				else:
					result["texto"] = "El golpe cargado encuentra su blanco. Impacto devastador.\n[ Daño infligido: %d — Stamina: -%d ]" % [daño, 15]
				result["daño_enemigo"] = daño
				result["ronda_ganada"] = true
			else:
				var daño_recibido := randi_range(enemy.dificultad, enemy.dificultad * 2) * 3
				result["texto"] = "El golpe cargado erró. Quedaste expuesto y lo pagaste caro.\n[ Daño recibido: %d — Stamina: -%d ]" % [daño_recibido, 15]
				result["daño_jugador"] = daño_recibido

		elif accion == "furia":
			state.furia_disponible = false
			state.uso_especiales = true
			player.gastar_energia(20)
			var daño := randi_range(enemy.dificultad * 2, enemy.dificultad * 3) * 4
			var daño_propio := randi_range(5, 15)
			result["texto"] = "La furia ignora todo. Golpeás sin control, sin defensa.\n[ Daño infligido: %d — Daño propio: %d — Stamina: -%d ]" % [daño, daño_propio, 20]
			result["daño_enemigo"] = daño
			result["daño_jugador"] = daño_propio
			result["ronda_ganada"] = true

		elif accion == "usar_eco_piedra":
			player.quitar_item("eco_piedra")
			result["texto"] = (
				"La Piedra de Eco vibra y se consume.\n"
				+ "El próximo Defender será perfecto, sin importar la tirada."
			)
			result["nuevo_estado"]["proximo_defender_exito"] = true
			result["ronda_ganada"] = false

	# ── HECHICERO ─────────────────────────────────────────────
	elif clase == "Hechicero":

		if accion == "daga":
			var t := tirar(stats["fuerza"], enemy.dificultad)
			if t["exito"]:
				var daño := randi_range(1, 3) * 2
				result["texto"] = "La daga encuentra un hueco. No es mucho, pero es algo.\n[ Daño infligido: %d ]" % daño
				result["daño_enemigo"] = daño
			else:
				var daño_recibido := randi_range(enemy.dificultad, enemy.dificultad * 2) * 2
				result["texto"] = "Sin magia, la daga no alcanza. Te golpea sin piedad.\n[ Daño recibido: %d ]" % daño_recibido
				result["daño_jugador"] = daño_recibido

		elif accion == "usar_tinta":
			player.quitar_item("tinta")
			player.modificar_psique({"corrupcion": 10})
			# Restaurar un hechizo gastado
			var gastados := []
			for h in state._hechizos_originales:
				if h not in state.hechizos_disponibles:
					gastados.append(h)
			if not gastados.is_empty():
				var restaurado: String = gastados.pick_random()
				state.hechizos_disponibles.append(restaurado)
				var hechizo_nombre: String = _hechizo_por_id(restaurado)["nombre"]
				result["texto"] = (
					"La Tinta del Abismo se consume. Corrupción +10.\n"
					+ "[ %s restaurado ]" % hechizo_nombre
				)
			else:
				result["texto"] = "La Tinta del Abismo se consume. No había hechizos que restaurar.\n[ Corrupción +10 ]"
			result["ronda_ganada"] = false
			state.uso_especiales = true

		else:
			var hechizo := _hechizo_por_id(accion)
			if hechizo.is_empty():
				result["texto"] = "Algo falló. El hechizo no existe."
				return result

			if accion in state.hechizos_disponibles:
				state.hechizos_disponibles.erase(accion)
			player.gastar_energia(hechizo["costo_energia"])
			state.uso_especiales = true

			if enemy.id_enemigo in hechizo["inmune"]:
				var daño_recibido := randi_range(enemy.dificultad, enemy.dificultad * 2) * 2
				result["texto"] = (
					"'%s' no encuentra donde aferrarse.\n" % hechizo["nombre"]
					+ "Este ser no tiene lo que buscás.\nEl rebote te golpea a vos.\n"
					+ "[ Daño recibido: %d ]" % daño_recibido
				)
				result["daño_jugador"] = daño_recibido
				return result

			var efecto: String = hechizo["efecto"]
			var t := tirar(stats["mente"], enemy.dificultad, ventaja)

			if efecto == "daño_alto":
				if t["exito"]:
					var daño := randi_range(enemy.dificultad, enemy.dificultad * 2) * 4
					if t["critico"]:
						daño *= 2
						result["critico"] = true
						result["texto"] = "CRÍTICO — La Palabra de Fuego resuena hasta el hueso.\n[ Daño infligido: %d ]" % daño
					else:
						result["texto"] = "La Palabra de Fuego consume lo que toca.\n[ Daño infligido: %d ]" % daño
					result["daño_enemigo"] = daño
					result["ronda_ganada"] = true
				else:
					var daño_recibido := randi_range(2, enemy.dificultad) * 2
					result["texto"] = "El fuego se apaga antes de llegar. Te quema a vos.\n[ Daño recibido: %d ]" % daño_recibido
					result["daño_jugador"] = daño_recibido

			elif efecto == "defensa":
				result["texto"] = "El Velo de Sombra te envuelve. Próxima ronda: daño reducido."
				result["nuevo_estado"]["defensa_activa"] = true
				result["ronda_ganada"] = false

			elif efecto == "ventaja":
				if t["exito"]:
					result["texto"] = "Resonancia Mental. Encontraste la frecuencia. Próxima tirada con ventaja."
					result["nuevo_estado"]["ventaja_activa"] = true
				else:
					result["texto"] = "La resonancia rebotó. Ruido en tu mente."
					var daño_recibido := randi_range(2, 5) * 2
					result["daño_jugador"] = daño_recibido

			elif efecto == "paralizar":
				if t["exito"]:
					result["texto"] = "Lo nombraste. Se detiene. Una ronda de silencio absoluto."
					result["nuevo_estado"]["enemigo_paralizado"] = true
					result["ronda_ganada"] = true
				else:
					var daño_recibido := randi_range(enemy.dificultad, enemy.dificultad * 2) * 2
					result["texto"] = "El nombre no lo alcanzó. Te encontró a vos en cambio.\n[ Daño recibido: %d ]" % daño_recibido
					result["daño_jugador"] = daño_recibido

			elif efecto == "nuclear":
				var daño := randi_range(enemy.dificultad * 2, enemy.dificultad * 3) * 5
				var daño_propio := randi_range(15, 30)
				result["texto"] = (
					"El Fragmento del Abismo no distingue.\nDestruye todo lo que toca, incluido vos.\n"
					+ "[ Daño infligido: %d — Daño propio: %d ]" % [daño, daño_propio]
				)
				result["daño_enemigo"] = daño
				result["daño_jugador"] = daño_propio
				result["ronda_ganada"] = true

	# ── LADRÓN ────────────────────────────────────────────────
	elif clase == "Ladrón":

		if accion == "observar":
			player.gastar_energia(5)
			var t := tirar(stats["resistencia"], enemy.dificultad)
			if t["exito"]:
				result["texto"] = (
					"Te fundís con la oscuridad. Estudiás cada movimiento.\n"
					+ "[ En posición — próxima ronda: Apuñalar o Estrangular disponibles — Ingenio: -5 ]"
				)
				result["nuevo_estado"]["en_posicion"] = true
			else:
				result["texto"] = "Intentás desaparecer pero algo te delata. No lograste posicionarte.\n[ Ingenio: -5 ]"
				result["nuevo_estado"]["en_posicion"] = false

		elif accion == "apuñalar":
			state.en_posicion = false
			state.uso_especiales = true
			player.gastar_energia(15)
			var t := tirar(stats["resistencia"], enemy.dificultad, true)
			if t["exito"]:
				var daño := randi_range(enemy.dificultad, enemy.dificultad * 2) * 5
				if t["critico"]:
					daño *= 2
					result["critico"] = true
					result["texto"] = "CRÍTICO — Punto vital. El daño es absoluto.\n[ Daño infligido: %d — Ingenio: -15 ]" % daño
				else:
					result["texto"] = "Por la espalda. Sin aviso. Sin defensa posible.\n[ Daño infligido: %d — Ingenio: -15 ]" % daño
				result["daño_enemigo"] = daño
				result["ronda_ganada"] = true
			else:
				var daño_recibido := randi_range(enemy.dificultad, enemy.dificultad * 2) * 3
				result["texto"] = (
					"Te vio en el último momento.\nTu ventaja se convirtió en trampa.\n"
					+ "[ Daño recibido: %d — Ingenio: -15 ]" % daño_recibido
				)
				result["daño_jugador"] = daño_recibido

		elif accion == "estrangular":
			state.en_posicion = false
			state.uso_especiales = true
			player.gastar_energia(10)
			var t := tirar(stats["resistencia"], enemy.dificultad)
			if t["exito"]:
				var daño := randi_range(enemy.dificultad, enemy.dificultad * 2) * 3
				result["texto"] = (
					"Lo atrapás desde atrás. El agarre es firme.\n"
					+ "No puede atacar la próxima ronda.\n[ Daño infligido: %d — Ingenio: -10 ]" % daño
				)
				result["daño_enemigo"] = daño
				result["nuevo_estado"]["_paralizado_siguiente"] = true
				result["ronda_ganada"] = true
			else:
				var daño_recibido := randi_range(enemy.dificultad, enemy.dificultad * 2) * 2
				result["texto"] = "Resiste. Te saca de encima con fuerza bruta.\n[ Daño recibido: %d — Ingenio: -10 ]" % daño_recibido
				result["daño_jugador"] = daño_recibido

		elif accion == "ataque_rapido":
			var t := tirar(stats["resistencia"], enemy.dificultad)
			if t["exito"]:
				var daño := randi_range(1, enemy.dificultad) * 2
				result["texto"] = "Golpe rápido, daño limitado. Pero conectó.\n[ Daño infligido: %d ]" % daño
				result["daño_enemigo"] = daño
			else:
				var daño_recibido := randi_range(enemy.dificultad, enemy.dificultad * 2) * 2
				result["texto"] = "Demasiado lento. Te devuelve el doble.\n[ Daño recibido: %d ]" % daño_recibido
				result["daño_jugador"] = daño_recibido

		elif accion == "huir":
			state.huyo = true
			var energia_rec := randi_range(10, 20)
			var daño_recibido := randi_range(2, enemy.dificultad) * 2
			result["texto"] = (
				"Te alejás. Ganás distancia y tiempo.\n"
				+ "Pero el enemigo no deja ir gratis.\n"
				+ "[ Energía recuperada: %d — Daño recibido: %d ]" % [energia_rec, daño_recibido]
			)
			result["daño_jugador"] = daño_recibido
			result["nuevo_estado"]["energia_recuperada"] = energia_rec

		elif accion == "improvisar":
			var tirada := randi_range(1, 6)
			if tirada >= 5:
				var daño := randi_range(enemy.dificultad, enemy.dificultad * 2) * 3
				result["texto"] = (
					"Sin plan. Sin recursos. Solo instinto.\n"
					+ "Encontraste un hueco que el enemigo no esperaba.\n"
					+ "[ Daño infligido: %d ]" % daño
				)
				result["daño_enemigo"] = daño
				result["ronda_ganada"] = true
			elif tirada >= 3:
				var energia_rec := randi_range(5, 15)
				result["texto"] = (
					"Nada funciona como debería.\n"
					+ "Pero al menos te recomponés un poco.\n"
					+ "[ Ingenio recuperado: %d ]" % energia_rec
				)
				result["nuevo_estado"]["energia_recuperada"] = energia_rec
			else:
				var daño_recibido := randi_range(enemy.dificultad, enemy.dificultad * 2) * 2
				result["texto"] = (
					"Sin plan es sin plan.\n"
					+ "El error fue costoso.\n"
					+ "[ Daño recibido: %d ]" % daño_recibido
				)
				result["daño_jugador"] = daño_recibido

	return result


# ─────────────────────────────────────────
# RESOLVER ATAQUE DEL ENEMIGO
# Port directo de resolver_ataque_enemigo().
# ─────────────────────────────────────────
static func resolver_ataque_enemigo(accion_enemigo: String, enemy: Enemy, player: Player, state: CombatState) -> Dictionary:
	if accion_enemigo == "paralizado":
		return {
			"texto": "%s está detenido. No puede actuar." % enemy.nombre,
			"daño": 0,
		}

	var texto_base: String = enemy.texto_para_ataque(accion_enemigo, player.clase)

	var daño_base: int
	if accion_enemigo == "ataque_pesado" or accion_enemigo == "desesperado":
		daño_base = randi_range(enemy.dificultad, enemy.dificultad * 2) * 3
	elif accion_enemigo == "detectar_sigilo":
		daño_base = randi_range(enemy.dificultad, enemy.dificultad * 2) * 3
		state.en_posicion = false
	elif accion_enemigo == "presencia_psiquica":
		daño_base = randi_range(2, enemy.dificultad) * 2
	else:
		daño_base = randi_range(2, enemy.dificultad) * 3

	if state.defensa_activa:
		daño_base = max(1, daño_base / 2)

	return {
		"texto": texto_base,
		"daño": daño_base,
	}


# ─────────────────────────────────────────
# ACCIONES DISPONIBLES (menú por clase + estado)
# Port directo de acciones_disponibles(). Devuelve Array de [id, label].
# ─────────────────────────────────────────
static func acciones_disponibles(player: Player, state: CombatState, _enemy: Enemy) -> Array:
	var clase: String = player.clase
	var acciones: Array = []

	if clase == "Guerrero":
		acciones.append(["golpe_directo", "Golpe directo"])
		acciones.append(["defender", "Defender y contraatacar"])
		if state.contraataque_disponible:
			acciones.append(["contraataque_total", "Contraataque Total  [postura ✓ — daño alto, gana ronda]"])
		if state.golpe_cargado_disponible and player.vida >= player.vida_max * 0.6:
			if player.energia >= 15:
				acciones.append(["golpe_cargado", "Golpe cargado  [1 uso — 15 ST]"])
		if state.furia_disponible and player.vida <= player.vida_max * 0.4:
			if player.energia >= 20:
				acciones.append(["furia", "Furia ciega  [1 uso — 20 ST, te daña]"])
		# Piedra de Eco
		if player.tiene_item("eco_piedra") and not state.proximo_defender_exito:
			acciones.append(["usar_eco_piedra", "Piedra de Eco  [próximo Defender garantizado]"])

	elif clase == "Hechicero":
		for hid in state.hechizos_disponibles:
			var hechizo := _hechizo_por_id(hid)
			var costo: int = hechizo["costo_energia"]
			if player.energia >= costo:
				acciones.append([hid, "%s — %s  [%d MP]" % [hechizo["nombre"], hechizo["descripcion"], costo]])
		# Tinta del Abismo
		if player.tiene_item("tinta"):
			var gastados := []
			for h in state._hechizos_originales:
				if h not in state.hechizos_disponibles:
					gastados.append(h)
			if not gastados.is_empty():
				acciones.append(["usar_tinta", "Tinta del Abismo  [restaura 1 hechizo — +10 Corrupción]"])
		if acciones.is_empty() or state.hechizos_disponibles.is_empty():
			acciones.append(["daga", "Daga  [sin magia, daño mínimo]"])
		else:
			acciones.append(["daga", "Daga  [daño bajo, gratis]"])

	elif clase == "Ladrón":
		if state.en_posicion:
			if player.energia >= 15:
				acciones.append(["apuñalar", "Apuñalar por la espalda  [posición ✓ — 15 IN]"])
			if player.energia >= 10:
				acciones.append(["estrangular", "Estrangular  [posición ✓ — 10 IN]"])
		else:
			if player.energia >= 5:
				acciones.append(["observar", "Observar — preparar posición  [5 IN]"])
		acciones.append(["ataque_rapido", "Ataque rápido  [daño bajo, gratis]"])
		acciones.append(["huir", "Huir y reagruparse  [recupera Ingenio, recibís daño]"])
		if player.energia < 5 and not state.en_posicion:
			acciones.append(["improvisar", "Improvisar  [gratis — efecto aleatorio]"])

	# Respirar: disponible para todos cuando la energía está baja
	if player.energia <= player.energia_max * 0.3:
		acciones.append(["respirar", "Respirar  [%s +10, ronda neutral]" % player.energia_nombre])

	return acciones


# ─────────────────────────────────────────
# TEXTO DE CIERRE (según rondas ganadas)
# Port directo de texto_cierre(). Devuelve [texto, resultado].
# ─────────────────────────────────────────
static func texto_cierre(state: CombatState, enemy: Enemy, _player: Player) -> Array:
	var rj: int = state.rondas_jugador
	var re: int = state.rondas_enemigo

	if rj > re:
		return [enemy.textos_derrota, "victoria"]
	elif re > rj:
		return [enemy.textos_victoria, "derrota"]
	else:
		return [enemy.texto_empate, "empate"]


# ─────────────────────────────────────────
# COMBATE COMPLETO (loop orquestador)
# Port directo de combate_completo(). async — usa la GameScreen para UI.
# Devuelve "muerte", "vivo".
# ─────────────────────────────────────────
static func combate_completo(enemy: Enemy, player: Player, pantalla) -> String:
	var state := CombatState.new()
	state.inicializar(player, enemy.rondas_max)

	if enemy.id_enemigo == "umbral":
		AudioManager.reproducir("boss")

	# ── Pantalla de intro ─────────────────────────────────────
	pantalla.actualizar_hud(player)
	await pantalla.mostrar_pantalla(enemy.imagen, enemy.texto_intro, [])

	# ── Bonus de El Viajero Perdido (Round 1 gratis) ─────────
	if player.viajero_activo and not player.viajero_usado:
		var daño_viajero := randi_range(8, 16)
		enemy.vida -= daño_viajero
		player.viajero_activo = false
		player.viajero_usado  = true
		var viajero_texto := (
			"\nEl Viajero Perdido aparece antes de que empiece la primera ronda.\n"
			+ "Un golpe rápido, silencioso. Luego desaparece hacia la oscuridad.\n"
			+ "[ Daño infligido: %d ]\n" % daño_viajero
		)
		await pantalla.mostrar_pantalla("res://assets/images/npc_viajero.jpg", viajero_texto, [])

	# ── Loop de rondas ────────────────────────────────────────
	while state.ronda_actual <= state.rondas_max:

		state.enemigo_paralizado = state._paralizado_siguiente
		state._paralizado_siguiente = false
		state.defensa_activa = false

		var acciones := acciones_disponibles(player, state, enemy)
		var ids: Array = []
		var labels: Array = []
		for a in acciones:
			ids.append(a[0])
			labels.append(a[1])

		var inv_txt := ""
		if not player.inventario.is_empty():
			var nombres: Array = []
			for i in player.inventario:
				nombres.append(Player.NOMBRES_ITEMS.get(i, i))
			inv_txt = "  Inventario: " + ", ".join(nombres) + "\n"

		var encabezado := (
			"═══ RONDA %d / %d ═══\n" % [state.ronda_actual, state.rondas_max]
			+ "Rondas ganadas — Vos: %d  |  %s: %d\n" % [state.rondas_jugador, enemy.nombre, state.rondas_enemigo]
			+ "Vida: %d/%d    " % [player.vida, player.vida_max]
			+ "%s: %d/%d" % [player.energia_nombre, player.energia, player.energia_max]
			+ "    Aliento: %d/10\n" % player.aliento
			+ inv_txt
		)

		if state.en_posicion and player.clase == "Ladrón":
			encabezado += "\n[ En posición — podés apuñalar o estrangular ]\n"

		var texto_ronda := encabezado + "\n¿Qué hacés?\n"

		pantalla.actualizar_hud(player)
		var eleccion_idx: int = await pantalla.mostrar_pantalla(enemy.imagen, texto_ronda, labels)

		var accion_id: String
		if eleccion_idx >= 0 and eleccion_idx < ids.size():
			accion_id = ids[eleccion_idx]
		else:
			accion_id = ids[0]

		state.acciones_jugador.append(accion_id)
		var sc: Dictionary = player.stats_combate
		sc["acciones"][accion_id] = sc["acciones"].get(accion_id, 0) + 1

		# Marcar "huyo en este nivel" en el engine
		if accion_id == "huir":
			GameEngine.huyo_este_nivel = true

		var result_jugador := resolver_accion_jugador(accion_id, player, enemy, state)

		for k in result_jugador["nuevo_estado"]:
			if k == "energia_recuperada":
				continue  # no es propiedad de state; se aplica abajo
			state.set(k, result_jugador["nuevo_estado"][k])

		enemy.vida -= result_jugador["daño_enemigo"]
		state.daño_jugador_total += result_jugador["daño_enemigo"]
		player.stats_combate["daño_infligido"] += result_jugador["daño_enemigo"]
		if result_jugador["critico"]:
			player.stats_combate["criticos"] += 1

		if result_jugador["daño_jugador"] > 0:
			var daño_real: int = player.recibir_daño(result_jugador["daño_jugador"])
			state.daño_enemigo_total += daño_real
			player.stats_combate["daño_recibido"] += daño_real
			pantalla.flash_daño()

		if result_jugador["nuevo_estado"].has("energia_recuperada"):
			player.recuperar(0, result_jugador["nuevo_estado"]["energia_recuperada"])

		var accion_enemigo: String = enemy.elegir_accion(state, player.clase)
		var result_enemigo := resolver_ataque_enemigo(accion_enemigo, enemy, player, state)

		var daño_enemigo_real := 0
		if result_enemigo["daño"] > 0:
			daño_enemigo_real = player.recibir_daño(result_enemigo["daño"])
			state.daño_enemigo_total += daño_enemigo_real
			player.stats_combate["daño_recibido"] += daño_enemigo_real
			pantalla.flash_daño()

		var _psique_por_accion := {
			"furia":    {"violencia": 3},
			"abismo":   {"corrupcion": 4},
			"nombre":   {"lucidez": 3},
			"apuñalar": {"violencia": 2},
			"huir":     {"miedo": 2},
		}
		if accion_id in _psique_por_accion:
			player.modificar_psique(_psique_por_accion[accion_id])

		if result_jugador["ronda_ganada"]:
			state.rondas_jugador += 1
			player.stats_combate["rondas_ganadas"] += 1
		elif daño_enemigo_real > result_jugador["daño_enemigo"]:
			state.rondas_enemigo += 1
			player.stats_combate["rondas_perdidas"] += 1

		var resultado_visual := (
			"═══ RESULTADO RONDA %d ═══\n\n" % state.ronda_actual
			+ "— Tu acción:\n%s\n\n" % result_jugador["texto"]
			+ "— %s:\n%s\n" % [enemy.nombre, result_enemigo["texto"]]
			+ "[ Daño recibido: %d ]\n\n" % daño_enemigo_real
			+ "Vida restante: %d/%d\n" % [player.vida, player.vida_max]
		)

		pantalla.actualizar_hud(player)
		await pantalla.mostrar_pantalla(enemy.imagen, resultado_visual, [])

		if not player.alive:
			return "muerte"

		state.ronda_actual += 1

	# ── Cierre narrativo ──────────────────────────────────────
	var cierre := texto_cierre(state, enemy, player)
	var texto_final: String = cierre[0]
	var resultado: String = cierre[1]

	# Bonificaciones de victoria
	var bonuses: Array = []
	if resultado == "victoria":
		player.modificar_psique(enemy.psique_victoria_jugador)
		player.recuperar(5)
		bonuses.append("Vida +5")
		player.ganar_aliento(1)
		bonuses.append("Aliento +1")

		# Perfect: 3/3 rondas ganadas
		player.ultimo_combate_perfecto = (state.rondas_jugador >= state.rondas_max)

		# Sin especiales: +5 energía
		if not state.uso_especiales:
			player.recuperar(0, 5)
			bonuses.append("%s +5" % player.energia_nombre)
	else:
		player.modificar_psique(enemy.psique_derrota_jugador)
		player.ultimo_combate_perfecto = false

	if not bonuses.is_empty():
		texto_final += "\n\n[ %s ]" % " — ".join(bonuses)

	pantalla.actualizar_hud(player)
	await pantalla.mostrar_pantalla(enemy.imagen, texto_final, [])

	# Cartel "Esto tendrá repercusión en tu futuro." (Fase 5).
	await pantalla.mostrar_cartel_psique()
	return "vivo"
