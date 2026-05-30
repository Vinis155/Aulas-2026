extends Node2D

@export var enemy_scene : PackedScene


@export_category("Mapa (limites em pixels)")

@export var map_x_min : float = 8.0
@export var map_x_max : float = 320.0

@export var map_y_min : float = 0.0
@export var map_y_max : float = 160.0



@export_category("Wave Config")

@export var enemies_first_wave : int = 3

@export var enemies_per_wave_increase : int = 1

@export var time_between_waves : float = 3.0


@export_category("Spawn Config")

@export var safe_radius : float = 40.0


@export_category("Loot Config")

@export var drop_chance : float = 0.5


var weapon_scenes = [

	"res://prefabs/crossbow.tscn",
	"res://prefabs/Kunai.tscn",
	"res://prefabs/machine_gun.tscn",
	"res://prefabs/pistol.tscn",
	"res://prefabs/Shotgun.tscn"

]


var starter_weapons = [

	"res://prefabs/crossbow.tscn",
	"res://prefabs/machine_gun.tscn",
	"res://prefabs/pistol.tscn",
	"res://prefabs/Shotgun.tscn"

]

var current_wave : int = 0

var enemies_alive : int = 0

var wave_label : Label


func _ready():

	randomize()

	var canvas = CanvasLayer.new()

	canvas.layer = 10

	add_child(canvas)


	# =====================================================
	# LABEL DA WAVE
	# =====================================================
	wave_label = Label.new()

	wave_label.text = ""

	wave_label.visible = false

	wave_label.position = Vector2(100, 60)

	wave_label.autowrap_mode = TextServer.AUTOWRAP_OFF

	wave_label.custom_minimum_size = Vector2(600, 200)

	wave_label.add_theme_color_override(
		"font_color",
		Color.RED
	)

	wave_label.add_theme_font_size_override(
		"font_size",
		32
	)

	var font = load(
		"res://fonts/RubikWetPaint-Regular.ttf"
	)

	if font:

		wave_label.add_theme_font_override(
			"font",
			font
		)

	canvas.add_child(wave_label)



	await get_tree().process_frame


	# DROP INICIAL
	var center = Vector2(

		(map_x_min + map_x_max) / 2.0,
		(map_y_min + map_y_max) / 2.0

	)

	drop_starter_weapon(center)


	# Pequeno delay
	await get_tree().create_timer(1.0).timeout


	# Inicia primeira wave
	start_next_wave()


# PLAYER
func get_player() -> Node:

	var players = get_tree().get_nodes_in_group(
		"player"
	)

	if players.size() > 0:

		return players[0]

	return null


# POSIÇÃO SEGURA
func get_safe_spawn_position() -> Vector2:

	var player = get_player()

	var attempts = 0


	while attempts < 20:

		var pos = Vector2(

			randf_range(map_x_min, map_x_max),

			randf_range(map_y_min, map_y_max)

		)

		if (
			player == null
			or pos.distance_to(
				player.global_position
			) >= safe_radius
		):

			return pos

		attempts += 1


	return Vector2(

		randf_range(map_x_min, map_x_max),

		randf_range(map_y_min, map_y_max)

	)

# DROP INICIAL
func drop_starter_weapon(pos: Vector2):

	var path = starter_weapons.pick_random()


	if not ResourceLoader.exists(path):

		return


	var packed = load(path)


	if packed == null:

		return


	var weapon = packed.instantiate()


	call_deferred(
		"add_weapon_to_scene",
		weapon,
		pos
	)



func drop_random_weapon(pos: Vector2):

	var path = weapon_scenes.pick_random()


	if not ResourceLoader.exists(path):

		push_warning(
			"Spawner: arma não encontrada em "
			+ path
		)

		return


	var packed = load(path)


	if packed == null:

		push_warning(
			"Spawner: falha ao carregar "
			+ path
		)

		return


	var weapon = packed.instantiate()


	call_deferred(
		"add_weapon_to_scene",
		weapon,
		pos
	)


func add_weapon_to_scene(
	weapon,
	pos
):

	if weapon == null:
		return

	get_tree().current_scene.add_child(
		weapon
	)

	weapon.global_position = pos



func start_next_wave():

	current_wave += 1


	var enemy_count = (
		enemies_first_wave
		+ (current_wave - 1)
		* enemies_per_wave_increase
	)


	wave_label.text = (
		"Wave %d"
		% current_wave
	)

	wave_label.visible = true

	wave_label.modulate.a = 1.0


	await get_tree().create_timer(
		time_between_waves
	).timeout


	var tween = create_tween()

	tween.tween_property(
		wave_label,
		"modulate:a",
		0.0,
		0.5
	)

	await tween.finished

	wave_label.visible = false


	spawn_enemies(enemy_count)



func spawn_enemies(count: int):

	if enemy_scene == null:

		push_error(
			"Spawner: enemy_scene não está configurada no Inspector!"
		)

		return


	enemies_alive = count


	for i in range(count):

		var enemy = enemy_scene.instantiate()

		get_tree().current_scene.add_child(
			enemy
		)

		enemy.global_position = (
			get_safe_spawn_position()
		)

		enemy.died.connect(
			_on_enemy_died
		)



func _on_enemy_died(pos: Vector2):

	enemies_alive -= 1



	if randf() <= drop_chance:

		call_deferred(
			"drop_random_weapon",
			pos
		)


	if enemies_alive <= 0:

		if not is_inside_tree():

			return


		await get_tree().create_timer(
			1.5
		).timeout


		start_next_wave()
