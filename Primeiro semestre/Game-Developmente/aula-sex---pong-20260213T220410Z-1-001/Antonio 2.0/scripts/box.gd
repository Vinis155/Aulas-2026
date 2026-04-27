extends StaticBody2D

var life = 3


func _on_area_2d_area_entered(area: Area2D) -> void:
	
	if area.get_parent().is_in_group("player"):
		$AnimatedSprite2D.play("hit")
		life -= 1
		
		area.get_parent().velocity.y = -400
		
		if life <= 0:
			queue_free()
			
			$CPUParticles2D.restart()
			$AnimatedSprite2D.queue_free()
			$CollisionShape2D.queue_free()
			$Area2D.queue_free()
			await get_tree().create_timer(1).timeout
			
			queue_free()
