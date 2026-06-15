extends Node
## GameEngine — director global del juego.
## Port de game_engine.py. Registrado como Autoload.

var current_level_index: int = 0
var player: Player = null
var modo_lectura: bool = false
var dificultad_global: float = 1.0
var huyo_este_nivel: bool = false
var niveles: Array = []        # BaseLevel × 10 (cargados por cargar_niveles)
var save_slot: int = 0

## GameScreen que conduce el juego (la UI persistente). La setea Main al arrancar.
## Ver ADR-007: los niveles son scripts que conducen esta pantalla vía async.
var pantalla = null

# Imágenes de fondo por nivel (port de _LEVEL_IMGS de game_engine.py)
const LEVEL_IMGS := [
	"res://assets/images/lvl1.jpg", "res://assets/images/lvl2.jpg",
	"res://assets/images/lvl3.jpg", "res://assets/images/lvl4.jpg",
	"res://assets/images/lvl5.jpg", "res://assets/images/lvl6.jpg",
	"res://assets/images/lvl7.jpg", "res://assets/images/lvl8.jpg",
	"res://assets/images/lvl9.jpg", "res://assets/images/lvl10.jpg",
]


# ─────────────────────────────────────────
# NAVEGACIÓN
# ─────────────────────────────────────────
func ir_a_escena(ruta: String) -> void:
	get_tree().change_scene_to_file(ruta)


# ─────────────────────────────────────────
# PANTALLA (conduce la GameScreen única)
# Port de game_engine.mostrar_nivel(). Devuelve el índice 0-based de la
# opción elegida, o -1 si no había opciones (pantalla narrativa).
# (El Python devolvía el string "1".."N"; acá usamos índice — ver ADR-007.)
# ─────────────────────────────────────────
func mostrar_nivel(imagen: String, texto: String, opciones: Array = []) -> int:
	pantalla.actualizar_hud(player)
	return await pantalla.mostrar_pantalla(imagen, texto, opciones)


# ─────────────────────────────────────────
# COMBATE NARRATIVO
# Port de game_engine.combate_narrativo().
# ─────────────────────────────────────────
func combate_narrativo(enemy: Enemy) -> String:
	if modo_lectura:
		await mostrar_nivel(enemy.imagen, enemy.texto_intro, [])
		player.modificar_psique(enemy.psique_victoria_jugador)
		return "vivo"
	enemy.dificultad = max(1, roundi(enemy.dificultad * dificultad_global))
	# Transición al combate: fundir a negro; la intro del combate funde desde negro.
	await pantalla.fundir_a_negro()
	return await CombatSystem.combate_completo(enemy, player, pantalla)


# ─────────────────────────────────────────
# COFRES
# Port de game_engine.ofrecer_cofre_*() y _dar_item().
# ─────────────────────────────────────────
func ofrecer_cofre_eco(_imagen_path: String = "") -> void:
	# Cofre de Eco: solo si el último combate fue perfecto (3/3 rondas).
	if not player.ultimo_combate_perfecto:
		return
	var img := "res://assets/images/chest_eco.jpg"
	var item: String = Player.TIER_MEDIO.pick_random()
	var texto_cofre := (
		"Cofre de Eco.\n\n"
		+ "Ganaste cada ronda.\nEl cofre lo sabe.\n\n"
		+ "Contenido: %s\n" % Player.NOMBRES_ITEMS.get(item, item)
	)
	await _dar_item(img, item, texto_cofre)


func ofrecer_cofre_piedra(_imagen_path: String = "") -> void:
	# Cofre de Piedra: requiere llave de piedra.
	if not player.llave_piedra:
		return
	player.llave_piedra = false
	var img := "res://assets/images/chest_stone.jpg"
	var item: String = Player.TIER_BASICO.pick_random()
	var texto_cofre := (
		"Cofre de Piedra.\n\n"
		+ "La llave encaja en silencio.\nAlgo guardado durante mucho tiempo.\n\n"
		+ "Contenido: %s\n" % Player.NOMBRES_ITEMS.get(item, item)
	)
	await _dar_item(img, item, texto_cofre)


func ofrecer_cofre_umbral(_imagen_path: String = "") -> void:
	# Cofre del Umbral: requiere ≥5 aliento y cofre disponible.
	if not player.cofre_umbral_disponible:
		return
	if player.aliento < 5:
		return
	player.cofre_umbral_disponible = false
	player.gastar_aliento(5)
	var img := "res://assets/images/chest_umbral.jpg"
	var item: String = Player.TIER_ALTO.pick_random()
	var texto_cofre := (
		"Cofre del Umbral.\n\n"
		+ "El Aliento que acumulaste abre esto.\n"
		+ "No cualquiera llega con tanto peso.\n\n"
		+ "Contenido: %s\n" % Player.NOMBRES_ITEMS.get(item, item)
		+ "[ −5 Aliento del Umbral ]\n"
	)
	# Fragmento del ending actual como bonus narrativo
	var ending_preview := determinar_final()
	texto_cofre += "\n— El cofre también muestra un fragmento de tu destino —\n%s…\n" % ending_preview.substr(0, 300)
	await _dar_item(img, item, texto_cofre)


