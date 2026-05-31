# =========================================================
# HUD - INTERFACE DO JOGADOR
# Canvas lógico ~288x162 (scale 4.0)
# =========================================================
extends CanvasLayer

@export var level_number: int = 1

const MAX_HEALTH       := 3.0
const COLOR_FULL       := Color(0.95, 0.15, 0.15)
const COLOR_HALF       := Color(1.00, 0.55, 0.10)
const COLOR_EMPTY      := Color(0.22, 0.22, 0.25)
const COLOR_P1_NAME    := Color(0.45, 0.85, 1.00)
const COLOR_P2_NAME    := Color(0.45, 1.00, 0.65)
const COLOR_LEVEL      := Color(1.00, 0.92, 0.45)
const COLOR_BAR_BG     := Color(0.04, 0.04, 0.05, 0.88)

var p1_hearts: Array  = []
var p2_hearts: Array  = []
var pause_panel: Control
var is_paused: bool   = false


# =========================================================
# READY
# =========================================================
func _ready():
	process_mode = Node.PROCESS_MODE_ALWAYS
	_build_hud()


# =========================================================
# PROCESS
# =========================================================
func _process(_delta):
	_update_hearts()
	if Input.is_action_just_pressed("ui_cancel"):
		_toggle_pause()


# =========================================================
# CONSTRUIR HUD
# =========================================================
func _build_hud():
	var root = Control.new()
	root.set_anchors_preset(Control.PRESET_FULL_RECT)
	root.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(root)

	# Fundo da barra superior
	var bar_bg = ColorRect.new()
	bar_bg.color = COLOR_BAR_BG
	bar_bg.set_anchors_preset(Control.PRESET_TOP_WIDE)
	bar_bg.custom_minimum_size = Vector2(0, 14)
	root.add_child(bar_bg)

	# Linha decorativa na base da barra
	var accent = ColorRect.new()
	accent.color = Color(1.0, 0.92, 0.45, 0.35)
	accent.set_anchors_preset(Control.PRESET_TOP_WIDE)
	accent.anchor_top    = 0.0
	accent.anchor_bottom = 0.0
	accent.offset_top    = 13
	accent.offset_bottom = 14
	root.add_child(accent)

	# HBox que preenche a barra toda
	var top_bar = HBoxContainer.new()
	top_bar.set_anchors_preset(Control.PRESET_TOP_WIDE)
	top_bar.custom_minimum_size = Vector2(0, 14)
	top_bar.add_theme_constant_override("separation", 0)
	root.add_child(top_bar)

	# --- Seção esquerda: P1 ---
	var left = HBoxContainer.new()
	left.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	left.add_theme_constant_override("separation", 1)
	left.alignment = BoxContainer.ALIGNMENT_BEGIN
	top_bar.add_child(left)

	var p1_gap = Control.new()
	p1_gap.custom_minimum_size = Vector2(3, 0)
	left.add_child(p1_gap)

	var p1_lbl = _make_label("P1 ", 6, COLOR_P1_NAME)
	left.add_child(p1_lbl)

	for i in 3:
		var h = _make_label("♥", 8, COLOR_FULL)
		left.add_child(h)
		p1_hearts.append(h)

	# --- Seção central: Fase ---
	var center_wrap = Control.new()
	center_wrap.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	top_bar.add_child(center_wrap)

	var level_lbl = _make_label("Fase %d" % level_number, 7, COLOR_LEVEL)
	level_lbl.set_anchors_preset(Control.PRESET_FULL_RECT)
	level_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	level_lbl.vertical_alignment   = VERTICAL_ALIGNMENT_CENTER
	center_wrap.add_child(level_lbl)

	# --- Seção direita: P2 ---
	var right = HBoxContainer.new()
	right.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	right.add_theme_constant_override("separation", 1)
	right.alignment = BoxContainer.ALIGNMENT_END
	top_bar.add_child(right)

	for i in 3:
		var h = _make_label("♥", 8, COLOR_FULL)
		right.add_child(h)
		p2_hearts.append(h)

	var p2_lbl = _make_label(" P2", 6, COLOR_P2_NAME)
	right.add_child(p2_lbl)

	var p2_gap = Control.new()
	p2_gap.custom_minimum_size = Vector2(3, 0)
	right.add_child(p2_gap)

	# Menu de pausa
	_build_pause_menu(root)


