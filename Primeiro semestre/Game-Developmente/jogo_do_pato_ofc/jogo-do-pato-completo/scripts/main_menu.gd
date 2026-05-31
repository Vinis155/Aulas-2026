# =========================================================
# MENU PRINCIPAL
# Canvas lógico: ~288x162px (1152x648 padrão / scale 4.0)
# Fontes em px lógicos — aparece 4x maior na tela física
# =========================================================
extends Control

const SAVE_PATH = "user://settings.cfg"

var settings_panel: Control
var master_slider: HSlider
var music_slider: HSlider
var sfx_slider: HSlider
var cfg := ConfigFile.new()


# =========================================================
# READY
# =========================================================
func _ready():
	_setup_audio_buses()
	_load_settings()
	_build_ui()


# =========================================================
# AUDIO BUSES
# =========================================================
func _setup_audio_buses():
	if AudioServer.get_bus_index("Music") == -1:
		AudioServer.add_bus()
		var idx = AudioServer.get_bus_count() - 1
		AudioServer.set_bus_name(idx, "Music")
		AudioServer.set_bus_send(idx, "Master")

	if AudioServer.get_bus_index("SFX") == -1:
		AudioServer.add_bus()
		var idx = AudioServer.get_bus_count() - 1
		AudioServer.set_bus_name(idx, "SFX")
		AudioServer.set_bus_send(idx, "Master")


# =========================================================
# CONFIGURAÇÕES
# =========================================================
func _load_settings():
	if cfg.load(SAVE_PATH) == OK:
		_set_vol("Master", cfg.get_value("audio", "master", 1.0))
		_set_vol("Music",  cfg.get_value("audio", "music",  1.0))
		_set_vol("SFX",    cfg.get_value("audio", "sfx",    1.0))


func _save_settings():
	cfg.set_value("audio", "master", master_slider.value)
	cfg.set_value("audio", "music",  music_slider.value)
	cfg.set_value("audio", "sfx",    sfx_slider.value)
	cfg.save(SAVE_PATH)


func _set_vol(bus: String, linear: float):
	var idx = AudioServer.get_bus_index(bus)
	if idx != -1:
		AudioServer.set_bus_volume_db(idx, linear_to_db(max(linear, 0.0001)))


func _get_linear(bus: String) -> float:
	var idx = AudioServer.get_bus_index(bus)
	return db_to_linear(AudioServer.get_bus_volume_db(idx)) if idx != -1 else 1.0


# =========================================================
# CONSTRUIR UI
# =========================================================
func _build_ui():
	set_anchors_preset(Control.PRESET_FULL_RECT)

	var bg = ColorRect.new()
	bg.color = Color(1.0, 0.449, 0.538, 1.0)
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(bg)

	var center = CenterContainer.new()
	center.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(center)

	var vbox = VBoxContainer.new()
	vbox.add_theme_constant_override("separation", 4)
	center.add_child(vbox)

	# Título — 10px lógico = 40px na tela
	var title = Label.new()
	title.text = "The Trinket Store Escape"
	title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	title.add_theme_font_size_override("font_size", 10)
	title.add_theme_color_override("font_color", Color(0.013, 0.009, 0.0, 1.0))
	vbox.add_child(title)

	var gap = Control.new()
	gap.custom_minimum_size = Vector2(0, 6)
	vbox.add_child(gap)

	# Botões — 7px lógico = 28px na tela, 80x14 lógico = 320x56 na tela
	var btn_play = _btn("Jogar")
	btn_play.pressed.connect(_on_play)
	vbox.add_child(btn_play)

	var btn_cfg = _btn("Configuracoes")
	btn_cfg.pressed.connect(_on_toggle_settings)
	vbox.add_child(btn_cfg)

	var btn_quit = _btn("Sair")
	btn_quit.pressed.connect(get_tree().quit)
	vbox.add_child(btn_quit)

	settings_panel = _build_settings_panel()
	settings_panel.visible = false
	add_child(settings_panel)


func _btn(label: String) -> Button:
	var b = Button.new()
	b.text = label
	b.custom_minimum_size = Vector2(80, 14)
	b.add_theme_font_size_override("font_size", 7)
	return b


# =========================================================
# PAINEL DE CONFIGURAÇÕES
# Overlay full-rect + CenterContainer para centralizar sempre
# =========================================================
func _build_settings_panel() -> Control:
	# Overlay cobre a tela toda e bloqueia cliques no menu atrás
	var overlay = Control.new()
	overlay.set_anchors_preset(Control.PRESET_FULL_RECT)
	overlay.mouse_filter = Control.MOUSE_FILTER_STOP

	var dim = ColorRect.new()
	dim.color = Color(0, 0, 0, 0.55)
	dim.set_anchors_preset(Control.PRESET_FULL_RECT)
	overlay.add_child(dim)

	var center = CenterContainer.new()
	center.set_anchors_preset(Control.PRESET_FULL_RECT)
	overlay.add_child(center)

	var panel = PanelContainer.new()
	panel.custom_minimum_size = Vector2(160, 0)
	center.add_child(panel)

	var margin = MarginContainer.new()
	for side in ["margin_left", "margin_right", "margin_top", "margin_bottom"]:
		margin.add_theme_constant_override(side, 8)
	panel.add_child(margin)

	var vbox = VBoxContainer.new()
	vbox.add_theme_constant_override("separation", 5)
	margin.add_child(vbox)

	var title = Label.new()
	title.text = "Configuracoes de Audio"
	title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	title.add_theme_font_size_override("font_size", 7)
	vbox.add_child(title)

	# Sliders — valor linear 0..1, bus em dB
	master_slider = _slider_row(vbox, "Geral",  _get_linear("Master"))
	master_slider.value_changed.connect(func(v): _set_vol("Master", v); _save_settings())

	music_slider = _slider_row(vbox, "Musica", _get_linear("Music"))
	music_slider.value_changed.connect(func(v): _set_vol("Music", v); _save_settings())

	sfx_slider = _slider_row(vbox, "SFX",    _get_linear("SFX"))
	sfx_slider.value_changed.connect(func(v): _set_vol("SFX", v); _save_settings())

	var gap = Control.new()
	gap.custom_minimum_size = Vector2(0, 3)
	vbox.add_child(gap)

	var btn_close = _btn("Fechar")
	btn_close.pressed.connect(_on_toggle_settings)
	vbox.add_child(btn_close)

	return overlay


func _slider_row(parent: Control, label_text: String, initial: float) -> HSlider:
	var row = HBoxContainer.new()
	row.add_theme_constant_override("separation", 4)
	parent.add_child(row)

	var lbl = Label.new()
	lbl.text = label_text
	lbl.custom_minimum_size = Vector2(40, 0)
	lbl.add_theme_font_size_override("font_size", 6)
	row.add_child(lbl)

	var slider = HSlider.new()
	slider.min_value = 0.0
	slider.max_value = 1.0
	slider.step = 0.01
	slider.value = clampf(initial, 0.0, 1.0)
	slider.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	row.add_child(slider)

	return slider


# =========================================================
# CALLBACKS
# =========================================================
func _on_play():
	get_tree().change_scene_to_file("res://level_1.tscn")


func _on_toggle_settings():
	settings_panel.visible = not settings_panel.visible
