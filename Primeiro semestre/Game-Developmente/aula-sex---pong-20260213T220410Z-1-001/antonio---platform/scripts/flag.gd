extends Area2D

@export var next_level: PackedScene


func _on_area_entered(area: Area2D) -> void:
	
	if area.get_parent().is_in_group("Player"):
		get_tree().call_deferred("change_scene_to_packed",next_level)	
	
	pass # Replace with function body.
