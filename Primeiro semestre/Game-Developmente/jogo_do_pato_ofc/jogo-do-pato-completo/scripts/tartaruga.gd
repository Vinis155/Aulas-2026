# =========================================================
# PERSONAGEM TOPDOWN
# =========================================================
extends CharacterBody2D


# =========================================================
# VARIÁVEIS EXPORTADAS
# =========================================================

@export var player_id := 1
@export var skin_frames : SpriteFrames

# Lanterna
@export var lantern_energy := 0.8
@export var lantern_color := Color(1.0, 0.95, 0.7)
@export var lantern_scale := 0.7
@export var lantern_position := Vector2(24.0, 2.0)
@export var lantern_texture_scale := 0.0


# =========================================================
# CONFIGURAÇÕES DO PERSONAGEM
# =========================================================

var speed = 50
var base_speed = 50
var dir = Vector2.ZERO
var last_direction = "down"
var health = 3.0
var damage_taken = 0.5
var is_alive = true
var can_take_damage = true

# Teia
var web_hit_count = 0
var is_slowed = false
var is_paralyzed = false


# =========================================================
# NODES
# =========================================================

@onready var anim: AnimatedSprite2D = $AnimatedSprite2D
@onready var animation_player = $AnimationPlayer
@onready var hand = $Hand
@onready var lantern : PointLight2D = $Hand/PointLight2D


# =========================================================
# READY
# =========================================================
func _ready():

	if skin_frames != null:
		anim.sprite_frames = skin_frames

	_setup_lantern()
	_add_ambient_light()


# =========================================================
# CONFIGURAR LANTERNA
# =========================================================
func _setup_lantern():
	lantern.texture = load("res://sprites/Flashlight_small_range_sprite_sheet/Lanterna ligada.png")
	lantern.energy = lantern_energy
	lantern.color = lantern_color
	lantern.texture_scale = lantern_scale
	lantern.shadow_enabled = true
	lantern.shadow_color = Color(0, 0, 0, 0.8)


# =========================================================
# LUZ AMBIENTE (círculo suave)
# =========================================================
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


# =========================================================
# PHYSICS PROCESS
# =========================================================
func _physics_process(_delta):

	if not is_alive:
		move_and_slide()
		return

	move()
	animations()
	rotate_lantern()


# =========================================================
# MOVIMENTAÇÃO
# =========================================================
func move():

	if is_paralyzed:
		velocity = Vector2.ZERO
		move_and_slide()
		return

	var input_dir = Vector2.ZERO

	if player_id == 1:
		input_dir = Input.get_vector(
			"p1_left", "p1_right",
			"p1_up", "p1_down"
		)

	elif player_id == 2:
		input_dir = Input.get_vector(
			"p2_left", "p2_right",
			"p2_up", "p2_down"
		)

	dir = input_dir
	input_dir = input_dir.normalized()
	velocity = input_dir * speed
	move_and_slide()


# =========================================================
# HIT DA TEIA
# =========================================================
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


# =========================================================
# LANTERNA - aponta para o mouse
# =========================================================
func rotate_lantern():

	var mouse_pos = get_global_mouse_position()
	var angle = (mouse_pos - global_position).angle()
	hand.rotation = angle


# =========================================================
# ANIMAÇÕES
# =========================================================
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


# =========================================================
# RECEBER DANO
# =========================================================
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


# =========================================================
# MORTE
# =========================================================
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


# =========================================================
# GAME OVER
# =========================================================
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