func encuentro_voz_umbral(imagen_path: String) -> void:
	# La Voz del Umbral — aliado de información. Level 5, lucidez ≥ 30.
	if player.psique["lucidez"] < 30:
		return
	if player.aliado_tipo != "":
		return
	player.aliado_tipo = "voz"
	player.modificar_psique({"culpa": 10})
	var ending_texto := determinar_final()
	var psique: Dictionary = player.psique
	var dominante := _stat_dominante(psique)
	var nombres_psique := {
		"violencia": "Violencia", "miedo": "Miedo", "culpa": "Culpa",
		"lucidez": "Lucidez", "corrupcion": "Corrupción",
	}
	var texto := (
		"La voz que siempre estuvo ahí.\n"
		+ "Ahora elige responder.\n\n"
		+ "— Tu destino proyectado —\n\n"
		+ "%s\n\n" % ending_texto
		+ "El factor dominante: %s (%d/100).\n\n" % [nombres_psique.get(dominante, dominante), psique[dominante]]
		+ "Eso dice hacia dónde vas.\n"
		+ "Si querés otro destino, ya sabés qué cambiar.\n\n"
		+ "[ Culpa +10 por saber tu destino ]\n"
	)
	await mostrar_nivel(imagen_path, texto, [])


func ofrecer_fusion_con_otro(imagen_path: String) -> void:
	# Tras derrotar a El Otro, ofrecer fusionarse (ending secreto).
	player.ganar_aliento(2)
	var texto := (
		"El Otro está derrotado.\n\n"
		+ "Pero no del todo.\n\n"
		+ "Todavía está ahí. En el límite.\n"
		+ "Y ofrece algo que ningún enemigo ofreció:\n\n"
		+ "Fusionarte con él.\n\n"
		+ "No desaparecerías.\n"
		+ "Serías más completo.\n"
		+ "Y también menos singular.\n\n"
		+ "[ +2 Aliento del Umbral ]\n"
	)
	var idx: int = await mostrar_nivel(
		imagen_path, texto, ["Fusionarte con El Otro", "Alejarte"]
	)
	if idx == 0:
		player.fusionado_con_otro = true
		player.registrar_decision("Te fusionaste con El Otro. La dualidad terminó.")
		await mostrar_nivel(
			imagen_path,
			"\nNo hay dos voces ahora.\nSolo una.\nMás silenciosa.\nMás completa.\n",
			[]
		)
	else:
		await mostrar_nivel(
			imagen_path,
			"\nTe alejás.\nEl Otro se queda donde estaba.\nSiempre estuvo ahí.\n",
			[]
		)


func _dar_item(img_path: String, item_id: String, texto_cofre: String) -> void:
	if player.inventario.size() < 3:
		player.agregar_item(item_id)
		await mostrar_nivel(img_path, texto_cofre + "\n[ Ítem añadido al inventario ]", [])
	else:
		await mostrar_nivel(img_path, texto_cofre + "\n— Inventario lleno. Elegí qué soltar —", [])
		var labels: Array = []
		for i in player.inventario:
			labels.append("Soltar: %s" % Player.NOMBRES_ITEMS.get(i, i))
		labels.append("Dejar el cofre cerrado")
		var idx: int = await mostrar_nivel(img_path, "", labels)
		if idx >= 0 and idx < player.inventario.size():
			player.inventario[idx] = item_id
			await mostrar_nivel(
				img_path,
				"Intercambiaste. Ahora llevás: %s." % Player.NOMBRES_ITEMS.get(item_id, item_id),
				[]
			)


# ═══════════════════════════════════════════════════════════════
# ARRANQUE — Menú → Intro → Creación de personaje
# Port de game_engine.iniciar() / crear_personaje() y de menu.py / intro.py.
# NOTA: guardado/carga (slots), NG+ y el loop completo de niveles quedan
# para la tarea de "completar el engine". Acá: nueva partida / lectura /
# créditos / salir, encadenando hasta Level1.
# ═══════════════════════════════════════════════════════════════
func iniciar() -> void:
	while true:
		var accion: String = await mostrar_menu()
		match accion:
			"nueva":
				var slot: int = await _elegir_slot("nueva")
				if slot < 0:
					continue
				save_slot = slot
				SaveSystem.borrar_partida(slot)
				current_level_index = 0
				modo_lectura = false
				await mostrar_intro()
				await crear_personaje()
				cargar_niveles()
				await jugar()
			"cargar":
				var slot: int = await _elegir_slot("cargar")
				if slot < 0:
					continue
				save_slot = slot
				if cargar_juego(slot):
					cargar_niveles()
					await jugar()
			"lectura":
				var slot: int = await _elegir_slot("nueva")
				if slot < 0:
					continue
				save_slot = slot
				modo_lectura = true
				SaveSystem.borrar_partida(slot)
				current_level_index = 0
				await mostrar_intro()
				await crear_personaje()
				cargar_niveles()
				await jugar()
				modo_lectura = false
			"creditos":
				await mostrar_creditos()
			"salir":
				get_tree().quit()
				return


