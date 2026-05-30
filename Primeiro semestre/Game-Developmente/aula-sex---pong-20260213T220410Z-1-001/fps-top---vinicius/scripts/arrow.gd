extends Area2D

var speed = 200
var damage = 20


func _ready():

	await get_tree().create_timer(
		2.0
	).timeout

	queue_free()


func _physics_process(delta):

	position += (
		transform.x
		* speed
		* delta
	)
