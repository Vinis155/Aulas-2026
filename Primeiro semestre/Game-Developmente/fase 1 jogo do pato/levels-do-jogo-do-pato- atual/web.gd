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
	queue_free()

# =========================================================
# PROCESS
# =========================================================
func _process(delta):

	# Rotaciona uma vez quando direction for definida
	if not rotated and direction != Vector2.ZERO:
		rotation = direction.angle()
		rotated = true

	global_position += direction * speed * delta

# =========================================================
# COLISÃO
# =========================================================
func _on_body_entered(body):

	if body.is_in_group("player"):
		body.take_damage()
		queue_free()

	elif body.is_in_group("wall"):
		queue_free()