func mostrar_menu() -> String:
	AudioManager.reproducir("menu")
	var texto := """
Descenso al Umbral


El mundo se consume en silencio.
Los que descienden no regresan.
Los que regresan... ya no son los mismos.


¿Quién sos vos para intentarlo?
"""
	var hay_guardado := SaveSystem.existe_partida()
	var opciones := ["Nueva partida"]
	if hay_guardado:
		opciones.append("Continuar")
	opciones.append("Modo Lectura  [sin combate]")
	opciones.append("Créditos")
	opciones.append("Salir")

	var idx: int = await mostrar_nivel("res://assets/images/menu_alt.jpg", texto, opciones)

	var mapa := ["nueva"]
	if hay_guardado:
		mapa.append("cargar")
	mapa.append("lectura")
	mapa.append("creditos")
	mapa.append("salir")
	return mapa[idx] if idx >= 0 and idx < mapa.size() else "salir"


func mostrar_intro() -> void:
	var pantallas := [
		["res://assets/images/intro1.jpg", """
Yerma no murió.

Solo olvidó para qué servía
estar viva.

Los dioses se fueron sin aviso.
Sin guerra.
Sin profecía.
Un día sostenían el orden.
Al siguiente, no estaban.

El mundo siguió girando por inercia.

Vos naciste en esa inercia.


[ ESPACIO para continuar ]
"""],
		["res://assets/images/intro2.jpg", """
Existe un lugar debajo de todo.

No en los mapas.
No en los libros sagrados
que quedaron.

Solo en los sueños de los que
están a punto de perder algo.

Lo llaman el Umbral.

Dicen que es una cueva.
Dicen que es una mente.

Dicen que es lo mismo.


[ ESPACIO para continuar ]
"""],
		["res://assets/images/intro3.jpg", """
Hace tres noches
escuchaste algo.

No con los oídos.
Desde adentro.

Una palabra sin sonido.
Una dirección sin nombre.

Esta mañana te encontraste
caminando hacia las afueras.

Sin provisiones.
Sin plan.

Como si una parte de vos
ya hubiera decidido
antes que vos.


[ ESPACIO para continuar ]
"""],
		["res://assets/images/lvl1.jpg", """
La entrada está frente a vos.

Piedra antigua.
Oscuridad total.

El aire que sale de ahí
no huele a tierra ni a muerte.

Huele a algo que no tiene
nombre todavía.

Podés darte vuelta.
Nadie te obliga.

Pero ya sabés
que no vas a hacerlo.


[ ESPACIO para continuar ]
"""],
		["res://assets/images/intro4.jpg", """
Entrás.

El sonido del mundo de afuera
desaparece antes de que hagas
tres pasos.

No es silencio.
Es ausencia de todo lo que
usabas para orientarte.

Aquí no hay arriba ni abajo.
Solo profundidad.

Y algo que te conoce
desde antes de que llegaras.


[ ESPACIO para comenzar ]
"""],
	]
	for p in pantallas:
		await mostrar_nivel(p[0], p[1], [])


func crear_personaje() -> void:
	var texto_clase := """
=== CREACIÓN DE PERSONAJE ===


Elegí tu senda:
"""
	var idx: int = await mostrar_nivel(
		"res://assets/images/lvl1.jpg", texto_clase,
		["Guerrero", "Hechicero", "Ladrón"]
	)
	var clases := ["Guerrero", "Hechicero", "Ladrón"]
	var clase: String = clases[idx] if idx >= 0 and idx < clases.size() else "Errante"

	await _mostrar_retrato_clase(clase)

	var nombre: String = await pantalla.pedir_nombre(clase)
	player = Player.new()
	player.inicializar(nombre, clase)
	player.level = 1

	var psique_previa := SaveSystem.cargar_ng_plus()
	if not psique_previa.is_empty():
		await _aplicar_herencia_ng_plus(psique_previa)

	await _elegir_dificultad()


func _aplicar_herencia_ng_plus(psique_previa: Dictionary) -> void:
	var herencia := {}
	for k in psique_previa:
		var v: int = int(psique_previa[k])
		if v > 0:
			herencia[k] = int(v * 0.20)
	# Filtrar las que quedaron en 0 tras el *0.20
	var herencia_real := {}
	for k in herencia:
		if herencia[k] > 0:
			herencia_real[k] = herencia[k]
	if herencia_real.is_empty():
		return

	player.modificar_psique(herencia_real)

	var lineas := ""
	for k in herencia_real:
		lineas += "  %-12s +%d\n" % [k, herencia_real[k]]
	var texto := """
Algo persistió.

No es un recuerdo exacto.
Es una marca.
Lo que el Umbral te dejó
antes de que empezara este descenso.

%s

Empezás con eso.
Ya era tuyo de antes.
""" % lineas
	await mostrar_nivel("res://assets/images/lvl1.jpg", texto, [])


func _retrato_path(clase: String) -> String:
	match clase:
		"Guerrero":  return "res://assets/images/portrait_warrior.jpg"
		"Hechicero": return "res://assets/images/portrait_mage.jpg"
		"Ladrón":    return "res://assets/images/portrait_rogue.jpg"
	return "res://assets/images/lvl1.jpg"


