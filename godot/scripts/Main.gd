extends Node
## Main — punto de entrada del juego.
## Instancia la GameScreen, la cablea al director (GameEngine) y arranca el
## flujo real: Menú → Intro → Creación de personaje → Level1.
## (El loop completo de niveles + guardado se completa en la tarea de engine.)

const GameScreenScene := preload("res://scenes/GameScreen.tscn")

var _gs: Control


func _ready() -> void:
	print("Descenso al Umbral — Godot 4.6 | Arranque: Menú → Intro → Personaje")
	_gs = GameScreenScene.instantiate()
	add_child(_gs)

	GameEngine.pantalla = _gs
	# Esperar un frame a que la GameScreen construya su UI (_ready) antes de usarla.
	await get_tree().process_frame
	await GameEngine.iniciar()
