extends CharacterBody2D

var speed = 160
var jump_velocity = -400
var gravity = 980

var max_jumps = 2
var extra_jumps = 2

func _physics_process(delta):

	var dir = Input.get_axis("left", "right")
	velocity.x = dir * speed

	if not is_on_floor():
		velocity.y += gravity * delta
	else:
		extra_jumps = max_jumps

	if Input.is_action_just_pressed("jump") and extra_jumps > 0:
		velocity.y = jump_velocity
		extra_jumps -= 1

	if is_on_floor():
		extra_jumps = 2
	
	move_and_slide()