func _mostrar_retrato_clase(clase: String) -> void:
	var descripciones := {
		"Guerrero": """
La senda del Guerrero.

Fuerza como primera respuesta.
Resistencia como segunda.

Stamina: 40
Recurso más bajo — cada acción especial cuesta.
Golpe Cargado y Furia Ciega son devastadores,
pero no infinitos.

Dos Defenders seguidos desbloquean
el Contraataque Total.

La fuerza no es solo del cuerpo.
""",
		"Hechicero": """
La senda del Hechicero.

Conocimiento como arma.
La mente como campo de batalla.

Magia: 100
El recurso más alto — pero cada hechizo se usa
una sola vez por combate.

Los hechizos más poderosos se desbloquean
a medida que descends.
Nombre Verdadero en nivel 3.
Fragmento del Abismo en nivel 4.

Saber tiene un precio.
""",
		"Ladrón": """
La senda del Ladrón.

Posición como ventaja.
La paciencia como táctica.

Ingenio: 70
Observar primero habilita ataques devastadores.
Sin setup, solo opciones básicas.

Sin Ingenio: Improvisar como última salida.
El resultado es incierto.

No todo se puede planear.
""",
	}
	var texto: String = descripciones.get(clase, "Clase desconocida.")
	await mostrar_nivel(_retrato_path(clase), texto, [])


func _elegir_dificultad() -> void:
	var texto := """
¿Qué tan profundo querés descender?

La dificultad afecta el daño enemigo y las tiradas de combate.
La narrativa y los finales son siempre los mismos.
"""
	var opciones := [
		"Umbral Suave  [enemigos más fáciles]",
		"Umbral Normal  [experiencia diseñada]",
		"Umbral Profundo  [enemigos más duros]",
	]
	var idx: int = await mostrar_nivel("res://assets/images/lvl1.jpg", texto, opciones)
	match idx:
		0: dificultad_global = 0.7
		2: dificultad_global = 1.4
		_: dificultad_global = 1.0


func mostrar_creditos() -> void:
	var bloques := [
		"[center]Descenso al Umbral[/center]",
		"[center]Desarrollo y diseño\nMarcos Martínez[/center]",
		"[center]Inspirado en\nDark Souls  ·  Elden Ring\nPsicología Junguiana\nFilosofía esotérica[/center]",
		"[center]\"El dungeon no es un lugar.\nEs una proyección.\"[/center]",
		"[center][ ESPACIO para volver ][/center]",
	]
	for b in bloques:
		await mostrar_nivel("res://assets/images/menu.jpg", b, [])


# ═══════════════════════════════════════════════════════════════
# LOOP PRINCIPAL DE NIVELES — port de game_engine.jugar()/cargar_niveles()
# ═══════════════════════════════════════════════════════════════
func cargar_niveles() -> void:
	niveles = []
	for i in range(1, 11):
		var script: GDScript = load("res://scripts/levels/level%d.gd" % i)
		niveles.append(script.new())


func jugar() -> void:
	while player.alive and current_level_index < niveles.size():
		huyo_este_nivel = false  # Reset por nivel

		# Transición: fundir a negro entre niveles; el primer mostrar_nivel
		# del nivel funde desde negro al mostrar el nuevo contenido.
		await pantalla.fundir_a_negro()

		var nivel: BaseLevel = niveles[current_level_index]
		var resultado: String = await nivel.jugar(player, self)

		if resultado == "muerte":
			player.morir("Fallaste en la prueba.")
			break

		elif resultado == "continuar":
			# Bonus por no haber huido
			if not huyo_este_nivel:
				player.ganar_aliento(1)

			await _mostrar_resumen_psique()
			await _entre_niveles()  # Gestión de inventario y descanso

			current_level_index += 1
			player.level = current_level_index + 1
			SaveSystem.guardar_partida(player, current_level_index, save_slot)

		else:
			break

	await final_juego()


# ─────────────────────────────────────────
# GESTIÓN ENTRE NIVELES — port de _entre_niveles()
# ─────────────────────────────────────────
func _entre_niveles() -> void:
	var img_path: String = LEVEL_IMGS[min(current_level_index, LEVEL_IMGS.size() - 1)]

	while true:
		var ids: Array = []
		var labels: Array = []

		if player.aliento >= 2:
			ids.append("descanso")
			labels.append("Descanso  [−2 Aliento → +10 HP]  (HP: %d/%d)" % [player.vida, player.vida_max])

		for item in player.inventario:
			if item in Player.ITEMS_ENTRE_COMBATES:
				ids.append("usar_%s" % item)
				labels.append("Usar: %s" % Player.NOMBRES_ITEMS.get(item, item))

		ids.append("continuar")
		labels.append("Continuar al siguiente nivel")

		var nombres: Array = []
		for i in player.inventario:
			nombres.append(Player.NOMBRES_ITEMS.get(i, i))
		var inv_txt: String = ", ".join(nombres) if not nombres.is_empty() else "—"

		var texto := (
			"\n— Entre niveles —\n\n"
			+ "Aliento del Umbral: %d/10\n" % player.aliento
			+ "Inventario: %s\n" % inv_txt
			+ "HP: %d/%d   %s: %d/%d\n\n" % [player.vida, player.vida_max, player.energia_nombre, player.energia, player.energia_max]
			+ "¿Hacés algo antes de continuar?\n"
		)

		var idx: int = await mostrar_nivel(img_path, texto, labels)
		var id_elegido: String = ids[idx] if idx >= 0 and idx < ids.size() else "continuar"

		if id_elegido == "continuar":
			break
		elif id_elegido == "descanso":
			player.gastar_aliento(2)
			player.recuperar(10)
			await mostrar_nivel(
				img_path,
				"\nDescansás un momento. El peso se alivia apenas.\n[ −2 Aliento   +10 HP ]\n",
				[]
			)
		elif id_elegido.begins_with("usar_"):
			var item_id: String = id_elegido.substr(5)
			await _aplicar_item(item_id, img_path)


