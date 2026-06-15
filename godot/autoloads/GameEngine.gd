extends Node
## GameEngine — director global del juego.
## Port de game_engine.py. Registrado como Autoload.

var current_level_index: int = 0
var player: Player = null
var modo_lectura: bool = false
var dificultad_global: float = 1.0
var huyo_este_nivel: bool = false

## GameScreen que conduce el juego (la UI persistente). La setea Main al arrancar.
## Ver ADR-007: los niveles son scripts que conducen esta pantalla vía async.
var pantalla = null


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
			"nueva", "lectura":
				modo_lectura = (accion == "lectura")
				await mostrar_intro()
				await crear_personaje()
				await _jugar_demo()
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
	# NOTA: "Continuar" (cargar partida) se agrega al integrar SaveSystem.
	var opciones := ["Nueva partida", "Modo Lectura  [sin combate]", "Créditos", "Salir"]
	var idx: int = await mostrar_nivel("res://assets/images/menu_alt.jpg", texto, opciones)
	match idx:
		0: return "nueva"
		1: return "lectura"
		2: return "creditos"
		_: return "salir"


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
	# NOTA: herencia NG+ (cargar_ng_plus) se aplica al integrar SaveSystem.

	await _elegir_dificultad()


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


## PLACEHOLDER: corre Level1. Se reemplaza por el loop completo jugar()
## (recorre Level1..Level10, _entre_niveles, guardado) en la tarea de engine.
func _jugar_demo() -> void:
	current_level_index = 0
	huyo_este_nivel = false
	var level1: BaseLevel = load("res://scripts/levels/level1.gd").new()
	await level1.jugar(player, self)


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
