extends Node2D  # ← muda o nó raiz para Node2D no .tscn também

@onready var sprite = $Sprite2D
@onready var player = get_tree().get_first_node_in_group("player")
@onready var bullet_marker = $"Sprite2D/Marker2D-bullet_marker"

@export var kunai_scene : PackedScene

enum State {GROUND, HAND}
var actual_state = State.GROUND

@export_category("Gun Status")
@export var kunai_speed = 250.0
@export var damage = 20.0
@export var kunai_size = 1.0

func _process(delta: float) -> void:
	if player.is_alive and actual_state == State.HAND:
		aim()
		shoot()

func aim():
	look_at(get_global_mouse_position())
	if get_global_mouse_position().x < global_position.x:
		sprite.scale.y = -1
	else:
		sprite.scale.y = 1

func shoot():
	if Input.is_action_just_pressed("shoot") and kunai_scene:
		var kunai = kunai_scene.instantiate()
		get_tree().current_scene.add_child(kunai)
		kunai.global_position = bullet_marker.global_position
		kunai.global_rotation = global_rotation
		kunai.speed = kunai_speed
		kunai.damage = damage
		kunai.scale = Vector2.ONE * kunai_size
		queue_free()

func grab():
	var hand = player.get_node("Hand")
	actual_state = State.HAND
	$Area2D.queue_free()
	if hand.get_child_count() >= 1:   # ← corrigido: >= 1
		hand.get_child(0).queue_free()
	call_deferred("reparent", hand, true)
	global_position = hand.global_position

func _on_area_2d_body_entered(body: Node2D) -> void:  # ← body_entered, não area_entered
	if body.is_in_group("player"):
		grab()
