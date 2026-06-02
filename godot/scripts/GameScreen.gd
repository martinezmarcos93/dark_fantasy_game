extends Control
## GameScreen — pantalla de juego. Reemplaza a ui.py.
##
## Construye la UI por código para que las zonas de contenido coincidan
## EXACTAMENTE con los huecos transparentes de ui_frame.png.
##
## Las coordenadas derivan de blender/frame_generator.py (canvas 10×6 unidades
## = 1000×600 px). Blender mide Y desde abajo; Godot desde arriba → se invierte.
##
## API principal (async):
##   var idx = await game_screen.mostrar_pantalla(imagen, texto, opciones)
##   idx = índice de la opción elegida (0-based), o -1 si no había opciones.

# ─────────────────────────────────────────
# RECTÁNGULOS DE CONTENIDO (px, sistema Godot top-down)
# Derivados de frame_generator.py. 1 unidad Blender = 100 px.
# godot_y = 600 - (blender_y * 100)
# ─────────────────────────────────────────
const PAD := 14  # padding interno para que el contenido no toque el marco

# Panel izquierdo — imagen del nivel/enemigo
const IMG_RECT  := Rect2(42, 42, 280, 420)
# Strip HUD inferior izquierdo
const HUD_RECT  := Rect2(42, 468, 280, 90)
# Panel derecho superior — texto narrativo
const TEXT_RECT := Rect2(390, 42, 568, 369)
# Panel derecho inferior — opciones
const OPT_RECT  := Rect2(390, 433, 568, 125)

# ─────────────────────────────────────────
# PALETA (heredada de ui.py)
# ─────────────────────────────────────────
const COL_TEXT  := Color(0.314, 0.549, 0.235)   # 80,140,60  verde apagado
const COL_BTN   := Color(0.431, 0.667, 0.333)   # 110,170,85
const COL_HOVER := Color(0.824, 0.157, 0.157)   # 210,40,40  rojo
const COL_BG    := Color(0.020, 0.020, 0.020)   # casi negro
const COL_HP    := Color(0.70, 0.12, 0.12)
const COL_EN    := Color(0.20, 0.35, 0.70)
const COL_ALI   := Color(0.72, 0.58, 0.20)

const RUTA_FRAME := "res://assets/images/ui_frame.png"
const RUTA_FONT  := "res://assets/fonts/Goth.ttf"

# ─────────────────────────────────────────
# ESTADO
# ─────────────────────────────────────────
signal _eleccion(idx: int)

var _font: FontFile
var _bg: ColorRect
var _level_img: TextureRect
var _frame: TextureRect
var _texto: RichTextLabel
var _opciones_box: VBoxContainer
var _hud_nombre: Label
var _hp_bar: ProgressBar
var _en_bar: ProgressBar
var _ali_bar: ProgressBar

var _typing := false
var _type_speed := 50.0   # caracteres por segundo
var _char_prog := 0.0
var _esperando := false
var _opciones_actuales: Array = []


# ═══════════════════════════════════════════════════════════════
# CONSTRUCCIÓN
# ═══════════════════════════════════════════════════════════════
func _ready() -> void:
	_font = load(RUTA_FONT)
	_construir_ui()


func _construir_ui() -> void:
	# Fondo negro a pantalla completa
	_bg = ColorRect.new()
	_bg.color = COL_BG
	_bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	_bg.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(_bg)

	# Imagen del nivel (debajo del marco → el borde la enmarca)
	_level_img = TextureRect.new()
	_level_img.position = IMG_RECT.position
	_level_img.size     = IMG_RECT.size
	_level_img.expand_mode  = TextureRect.EXPAND_IGNORE_SIZE
	_level_img.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_COVERED
	_level_img.clip_contents = true
	_level_img.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(_level_img)

	# Marco ornamental (encima de la imagen, ignora mouse)
	_frame = TextureRect.new()
	_frame.texture = load(RUTA_FRAME)
	_frame.set_anchors_preset(Control.PRESET_FULL_RECT)
	_frame.expand_mode  = TextureRect.EXPAND_IGNORE_SIZE
	_frame.stretch_mode = TextureRect.STRETCH_SCALE
	_frame.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(_frame)

	# Texto narrativo (encima del marco → siempre legible)
	_texto = RichTextLabel.new()
	_texto.position = TEXT_RECT.position + Vector2(PAD, PAD)
	_texto.size     = TEXT_RECT.size - Vector2(PAD * 2, PAD * 2)
	_texto.bbcode_enabled = true
	_texto.scroll_active  = true
	_texto.fit_content    = false
	_texto.add_theme_font_override("normal_font", _font)
	_texto.add_theme_font_size_override("normal_font_size", 22)
	_texto.add_theme_color_override("default_color", COL_TEXT)
	_texto.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(_texto)

	# Contenedor de opciones (encima del marco)
	_opciones_box = VBoxContainer.new()
	_opciones_box.position = OPT_RECT.position + Vector2(PAD, PAD)
	_opciones_box.size     = OPT_RECT.size - Vector2(PAD * 2, PAD * 2)
	_opciones_box.add_theme_constant_override("separation", 4)
	add_child(_opciones_box)

	# HUD (encima del marco)
	_construir_hud()