# =========================================================
# CONSTRUIR MENU DE PAUSA
# =========================================================
func _build_pause_menu(parent: Control):
	pause_panel = Control.new()
	pause_panel.set_anchors_preset(Control.PRESET_FULL_RECT)
	pause_panel.visible      = false
	pause_panel.process_mode = Node.PROCESS_MODE_ALWAYS
	pause_panel.mouse_filter = Control.MOUSE_FILTER_STOP
	parent.add_child(pause_panel)

	var dim = ColorRect.new()
	dim.color = Color(0.0, 0.0, 0.0, 0.65)
	dim.set_anchors_preset(Control.PRESET_FULL_RECT)
	pause_panel.add_child(dim)

	var center = CenterContainer.new()
	center.set_anchors_preset(Control.PRESET_FULL_RECT)
	pause_panel.add_child(center)

	var panel = PanelContainer.new()
	panel.custom_minimum_size = Vector2(95, 0)
	center.add_child(panel)

	var style = StyleBoxFlat.new()
	style.bg_color            = Color(0.07, 0.07, 0.09, 0.97)
	style.border_color        = Color(1.0, 0.92, 0.45, 0.8)
	style.border_width_left   = 1
	style.border_width_right  = 1
	style.border_width_top    = 1
	style.border_width_bottom = 1
	style.corner_radius_top_left     = 2
	style.corner_radius_top_right    = 2
	style.corner_radius_bottom_left  = 2
	style.corner_radius_bottom_right = 2
	panel.add_theme_stylebox_override("panel", style)

	var margin = MarginContainer.new()
	for side in ["margin_left", "margin_right", "margin_top", "margin_bottom"]:
		margin.add_theme_constant_override(side, 8)
	panel.add_child(margin)

	var vbox = VBoxContainer.new()
	vbox.add_theme_constant_override("separation", 4)
	margin.add_child(vbox)

	var title = _make_label("PAUSADO", 9, COLOR_LEVEL)
	title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	vbox.add_child(title)

	var sep = HSeparator.new()
	vbox.add_child(sep)

	var gap = Control.new()
	gap.custom_minimum_size = Vector2(0, 2)
	vbox.add_child(gap)

	var btn_resume = _pause_btn("Continuar  [ESC]")
	btn_resume.pressed.connect(_toggle_pause)
	vbox.add_child(btn_resume)

	var btn_restart = _pause_btn("Reiniciar Fase")
	btn_restart.pressed.connect(func():
		_unpause()
		get_tree().reload_current_scene()
	)
	vbox.add_child(btn_restart)

	var btn_menu = _pause_btn("Menu Principal")
	btn_menu.pressed.connect(func():
		_unpause()
		get_tree().change_scene_to_file("res://scenes/main_menu.tscn")
	)
	vbox.add_child(btn_menu)


# =========================================================
# ATUALIZAR CORAÇÕES
# =========================================================
func _update_hearts():
	var p1_health := 0.0
	var p2_health := 0.0

	for node in get_tree().get_nodes_in_group("player"):
		if not is_instance_valid(node):
			continue
		var pid = node.get("player_id")
		var hp  = node.get("health")
		if hp == null:
			continue
		if pid == 1:
			p1_health = hp if node.get("is_alive") else 0.0
		elif pid == 2:
			p2_health = hp if node.get("is_alive") else 0.0

	_apply_hearts(p1_hearts, p1_health)
	_apply_hearts(p2_hearts, p2_health)


func _apply_hearts(hearts: Array, hp: float):
	for i in hearts.size():
		var threshold_full := float(i + 1)
		var threshold_half := float(i) + 0.5
		if hp >= threshold_full:
			hearts[i].add_theme_color_override("font_color", COLOR_FULL)
		elif hp >= threshold_half:
			hearts[i].add_theme_color_override("font_color", COLOR_HALF)
		else:
			hearts[i].add_theme_color_override("font_color", COLOR_EMPTY)


# =========================================================
# CONTROLE DE PAUSA
# =========================================================
func _toggle_pause():
	if is_paused:
		_unpause()
	else:
		_pause()


func _pause():
	is_paused = true
	pause_panel.visible = true
	get_tree().paused   = true


func _unpause():
	is_paused           = false
	pause_panel.visible = false
	get_tree().paused   = false


# =========================================================
# HELPERS
# =========================================================
func _make_label(txt: String, size: int, color: Color) -> Label:
	var l = Label.new()
	l.text = txt
	l.add_theme_font_size_override("font_size", size)
	l.add_theme_color_override("font_color", color)
	l.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	return l


func _pause_btn(txt: String) -> Button:
	var b = Button.new()
	b.text = txt
	b.custom_minimum_size = Vector2(85, 12)
	b.add_theme_font_size_override("font_size", 6)
	b.process_mode = Node.PROCESS_MODE_ALWAYS
	return b
