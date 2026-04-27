extends Area2D


func _on_area_entered(area: Area2D) -> void:
	
	if area.get_parent().is_in_group("player"):
		$AnimatedSprite2D.play("collected")
		
		Global.score += 1
		
		$CollisionShape2D.queue_free()
		
		
		await get_tree().create_timer(1).timeout
		
		queue_free()
	
	pass # Replace with function body.
