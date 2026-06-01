# =========================================================
# PERSONAGEM TOPDOWN - TARTARUGA
# =========================================================
extends CharacterBody2D


@export var player_id := 1
@export var skin_frames : SpriteFrames

@export var lantern_energy := 0.8
@export var lantern_color := Color(1.0, 0.95, 0.7)
@export var lantern_scale := 0.7
@export var lantern_position := Vector2(24.0, 2.0)
@export var lantern_texture_scale := 0.0

var speed = 50
var base_speed = 50
var dir = Vector2.ZERO
var last_direction = "down"
var health = 3.0
var damage_taken = 0.5
var is_alive = true
var can_take_damage = true

var web_hit_count = 0
var is_slowed = false
var is_paralyzed = false

var last_lan_angle := 0.0

@onready var anim: AnimatedSprite2D = $AnimatedSprite2D
@onready var animation_player = $AnimationPlayer
@onready var hand = $Hand
@onready var lantern : PointLight2D = $Hand/PointLight2D


func _ready():
	if skin_frames != null:
		anim.sprite_frames = skin_frames
	_setup_lantern()
	_add_ambient_light()


func _setup_lantern():
	lantern.texture = load("res://sprites/Flashlight_small_range_sprite_sheet/Lanterna ligada.png")
	lantern.energy = lantern_energy
	lantern.color = lantern_color
	lantern.texture_scale = lantern_scale
	lantern.shadow_enabled = true
	lantern.shadow_color = Color(0, 0, 0, 0.8)


func _add_ambient_light():
	var gradient = Gradient.new()
	gradient.colors = [Color(1, 1, 1, 1), Color(1, 1, 1, 0)]
	gradient.offsets = [0.0, 1.0]

	var grad_tex = GradientTexture2D.new()
	grad_tex.gradient = gradient
	grad_tex.fill = GradientTexture2D.FILL_RADIAL
	grad_tex.fill_from = Vector2(0.5, 0.5)
	grad_tex.fill_to = Vector2(1.0, 0.5)
	grad_tex.width = 256
	grad_tex.height = 256

	var ambient = PointLight2D.new()
	ambient.texture = grad_tex
	ambient.energy = 0.15
	ambient.color = Color(1.0, 0.9, 0.75)
	ambient.texture_scale = 0.5
	add_child(ambient)


func _physics_process(_delta):
	if not is_alive:
		move_and_slide()
		return
	move()
	animations()
	rotate_lantern()


func move():
	if is_paralyzed:
		velocity = Vector2.ZERO
		move_and_slide()
		return

	var device = GamepadManager.get_device(player_id)
	var input_dir = Vector2.ZERO

	if device != -1:
		input_dir = Vector2(
			Input.get_joy_axis(device, JOY_AXIS_LEFT_X),
			Input.get_joy_axis(device, JOY_AXIS_LEFT_Y)
		)
		if input_dir.length() < 0.2:
			input_dir = Vector2.ZERO

	dir = input_dir
	input_dir = input_dir.normalized()
	velocity = input_dir * speed
	move_and_slide()


func web_hit():
	web_hit_count += 1

	if web_hit_count == 1:
		is_slowed = true
		speed = base_speed * 0.4
		anim.modulate = Color(0.5, 0.8, 1.0)

	elif web_hit_count >= 2:
		is_paralyzed = true
		speed = 0
		anim.modulate = Color(0.3, 0.6, 1.0)

		await get_tree().create_timer(3.0).timeout

		if is_instance_valid(self):
			is_paralyzed = false
			is_slowed = false
			web_hit_count = 0
			speed = base_speed
			anim.modulate = Color(1, 1, 1)


func rotate_lantern():
	var device = GamepadManager.get_device(player_id)
	if device == -1:
		return

	var lan_dir = Vector2(
		Input.get_joy_axis(device, JOY_AXIS_RIGHT_X),
		Input.get_joy_axis(device, JOY_AXIS_RIGHT_Y)
	)
	if lan_dir.length() > 0.2:
		last_lan_angle = lan_dir.angle()
	hand.rotation = last_lan_angle


func animations():
	if velocity != Vector2.ZERO:
		if abs(dir.y) > abs(dir.x):
			if dir.y > 0:
				anim.play("down")
				last_direction = "down"
			else:
				anim.play("up")
				last_direction = "up"
		else:
			anim.play("side")
			last_direction = "side"
			if dir.x > 0:
				anim.flip_h = false
			elif dir.x < 0:
				anim.flip_h = true
	else:
		if last_direction == "down":
			anim.play("idle_down")
		elif last_direction == "up":
			anim.play("up")
			anim.stop()
			anim.frame = 0
		elif last_direction == "side":
			anim.play("idle_side")


func take_damage():
	if not can_take_damage:
		return

	can_take_damage = false
	health -= damage_taken
	animation_player.play("hit")

	print("Player ", player_id, " Vida atual: ", health)

	if health <= 0:
		die()
		return

	await get_tree().create_timer(0.5).timeout
	can_take_damage = true


func die():
	if not is_alive:
		return

	is_alive = false
	velocity = Vector2.ZERO
	$CollisionShape2D.set_deferred("disabled", true)
	animation_player.play("hit")
	await animation_player.animation_finished
	visible = false
	check_game_over()


func check_game_over():
	await get_tree().create_timer(0.2).timeout

	var players = get_tree().get_nodes_in_group("player")
	var alive_count = 0

	for p in players:
		if is_instance_valid(p) and p.is_alive:
			alive_count += 1

	if alive_count <= 0:
		await get_tree().create_timer(1.0).timeout
		get_tree().reload_current_scene()