func _aplicar_item(item_id: String, img_path: String) -> void:
	var consumible: bool = item_id in Player.ITEMS_CONSUMIBLES
	var texto := ""

	if item_id == "antorcha":
		player.modificar_psique({"miedo": -10, "lucidez": 5})
		texto = "La Antorcha arde. La luz revela demasiado.\n[ Miedo −10   Lucidez +5 ]"

	elif item_id == "sal":
		player.modificar_psique({"corrupcion": -15, "culpa": 8})
		texto = "La Sal Consagrada purifica. El precio es moral.\n[ Corrupción −15   Culpa +8 ]\n(consumida)"

	elif item_id == "vendas":
		player.recuperar(25)
		texto = "Las Vendas Viejas. Algo tan simple como sobrevivir.\n[ HP +25 ]\n(consumidas)"

	elif item_id == "espejo":
		var dominante := _stat_dominante(player.psique)
		var val: int = player.psique[dominante]
		var nombres_p := {
			"violencia": "Violencia", "miedo": "Miedo", "culpa": "Culpa",
			"lucidez": "Lucidez", "corrupcion": "Corrupción",
		}
		player.modificar_psique({"miedo": 5})
		texto = (
			"El Fragmento de Espejo muestra lo que sos.\n\n"
			+ "Psique dominante: %s (%d/100)\n\n" % [nombres_p.get(dominante, dominante), val]
			+ "Saber tiene un precio.\n[ Miedo +5 ]\n(consumido)"
		)

	elif item_id == "sangre":
		player.modificar_psique({"culpa": 5})
		player.recuperar(15)
		texto = "Sangre Seca. Funciona. El cuerpo no pregunta de dónde viene.\n[ HP +15   Culpa +5 ]"
		consumible = false  # Reutilizable — no se quita del inventario

	elif item_id == "mapa":
		var prox := current_level_index + 1
		var usos_violentos := (player.contar_usos_accion("furia") + player.contar_usos_accion("apuñalar"))
		var tiene_secreto: bool = (
			prox in [3, 4]
			or (prox in [5, 8] and usos_violentos > 4)
		)
		var texto_mapa := ""
		if tiene_secreto:
			texto_mapa = "El mapa susurra: hay algo que no debería estar en el siguiente nivel."
		else:
			texto_mapa = "El mapa dice: el camino parece despejado."
		texto = "Mapa Roto — %s\n(consumido)" % texto_mapa

	elif item_id == "elixir":
		if player.historial.is_empty():
			await mostrar_nivel(img_path, "El Elixir del Olvido no tiene nada que borrar.\nTu historial está vacío.", [])
			return
		var entries: Array = player.historial
		var labels_mem: Array = []
		for e in entries:
			labels_mem.append("Olvidar: %s…" % e.substr(0, 50) if e.length() > 50 else "Olvidar: %s" % e)
		labels_mem.append("Cancelar")
		var elec: int = await mostrar_nivel(
			img_path,
			"El Elixir del Olvido. Elegí qué borrar:\n[ Lucidez −10 ]\n",
			labels_mem
		)
		if elec >= 0 and elec < entries.size():
			player.gastar_memoria(elec)
			player.modificar_psique({"lucidez": -10})
			var t := "Un recuerdo se disuelve. El Elixir se consume.\n[ Lucidez −10 ]\n(consumido)"
			if player.historial.is_empty():
				t += "\n\nNo recordás nada de lo que hiciste.\nEso también dice algo."
			await mostrar_nivel(img_path, t, [])
		return
	else:
		return

	await mostrar_nivel(img_path, texto, [])
	if consumible:
		player.quitar_item(item_id)


