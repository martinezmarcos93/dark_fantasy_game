extends Node
## Captura una pantalla de juego representativa a PNG, para revisar el
## calce del marco sin tener que jugar. Descartable: no forma parte del juego.
const GameScreenScene := preload("res://scenes/GameScreen.tscn")

func _ready() -> void:
	var gs: Control = GameScreenScene.instantiate()
	add_child(gs)
	await get_tree().process_frame

	var p := Player.new()
	p.name_jugador = "Marcos"
	p.clase = "Guerrero"
	p.vida = 17
	p.vida_max = 24
	p.energia = 6
	p.energia_max = 10
	p.aliento = 7
	p.psique = {"violencia": 55, "miedo": 30, "culpa": 10, "lucidez": 5, "corrupcion": 0}
	gs.actualizar_hud(p)

	gs.mostrar_pantalla(
		"res://assets/images/lvl3.jpg",
		"El pasadizo se estrecha hasta obligarte a avanzar de costado.\n\n" +
		"La piedra está tibia. No debería estarlo.\n\n" +
		"Algo respira del otro lado del muro, y su ritmo coincide con el tuyo.",
		["Apoyar la mano contra la piedra tibia",
		 "Seguir de largo sin mirar",
		 "Hablarle a lo que respira"])

	gs._skip_typing()
	for i in range(6):
		await get_tree().process_frame
	await RenderingServer.frame_post_draw
	var img := get_viewport().get_texture().get_image()
	img.save_png("res://preview_ui.png")
	print("captura guardada")
	get_tree().quit()
