extends RigidBody2D

var speed = 500

var dir = [-1,1]


func _ready() -> void:
	
	Reset()
	
	pass

func _physics_process(delta: float) -> void:
	
	Score()
	
	pass
	
func Reset():
	
	global_position = get_viewport_rect().size /2
	
	freeze = true
	await get_tree().create_timer(1).timeout
	freeze = false
	
	apply_central_impulse(Vector2 (dir.pick_random() * speed, dir.pick_random() * speed))
	
	pass
	
func Score():
	
	if global_position.x >= get_viewport_rect().size.x:
		Reset()
	if global_position.x <= 0:
		Reset() 
	pass