# ─────────────────────────────────────────
# SLOTS Y CARGA — port de _elegir_slot()/cargar_juego()
# ─────────────────────────────────────────
func _elegir_slot(modo: String = "cargar") -> int:
	var slots := SaveSystem.listar_slots()

	if modo == "cargar":
		var labels: Array = []
		var ids: Array = []
		for s in slots:
			if not s["vacio"]:
				labels.append("Slot %d  — %s (%s)  Nivel %d" % [s["slot"] + 1, s["nombre"], s["clase"], s["nivel"]])
				ids.append(s["slot"])
		if ids.is_empty():
			return -1
		var idx: int = await mostrar_nivel("res://assets/images/lvl1.jpg", "\n¿Qué partida querés cargar?\n", labels)
		return ids[idx] if idx >= 0 and idx < ids.size() else ids[0]
	else:
		var labels: Array = []
		for s in slots:
			if s["vacio"]:
				labels.append("Slot %d  [libre]" % [s["slot"] + 1])
			else:
				labels.append("Slot %d  — %s (%s)  [sobreescribir]" % [s["slot"] + 1, s["nombre"], s["clase"]])
		var idx: int = await mostrar_nivel("res://assets/images/lvl1.jpg", "\n¿En qué slot guardás la nueva partida?\n", labels)
		return idx if idx >= 0 and idx < labels.size() else 0


func cargar_juego(slot: int = 0) -> bool:
	player = Player.new()
	if not SaveSystem.cargar_en_player(player, slot):
		return false
	var data := SaveSystem.cargar_partida(slot)
	current_level_index = data.get("nivel_actual", 0)
	return true


# ─────────────────────────────────────────
# PANTALLA DE MUERTE — port de pantalla_muerte()
# ─────────────────────────────────────────
func pantalla_muerte() -> void:
	var clase: String = player.clase
	var nivel: int = current_level_index
	var nom: String = player.name_jugador

	var imagenes := {
		"Guerrero":  "res://assets/images/death_warrior.jpg",
		"Hechicero": "res://assets/images/death_mage.jpg",
		"Ladrón":    "res://assets/images/death_rogue.jpg",
	}
	var imagen_path: String = imagenes.get(clase, "res://assets/images/game_over.jpg")
	AudioManager.reproducir("ambiente")

	var textos_guerrero := [
		"%s.\n\nLa piedra no distingue entre los valientes y los demás.\nSolo entre lo que resiste... y lo que cede.\n\nCediste.\n\nEl Umbral absorbió tu fuerza.\nAhora es suya.\n" % nom,
		"%s.\n\nPeleaste contra vos mismo.\nY perdiste.\n\nNo hay vergüenza en eso.\nSolo hay silencio.\n\nEl reflejo sigue ahí.\nCon tu cara.\nCon tu fuerza.\nSin vos.\n" % nom,
		"%s.\n\nEl Sacerdote no te mató.\nTomó algo.\n\nY sin eso...\nel cuerpo siguió un rato más.\nPero vos ya no estabas adentro.\n" % nom,
		"%s.\n\nLa Sombra Soberana te conocía\nmejor de lo que te conocías vos.\n\nCada derrota que alguna vez tuviste\nya estaba en ella.\n\nAhora también estás vos.\n" % nom,
	]
	var textos_hechicero := [
		"%s.\n\nLa piedra no tiene memoria.\nTenías razón.\n\nPero tampoco tiene piedad.\n\nTu hechizo volvió.\nY fue más honesto que vos.\n" % nom,
		"%s.\n\nEl conocimiento que usaste contra el Reflejo\nera tuyo.\n\nY él te lo devolvió\nmultiplicado por todo lo que sabías.\n\nMoriste de tu propia comprensión.\n" % nom,
		"%s.\n\nIntentaste nombrarlo.\nFallaste.\n\nLo que no puede ser nombrado\ntampoco puede ser detenido.\n\nSe llevó algo tuyo.\nEl nombre que más importaba.\nEl tuyo.\n" % nom,
		"%s.\n\nHabía demasiadas historias en la Sombra.\nNo podías contenerlas todas.\n\nUna mente que lo intenta igual\nse rompe igual.\n\nLa tuya resistió hasta el final.\nEso es suficiente.\nO debería serlo.\n" % nom,
	]
	var textos_ladron := [
		"%s.\n\nSiempre hay alguien que te ve\naunque no quieras ser visto.\n\nEl Guardián no tenía ojos.\nPero te encontró igual.\n\nAlgunas cosas no se pueden esquivar.\nSolo se pueden recibir.\n" % nom,
		"%s.\n\nIntentaste desaparecer.\nEl Reflejo sabía adónde ibas\nantes de que lo supieras vos.\n\nPorque eras predecible.\nNo por tus movimientos.\nPor tus miedos.\n" % nom,
		"%s.\n\nTe vaciaste de intención.\nCasi lo lograste.\n\nPero quedó un rastro.\nPequeño.\nSuficiente.\n\nEl Sacerdote marcó ese rastro.\nY lo que está marcado\nno puede ocultarse más.\n" % nom,
		"%s.\n\nLe diste algo tuyo como señuelo.\nLa Sombra no lo aceptó.\n\nFue por vos directamente.\n\nPorque ya te tenía adentro\ndesde antes de que empezara la pelea.\n" % nom,
	]

	var textos := {
		"Guerrero": textos_guerrero,
		"Hechicero": textos_hechicero,
		"Ladrón": textos_ladron,
	}
	var lista: Array = textos.get(clase, textos_guerrero)
	var idx: int = min(nivel, lista.size() - 1)
	await mostrar_nivel(imagen_path, lista[idx], [])


