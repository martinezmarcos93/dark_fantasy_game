extends Node
## Main — punto de entrada del juego.
## Por ahora ejecuta un DEMO de GameScreen (Fase 2) para verificar la UI.
## En Fase 4 se reemplaza por el flujo Menu → Intro → niveles.

const GameScreenScene := preload("res://scenes/GameScreen.tscn")

var _gs: Control


func _ready() -> void:
	print("Descenso al Umbral — Godot 4.6 | Fase 2: GameScreen")
	_gs = GameScreenScene.instantiate()
	add_child(_gs)
	_demo()


func _demo() -> void:
	# Player de prueba
	var p := Player.new()
	p.inicializar("Marcos", "Hechicero")
	p.aliento = 4
	GameEngine.player = p
	_gs.actualizar_hud(p)

	# Pantalla de prueba con la estética del juego
	var texto := "[center]Descenso al Umbral[/center]\n\n" \
		+ "El mundo se consume en silencio.\n" \
		+ "Los que descienden no regresan.\n" \
		+ "Los que regresan… ya no son los mismos.\n\n" \
		+ "¿Quién sos para intentarlo?"

	var idx: int = await _gs.mostrar_pantalla(
		"res://assets/images/lvl1.jpg",
		texto,
		["Descender al Umbral", "Volver", "Salir"]
	)
	print("[demo] Opción elegida: ", idx)

	# Segunda pantalla: reacción a la elección
	var reacciones := [
		"Bajás el primer escalón.\nLa oscuridad no te recibe.\nTe reconoce.",
		"Te das vuelta.\nPero el umbral ya quedó adentro tuyo.",
		"Cerrás los ojos.\nEl descenso igual empezó.",
	]
	var r: String = reacciones[idx] if idx >= 0 and idx < reacciones.size() else "…"
	await _gs.mostrar_pantalla("res://assets/images/lvl1.jpg", r, [])

	# ── DEMO DE COMBATE (Fase 3) ──────────────────────────────
	var enemy := EnemyFactory.crear_guardian()
	var resultado: String = await CombatSystem.combate_completo(enemy, p, _gs)
	print("[demo] Resultado del combate: ", resultado)
	print("[demo] Fin del demo.")
