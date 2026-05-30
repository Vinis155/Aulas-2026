extends Area2D

# =========================================================
# CONFIGURAÇÕES
# =========================================================
@export var speed := 250.0
@export var life_time := 3.0

# =========================================================
# VARIÁVEIS
# =========================================================
var direction = Vector2.ZERO
var rotated = false

# =========================================================
# NODES
# =========================================================
@onready var anim = $AnimatedSprite2D


# =========================================================
# READY
# =========================================================
func _ready():
	anim.play("shoot")

	await get_tree().create_timer(life_time).timeout
	if is_instance_valid(self):
		queue_free()


# =========================================================
# PROCESS
# =========================================================
func _process(delta):

	if not rotated and direction != Vector2.ZERO:
		rotation = direction.angle()
		rotated = true

	global_position += direction * speed * delta

	for body in get_overlapping_bodies():
		if body.is_in_group("player"):
			body.take_damage()
			queue_free()
			return
		elif body.is_in_group("wall"):
			# Só destrói se bater em superfície no mesmo eixo da direção
			queue_free()
			return


func _on_body_entered(body):
	if body.is_in_group("player"):
		body.take_damage()
		queue_free()
	elif body.is_in_group("wall"):
		queue_free()
