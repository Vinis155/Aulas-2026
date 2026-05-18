extends CharacterBody2D

@onready var sprite = $AnimatedSprite2D

var speed = 40
var direction = Vector2.ZERO
var is_alive = true

func _physics_process(delta: float) -> void:
	if is_alive:
		move()
		anim()

func move():
	direction = Input.get_vector("left", "right", "up", "down")

	if direction != Vector2.ZERO:
		velocity = direction * speed
	else:
		velocity = velocity.move_toward(Vector2.ZERO, speed)

	move_and_slide()

func anim():
	if direction == Vector2.ZERO:
		sprite.play("idle")
	else:
		if abs(direction.x) > abs(direction.y):
			sprite.play("walk_side")

			if direction.x < 0:
				sprite.flip_h = true
			else:
				sprite.flip_h = false
		elif direction.y > 0:
			sprite.play("walk_down")
		else:
			sprite.play("walk_up")
			
func die():
	if is_alive:
		is_alive = false
		sprite.play("death")
		await get_tree().create_timer(3.0).timeout
		get_tree().reload_current_scene()
