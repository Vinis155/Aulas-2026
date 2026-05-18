extends Area2D

@onready var sprite = $AnimatedSprite2D

var speed = 30
var velocity = Vector2.ZERO

var life = 100
var is_alive = true

func _physics_process(delta: float) -> void:
	if is_alive:
		move(delta)
		
	pass

func move(delta):
	
	var player = get_tree().get_first_node_in_group("player")
	
	if not player:
		return
	
	var direction = global_position.direction_to(player.global_position)

	var push = Vector2.ZERO
	for enemy in get_tree().get_nodes_in_group("enemies"):
		if enemy != self:
			if global_position.distance_to(enemy.global_position) <40:
				push += enemy.global_position.direction_to(global_position)
	
	var final_direction = (direction + push).normalized()			
	
	velocity = velocity.lerp(final_direction * speed, 0.1)
	
	global_position += velocity * delta

	if global_position.x < player.global_position.x:
		sprite.flip_h = false
	else:
		sprite.flip_h = true


func _on_area_entered(area: Area2D) -> void:
	
	if area.is_in_group("bullets"):
		$AnimationPlayer.play("hit")
		life -= area.damage
		area.queue_free()
		
	if life <= 0:
		die()
		
	if area.get_parent().is_in_group("player"):
		die()
		area.get_parent().die()	
	
	pass # Replace with function body.
func die():
	
	is_alive = false
	sprite.play("death")
	$CollisionShape2D.queue_free()
	await get_tree().create_timer(1.0).timeout
	queue_free()
	
	
	pass