func _construir_hud() -> void:
	var hud := VBoxContainer.new()
	hud.position = HUD_RECT.position + Vector2(PAD, PAD - 6)
	hud.size     = HUD_RECT.size - Vector2(PAD * 2, PAD * 2)
	hud.add_theme_constant_override("separation", 2)
	add_child(hud)

	_hud_nombre = Label.new()
	_hud_nombre.add_theme_font_override("font", _font)
	_hud_nombre.add_theme_font_size_override("font_size", 16)
	_hud_nombre.add_theme_color_override("font_color", COL_TEXT)
	_hud_nombre.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	hud.add_child(_hud_nombre)

	_hp_bar  = _crear_barra(hud, COL_HP)
	_en_bar  = _crear_barra(hud, COL_EN)
	_ali_bar = _crear_barra(hud, COL_ALI)


func _crear_barra(parent: Node, color: Color) -> ProgressBar:
	var bar := ProgressBar.new()
	bar.custom_minimum_size = Vector2(0, 14)
	bar.show_percentage = false
	var sb_bg := StyleBoxFlat.new()
	sb_bg.bg_color = Color(0.08, 0.08, 0.08)
	sb_bg.set_border_width_all(1)
	sb_bg.border_color = Color(0.3, 0.3, 0.3)
	var sb_fill := StyleBoxFlat.new()
	sb_fill.bg_color = color
	bar.add_theme_stylebox_override("background", sb_bg)
	bar.add_theme_stylebox_override("fill", sb_fill)
	parent.add_child(bar)
	return bar


# ═══════════════════════════════════════════════════════════════
# API PÚBLICA
# ═══════════════════════════════════════════════════════════════
## Muestra una pantalla y espera la elección del jugador.
## opciones: Array de String. Vacío = pantalla narrativa (espera ESPACIO).
## Devuelve el índice 0-based de la opción, o -1 si no había opciones.
func mostrar_pantalla(imagen: String, texto: String, opciones: Array = []) -> int:
	if imagen != "" and ResourceLoader.exists(imagen):
		_level_img.texture = load(imagen)
	_set_texto(texto)
	_construir_opciones(opciones)
	_esperando = true
	var idx: int = await _eleccion
	_esperando = false
	return idx


## Actualiza el HUD desde el Player.
func actualizar_hud(player: Resource) -> void:
	if player == null:
		return
	_hud_nombre.text = "%s — %s" % [player.name_jugador, player.clase]
	_hp_bar.max_value  = player.vida_max
	_hp_bar.value      = player.vida
	_en_bar.max_value  = player.energia_max
	_en_bar.value      = player.energia
	_ali_bar.max_value = 10
	_ali_bar.value     = player.aliento


# ═══════════════════════════════════════════════════════════════
# TEXTO (typewriter)
# ═══════════════════════════════════════════════════════════════
func _set_texto(t: String) -> void:
	_texto.text = t
	_texto.visible_characters = 0
	_char_prog = 0.0
	_typing = true


func _skip_typing() -> void:
	_texto.visible_characters = -1
	_typing = false


func _process(delta: float) -> void:
	if not _typing:
		return
	_char_prog += _type_speed * delta
	var total := _texto.get_total_character_count()
	if _char_prog >= total:
		_texto.visible_characters = -1
		_typing = false
	else:
		_texto.visible_characters = int(_char_prog)


# ═══════════════════════════════════════════════════════════════
# OPCIONES
# ═══════════════════════════════════════════════════════════════
func _construir_opciones(opciones: Array) -> void:
	for c in _opciones_box.get_children():
		c.queue_free()
	_opciones_actuales = opciones

	for i in range(opciones.size()):
		var btn := Button.new()
		btn.text = "%d. %s" % [i + 1, opciones[i]]
		btn.alignment = HORIZONTAL_ALIGNMENT_LEFT
		btn.flat = true
		btn.add_theme_font_override("font", _font)
		btn.add_theme_font_size_override("font_size", 20)
		btn.add_theme_color_override("font_color", COL_BTN)
		btn.add_theme_color_override("font_hover_color", COL_HOVER)
		btn.add_theme_color_override("font_focus_color", COL_HOVER)
		btn.pressed.connect(_on_boton_pressed.bind(i))
		_opciones_box.add_child(btn)


func _on_boton_pressed(idx: int) -> void:
	if _esperando and not _typing:
		_eleccion.emit(idx)


# ═══════════════════════════════════════════════════════════════
# INPUT (teclado)
# ═══════════════════════════════════════════════════════════════
func _input(event: InputEvent) -> void:
	if not _esperando:
		return

	# Mientras escribe: ESPACIO completa el texto
	if _typing:
		if event.is_action_pressed("interactuar"):
			_skip_typing()
			get_viewport().set_input_as_handled()
		return

	# Texto completo, sin opciones: ESPACIO continúa
	if _opciones_actuales.is_empty():
		if event.is_action_pressed("interactuar"):
			_eleccion.emit(-1)
			get_viewport().set_input_as_handled()
		return

	# Con opciones: teclas 1-4
	for i in range(min(4, _opciones_actuales.size())):
		if event.is_action_pressed("opcion_%d" % (i + 1)):
			_eleccion.emit(i)
			get_viewport().set_input_as_handled()
			return

	# Scroll del texto
	if event.is_action_pressed("scroll_abajo"):
		_texto.get_v_scroll_bar().value += 40
	elif event.is_action_pressed("scroll_arriba"):
		_texto.get_v_scroll_bar().value -= 40
