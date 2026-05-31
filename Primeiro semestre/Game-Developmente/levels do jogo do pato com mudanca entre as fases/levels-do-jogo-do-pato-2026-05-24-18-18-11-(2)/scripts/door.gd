extends Area2D

@export var next_level : PackedScene

@onready var sprite = $AnimatedSprite2D

var entered = false

func _on_body_entered(body):
	if entered:
		return

	if body.is_in_group("player"):
		entered = true

		body.visible = false

		sprite.play("door_opening")

		await sprite.animation_finished

		get_tree().change_scene_to_packed(next_level)
