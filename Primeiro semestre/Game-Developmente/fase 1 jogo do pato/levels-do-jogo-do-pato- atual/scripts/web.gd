extends Area2D
# =========================================================
# CONFIGURAÇÕES
# =========================================================
@export var speed := 20
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
@onready var ray = $RayCast2D
# =========================================================
# READY
# =========================================================
func _ready():
	ray.collision_mask = 3
	ray.enabled = true
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

	ray.target_position = direction * speed * delta * 10

	if ray.is_colliding():
		var collider = ray.get_collider()
		if collider and collider.is_in_group("player"):
			collider.web_hit()
			queue_free()
			return
		else:
			queue_free()
			return

	global_position += direction * speed * delta

	for body in get_overlapping_bodies():
		if body.is_in_group("player"):
			body.web_hit()
			queue_free()
			return

	for area in get_overlapping_areas():
		if area.name == "Sword":
			queue_free()
			return

# =========================================================
# COLISÃO
# =========================================================
func _on_body_entered(body):
	if body.is_in_group("player"):
		body.web_hit()
		queue_free()