# ─────────────────────────────────────────
# FINAL DEL JUEGO — port de final_juego()
# ─────────────────────────────────────────
func final_juego() -> void:
	if not player.alive:
		await pantalla_muerte()
		SaveSystem.borrar_partida(save_slot)
		return

	await _mostrar_estadisticas()
	await _mostrar_historial()

	var ending := determinar_final()
	var texto := "\n%s.\n\nTu destino:\n\n%s\n" % [player.name_jugador, ending]
	await mostrar_nivel("res://assets/images/lvl6.jpg", texto, [])
	SaveSystem.guardar_ng_plus(player.psique)
	SaveSystem.borrar_partida(save_slot)


func _mostrar_estadisticas() -> void:
	var sc: Dictionary = player.stats_combate
	var total_rondas: int = sc["rondas_ganadas"] + sc["rondas_perdidas"]
	var winrate: int = int(float(sc["rondas_ganadas"]) / total_rondas * 100) if total_rondas > 0 else 0

	var linea_accion := "Acción más usada:   —"
	if not sc["acciones"].is_empty():
		var accion_top := ""
		var veces_top := -1
		for a in sc["acciones"]:
			if sc["acciones"][a] > veces_top:
				veces_top = sc["acciones"][a]
				accion_top = a
		linea_accion = "Acción más usada:   %s  (%d veces)" % [accion_top, veces_top]

	var mem_txt := ""
	if player.memorias_gastadas > 0:
		mem_txt = "Memorias borradas:  %d\n" % player.memorias_gastadas

	var texto := (
		"\n— Lo que dejaste en el camino —\n\n\n"
		+ "Daño infligido:     %d\n" % sc["daño_infligido"]
		+ "Daño recibido:      %d\n" % sc["daño_recibido"]
		+ "Rondas ganadas:     %d / %d  (%d%%)\n" % [sc["rondas_ganadas"], total_rondas, winrate]
		+ "Golpes críticos:    %d\n" % sc["criticos"]
		+ "%s\n" % linea_accion
		+ "Aliento acumulado:  %d/10\n" % player.aliento
		+ "%s\n" % mem_txt
		+ "Estos números no mienten.\n"
		+ "Aunque vos sí lo hayas hecho.\n\n"
	)
	await mostrar_nivel("res://assets/images/lvl6.jpg", texto, [])


func _rep(ch: String, n: int) -> String:
	# String.repeat(0) lanza error en Godot — guardar el caso vacío.
	return ch.repeat(n) if n > 0 else ""


func _mostrar_resumen_psique() -> void:
	var p: Dictionary = player.psique
	var nombres := {
		"violencia": "Violencia", "miedo": "Miedo", "culpa": "Culpa",
		"lucidez": "Lucidez", "corrupcion": "Corrupción",
	}
	var barras := ""
	for clave in nombres:
		var val: int = p[clave]
		var llenas: int = int(val / 10.0)
		var vacias: int = 10 - llenas
		var barra := _rep("█", llenas) + _rep("░", vacias)
		barras += "%-12s [%s] %3d/100\n" % [nombres[clave], barra, val]

	var aliento_barra := _rep("●", player.aliento) + _rep("○", 10 - player.aliento)
	var nombres_inv: Array = []
	for i in player.inventario:
		nombres_inv.append(Player.NOMBRES_ITEMS.get(i, i))
	var inv_txt: String = ", ".join(nombres_inv) if not nombres_inv.is_empty() else "—"

	var texto := (
		"\n— Estado psicológico —\n\n\n"
		+ "%s\n" % barras
		+ "Aliento del Umbral  [%s] %d/10\n" % [aliento_barra, player.aliento]
		+ "Inventario: %s\n\n" % inv_txt
		+ "Lo que sentís va dejando marca.\n\n"
	)
	var img: String = LEVEL_IMGS[min(current_level_index, LEVEL_IMGS.size() - 1)]
	await mostrar_nivel(img, texto, [])


func _mostrar_historial() -> void:
	if player.historial.is_empty():
		if player.memorias_gastadas > 0:
			await mostrar_nivel(
				"res://assets/images/lvl6.jpg",
				"\nNo recordás nada de lo que hiciste.\nEso también dice algo.\n",
				[]
			)
		return
	var lineas: Array = []
	for d in player.historial:
		lineas.append("— %s" % d)
	var texto := (
		"\nLo que hiciste no desaparece.\nSolo se acumula.\n\n"
		+ "%s\n\n" % "\n".join(lineas)
		+ "Eso sos.\nTodo eso junto.\n"
	)
	await mostrar_nivel("res://assets/images/lvl6.jpg", texto, [])


