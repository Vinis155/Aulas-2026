#funcoes em azul sao do sistema e em verde sao conectadas

extends Area2D

@export_category("Movement Settings")

@export_enum("Up", "Down", "Left", "Right")
var move_dir: int

@export var speed = 100

@export_range(50.0, 500.0, 5.0, "Distância máxima de serra")
var distance: float = 50.0

var dir: Vector2

@onready var start_position = global_position

func _ready() -> void:
	set_dir()
	pass
	
func _physics_process(delta: float) -> void:
	move(delta)
	pass

func move(delta):
	
	global_position += dir * speed * delta
	
	if global_position.distance_to(start_position) >= distance:
		dir = -dir
		start_position = global_position
	
func set_dir():
	
	dir = Vector2()
	
	match move_dir:
		0:
			dir = Vector2(0, -1)
		1:
			dir = Vector2(0, 1)
		2:
			dir = Vector2(-1, 0)
		3:
			dir = Vector2(1, 0)
	
	pass
			
			

#queue_free(): deleta o personagem

func _on_area_entered(area: Area2D) -> void:
	
	if area.get_parent().is_in_group("player"):
		area.get_parent().die()
		
	
	pass # Replace with function body.
