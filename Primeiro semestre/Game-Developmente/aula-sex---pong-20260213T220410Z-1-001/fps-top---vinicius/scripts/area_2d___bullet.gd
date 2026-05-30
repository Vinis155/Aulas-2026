extends Area2D
 
var speed = 200
var damage = 10
 
func _ready():
	await get_tree().create_timer(2.0).timeout
	queue_free()
 
func _physics_process(delta: float) -> void:
	position += transform.x * speed * delta
 
func _on_area_entered(area: Area2D) -> void:
	if area.is_in_group("player"):
		return
	queue_free()
 
func _on_body_entered(body: Node2D) -> void:
	if body.is_in_group("enemy"):
		body.take_damage(damage)
		queue_free()
