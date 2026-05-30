# =========================================================
# PERSONAGEM TOPDOWN
# =========================================================
extends CharacterBody2D


# =========================================================
# VARIÁVEIS EXPORTADAS
# =========================================================

@export var player_id := 1
@export var skin_frames : SpriteFrames


# =========================================================
# CONFIGURAÇÕES DO PERSONAGEM
# =========================================================

var speed = 50
var dir = Vector2.ZERO
var last_direction = "down"
var health = 3.0
var damage_taken = 0.5
var is_alive = true
var can_take_damage = true

# Espada
var can_attack = true
var is_attacking = false


# =========================================================
# NODES
# =========================================================

@onready var anim: AnimatedSprite2D = $AnimatedSprite2D
@onready var animation_player = $AnimationPlayer
@onready var hand = $Hand
@onready var sword = $Hand/Sword
@onready var sword_sprite = $Hand/Sword/Sprite2D
@onready var sword_collision = $Hand/Sword/CollisionShape2D
@onready var lantern = $Hand/PointLight2D


# =========================================================
# READY
# =========================================================
func _ready():

	if skin_frames != null:
		anim.sprite_frames = skin_frames

	# Player 1 = espada, desativa lanterna
	if player_id == 1:
		lantern.visible = false
		sword.monitoring = true
		sword_collision.disabled = true

	# Player 2 = lanterna, desativa espada
	elif player_id == 2:
		lantern.visible = true
		sword.visible = false
		sword.monitoring = false
		sword_collision.disabled = true

	# Luz ambiente fraca ao redor do player
	_add_ambient_light()


# =========================================================
# LUZ AMBIENTE DO PLAYER
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
	ambient.energy = 0.35
	ambient.color = Color(1.0, 0.9, 0.75)
	ambient.texture_scale = 0.5
	add_child(ambient)


# =========================================================
# PHYSICS PROCESS
# =========================================================
func _physics_process(delta):

	if not is_alive:
		move_and_slide()
		return

	move()
	animations()

	if player_id == 1:
		attack()

	elif player_id == 2:
		rotate_lantern()


# =========================================================
# MOVIMENTAÇÃO
# =========================================================
func move():

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
# ATAQUE - PLAYER 1
# =========================================================
func attack():

	if Input.is_action_just_pressed("p1_attack") and can_attack:

		can_attack = false
		is_attacking = true

		# Ativa hitbox
		sword_collision.disabled = false

		# Rotaciona espada em arco
		var tween = create_tween()
		tween.tween_property(
			hand,
			"rotation_degrees",
			hand.rotation_degrees + 180.0,
			0.25
		)

		await tween.finished

		# Desativa hitbox
		sword_collision.disabled = true
		is_attacking = false

		# Cooldown
		await get_tree().create_timer(0.3).timeout
		can_attack = true


# =========================================================
# LANTERNA - PLAYER 2
# =========================================================
func rotate_lantern():

	# Aponta para o mouse
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
				anim.flip_h = true
			elif dir.x < 0:
				anim.flip_h = false

	else:
		anim.play(last_direction)
		anim.stop()
		anim.frame = 0


# =========================================================
# RECEBER DANO
# =========================================================
func take_damage():

	if not can_take_damage:
		return

	can_take_damage = false
	health -= damage_taken
	animation_player.play("hit")

	print("Vida atual: ", health)

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


# =========================================================
# ESPADA - COLISÃO
# =========================================================
func _on_sword_body_entered(body):

	if body.is_in_group("enemy") and is_attacking:

		# Empurra inimigo
		var push_dir = (body.global_position - global_position).normalized()
		body.velocity += push_dir * 150.0

		# Dano no inimigo
		if body.has_method("take_damage"):
			body.take_damage()


func _on_web_body_entered(body: Node2D) -> void:

	if body.is_in_group("player"):
		body.take_damage()
		queue_free()

	elif body.is_in_group("wall"):
		queue_free()
