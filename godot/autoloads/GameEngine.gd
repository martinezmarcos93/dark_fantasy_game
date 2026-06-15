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
