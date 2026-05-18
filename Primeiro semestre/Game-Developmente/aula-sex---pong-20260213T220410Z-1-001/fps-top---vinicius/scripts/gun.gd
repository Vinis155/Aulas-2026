extends Node2D

@onready var sprite = $Sprite2D
@onready var player = get_tree().get_first_node_in_group("player")
@onready var bullet_marker = $"Sprite2D/Marker2D-bullet_marker"

@export var bullet_scene : PackedScene

func _ready() -> void:
	await get_tree().create_timer(2.0).timeout
	queue_free()
	pass

func _process(delta: float) -> void:
	if player.is_alive:
		aim()
		shoot()
	
	
func aim():
	
	look_at(get_global_mouse_position())
	
	if get_global_mouse_position().x < global_position.x:
		sprite.scale.y = -1
	else:
		sprite.scale.y = 1	
	
func shoot():
	if Input.is_action_just_pressed("shoot")	 and bullet_scene:
		var bullet = bullet_scene.instantiate()
		
		get_tree().current_scene.add_child(bullet)
		bullet.global_position = bullet_marker.global_position
		bullet.global_rotation = global_rotation
		
	
	pass
