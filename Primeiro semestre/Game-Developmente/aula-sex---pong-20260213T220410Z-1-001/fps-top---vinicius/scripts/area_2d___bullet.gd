extends Area2D


var speed = 200
var damage = 20

func _ready() -> void:
	
	pass
	
func _physics_process(delta: float) -> void:
	
	position += transform.x * speed * delta
	
	pass	