# ─────────────────────────────────────────
# SISTEMA DE FINALES
# Port directo de game_engine.determinar_final()
# Comportamiento idéntico al Python — no modificar sin revisar test_game.py
# ─────────────────────────────────────────
func determinar_final() -> String:
	# Ending secreto: fusión con El Otro
	if player.fusionado_con_otro:
		return """
El Otro ya no está frente a vos.
Porque ahora sos también él.

No hay tensión.
No hay dualidad.
Solo la quietud de quien finalmente
no tiene nada que esconder de sí mismo.

Algunos llaman a eso paz.
Otros lo llaman vaciamiento.
La diferencia no importa
cuando ya no hay dos voces para discutirlo.
"""

	var psique: Dictionary = player.psique
	var dominante := _stat_dominante(psique)
	var segundo   := _stat_segundo(psique, dominante)
	var val_dom: int   = psique[dominante]
	var val_seg: int   = psique[segundo]
	var co: int        = psique["corrupcion"]

	var combo := [dominante, segundo] if val_seg >= 35 else [dominante, ""]

	# ── Combos dobles ─────────────────────────────────────────────
	var par := _par(combo[0], combo[1])
	if par == _par("miedo", "culpa"):
		return """
No corrés.
No te quedás.
Estás suspendido entre las dos.
El miedo dice: movete.
La culpa dice: no merecés escapar.
Y así…
el tiempo pasa alrededor.
Sin vos adentro.
"""
	if par == _par("violencia", "miedo"):
		return """
Atacás porque tenés miedo.
No porque seas valiente.
Cada golpe es un grito
que nadie escucha.
Incluyéndote.
La violencia no te protegió.
Solo te aisló más rápido.
"""
	if par == _par("culpa", "lucidez"):
		return """
Lo entendés todo.
Cada error.
Cada momento en que pudiste elegir distinto.
La lucidez no te absuelve.
Te hace cómplice
de cada versión tuya
que sabía
y eligió igual.
"""
	if par == _par("miedo", "lucidez"):
		return """
Ves exactamente por qué tenés miedo.
Podés nombrarlo.
Describirlo.
Rastrearlo hasta su origen.
Y aun así…
no desaparece.
Entender no es sanar.
A veces es solo
una forma más precisa de sufrir.
"""
	if par == _par("violencia", "culpa"):
		return """
Golpeaste.
Y después lo lamentaste.
Una y otra vez.
El ciclo no es debilidad.
Es la forma que encontraste
de no quedarte quieto
con lo que hiciste.
El movimiento como anestesia.
Funciona.
Hasta que deja de funcionar.
"""
	if par == _par("corrupcion", "lucidez"):
		return """
Lo ves.
Todo.
Sin filtros.
Sin excusas.
Y aún así…
no te detenés.
Algo en vos entiende.
Y algo en vos elige continuar.
No sos víctima.
No sos héroe.
Sos voluntad.
Y el abismo… ahora tiene ojos.
"""

	# ── Endings por stat dominante único ──────────────────────────
	if dominante == "corrupcion" and co >= 40:
		return """
El silencio ya no te resulta ajeno.
Late contigo.
La cueva… respira como vos.
No entraste a destruir nada.
Entraste a recordar.
Y ahora…
alguien más desciende.
Vos esperás.
"""
	if dominante == "lucidez" and co < 50:
		return """
No hay salida.
Pero tampoco prisión.
Lo que enfrentaste…
no desaparece.
Se integra.
Das un paso.
No hacia afuera.
Sino hacia algo más amplio.
El ciclo… no se rompe.
Se comprende.
"""
	if dominante == "miedo":
		return """
Corrés.
Pero no hay dirección.
Las puertas ya no existen.
El espacio se pliega.
Tu mente intenta sostener algo que ya no tiene forma.
Y entonces…
todo se fragmenta.
Seguís ahí.
Pero ya no sabés qué sos.
"""
	if dominante == "violencia":
		return """
Intentaste destruirlo.
Pero nunca estuvo separado.
Cada golpe fue hacia adentro.
Cada intento… una grieta más.
Hasta que no quedó nada coherente.
Solo impulso.
Solo reacción.
Solo ruptura.
"""
	if dominante == "culpa":
		return """
Recordás.
Una y otra vez.
Cada decisión.
Cada omisión.
Cada instante en el que pudiste ser distinto.
Pero no lo fuiste.
No hay castigo externo.
No hace falta.
Vos ya sos suficiente.
"""
	# Default: psique equilibrada o baja
	return """
Salís.
O al menos… eso parece.
El mundo sigue.
La gente habla.
El tiempo avanza.
Pero algo falta.
No recordás qué.
Y nunca lo harás.
"""


# ─────────────────────────────────────────
# HELPERS INTERNOS PARA LOS FINALES
# ─────────────────────────────────────────
func _stat_dominante(psique: Dictionary) -> String:
	var mejor := ""
	var max_val := -1
	for k in psique:
		if psique[k] > max_val:
			max_val = psique[k]
			mejor = k
	return mejor


func _stat_segundo(psique: Dictionary, excluir: String) -> String:
	var mejor := ""
	var max_val := -1
	for k in psique:
		if k == excluir:
			continue
		if psique[k] > max_val:
			max_val = psique[k]
			mejor = k
	return mejor


# Devuelve un Set de dos stats para comparación sin importar orden
func _par(a: String, b: String) -> Array:
	var arr := [a, b]
	arr.sort()
	return arr
