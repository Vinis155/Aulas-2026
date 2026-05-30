extends CharacterBody2D

# =========================================================
# CONFIGURAÇÕES
# =========================================================
@export var speed := 35.0
@export var keep_distance := 120.0
@export var min_time := 1.0
@export var max_time := 3.0
@export var web_scene : PackedScene

# =========================================================
# VARIÁVEIS
# =========================================================
var target = null
var direction = Vector2.ZERO
var timer = 0.0
var can_shoot = true
var is_shooting = false
var last_flip = false

# =========================================================
# NODES
# =========================================================
@onready var anim = $AnimatedSprite2D
@onready var shoot_point = $Marker2D
@onready var shoot_timer = $ShootTimer


# =========================================================
# READY
# =========================================================
func _ready():
	randomize()
	change_direction()


# =========================================================
# PROCESS
# =========================================================
func _physics_process(delta):

	if target != null and is_instance_valid(target) and target.is_alive:
		var distance = global_position.distance_to(target.global_position)
		if distance > keep_distance:
			direction = (target.global_position - global_position).normalized()
		else:
			direction = Vector2.ZERO
			if can_shoot:
				shoot_web()
	else:
		if target != null and not is_instance_valid(target):
			target = null
			change_direction()
		timer -= delta
		if timer <= 0:
			change_direction()

	velocity = direction * speed
	move_and_slide()

	# =========================================
	# COLISÕES
	# =========================================
	if get_slide_collision_count() > 0:
		for i in range(get_slide_collision_count()):
			var collision = get_slide_collision(i)
			var body = collision.get_collider()
			if body.is_in_group("player"):
				body.take_damage()
			else:
				if target == null:
					var normal = collision.get_normal()
					direction = (direction + normal * 2.0).normalized()

	animations()


# =========================================================
# TROCAR DIREÇÃO
# =========================================================
func change_direction():
	timer = randf_range(min_time, max_time)
	direction = [
		Vector2.LEFT,
		Vector2.RIGHT,
		Vector2.UP,
		Vector2.DOWN
	].pick_random()


# =========================================================
# ATIRAR TEIA
# =========================================================
func shoot_web():
	if target == null:
		return
	if web_scene == null:
		return

	can_shoot = false
	is_shooting = true

	last_flip = anim.flip_h
	anim.flip_h = not anim.flip_h

	await get_tree().create_timer(0.2).timeout

	if target == null or not is_instance_valid(target):
		is_shooting = false
		anim.flip_h = last_flip
		return

	var web = web_scene.instantiate()
	get_tree().current_scene.add_child(web)
	web.global_position = shoot_point.global_position
	web.direction = (target.global_position - global_position).normalized()

	shoot_timer.start()

	await get_tree().create_timer(0.2).timeout

	anim.flip_h = last_flip
	is_shooting = false


# =========================================================
# ANIMAÇÕES
# =========================================================
func animations():
	anim.play("walk")

	if is_shooting:
		return

	if target != null:
		anim.flip_h = target.global_position.x < global_position.x
		last_flip = anim.flip_h
	else:
		if direction == Vector2.LEFT:
			anim.flip_h = false
			last_flip = false
		elif direction == Vector2.RIGHT:
			anim.flip_h = true
			last_flip = true


# =========================================================
# PLAYER ENTROU NA VISÃO
# =========================================================
func _on_vision_area_body_entered(body):
	if body.is_in_group("player"):
		target = body


# =========================================================
# PLAYER SAIU DA VISÃO
# =========================================================
func _on_vision_area_body_exited(body):
	if body == target:
		target = null
		direction = Vector2.ZERO
		change_direction()


# =========================================================
# COOLDOWN DO TIRO
# =========================================================
func _on_shoot_timer_timeout():
	can_shoot = true
