# =========================================================
# SPIDER IA
# =========================================================
extends CharacterBody2D


# =========================================================
# CONFIGURAÇÕES
# =========================================================

@export var speed := 40.0
@export var min_time := 1.0
@export var max_time := 3.0


# =========================================================
# VIDA
# =========================================================

@export var max_health := 3.0
var health := max_health
var is_alive := true
var can_take_damage := true


# =========================================================
# VARIÁVEIS
# =========================================================

var target = null
var direction = Vector2.ZERO
var timer = 0.0
var knockback = Vector2.ZERO


# =========================================================
# NODES
# =========================================================

@onready var anim = $AnimatedSprite2D
@onready var animation_player = $AnimationPlayer


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

	if not is_alive:
		return

	if knockback != Vector2.ZERO:
		velocity = knockback
		knockback = knockback.move_toward(Vector2.ZERO, 300 * delta)
		move_and_slide()
		return

	if target != null:
		direction = (target.global_position - global_position).normalized()
	else:
		timer -= delta
		if timer <= 0:
			change_direction()

	velocity = direction * speed
	move_and_slide()

	if get_slide_collision_count() > 0:
		for i in range(get_slide_collision_count()):
			var collision = get_slide_collision(i)
			var body = collision.get_collider()
			if body.is_in_group("player"):
				body.take_damage()
			else:
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
# ANIMAÇÕES
# =========================================================
func animations():

	if not is_alive:
		return

	anim.play("walk")

	if direction.x > 0:
		anim.flip_h = true
	elif direction.x < 0:
		anim.flip_h = false


# =========================================================
# RECEBER DANO
# =========================================================
func take_damage(knock_dir = Vector2.ZERO):

	if not can_take_damage or not is_alive:
		return

	can_take_damage = false
	health -= 1.0
	knockback = knock_dir * 200.0

	print("Spider vida: ", health)

	if health <= 0:
		die()
		return

	animation_player.play("hit")

	await get_tree().create_timer(0.4).timeout
	can_take_damage = true


# =========================================================
# MORTE
# =========================================================
func die():

	is_alive = false
	velocity = Vector2.ZERO

	$CollisionShape2D.set_deferred("disabled", true)

	anim.play("die")

	await get_tree().create_timer(1.0).timeout
	queue_free()


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
		change_direction()
