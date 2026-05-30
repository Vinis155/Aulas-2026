extends Node2D

@onready var sprite = $Sprite2D
@onready var player = get_tree().get_first_node_in_group("player")
@onready var bullet_marker = $"Sprite2D/Marker2D-bullet_marker"

@export var bullet_scene : PackedScene

enum State {GROUND, HAND}

var actual_state = State.GROUND


# =========================================================
# GUN STATUS
# =========================================================
@export_category("Gun Status")

@export var fire_time = 1.5
@export var bullet_speed = 400.0
@export var damage = 25.0
@export var bullet_size = 1.0


var can_shoot = true


# =========================================================
# PROCESS
# =========================================================
func _process(_delta):

	if player == null:
		return

	if player.is_alive and actual_state == State.HAND:

		aim()

		shoot()


# =========================================================
# AIM
# =========================================================
func aim():

	look_at(get_global_mouse_position())


	if get_global_mouse_position().x < global_position.x:

		sprite.scale.y = -1

	else:

		sprite.scale.y = 1


# =========================================================
# SHOOT
# =========================================================
func shoot():

	if (
		Input.is_action_just_pressed("shoot")
		and bullet_scene
		and can_shoot
	):

		can_shoot = false

		$Timer.start(fire_time)


		# Cria bullet
		var bullet = bullet_scene.instantiate()

		get_tree().current_scene.add_child(
			bullet
		)


		# POSIÇÃO
		bullet.global_position = (
			bullet_marker.global_position
		)


		# ROTAÇÃO
		bullet.global_rotation = (
			global_rotation
		)


		# STATUS
		bullet.speed = bullet_speed

		bullet.damage = damage

		bullet.scale = (
			Vector2.ONE * bullet_size
		)


# =========================================================
# PEGAR ARMA
# =========================================================
func grab():

	var hand = player.get_node("Hand")

	actual_state = State.HAND

	$Area2D.queue_free()


	if hand.get_child_count() == 0:

		call_deferred(
			"reparent",
			hand,
			true
		)

		global_position = hand.global_position


	else:

		hand.get_child(0).queue_free()

		call_deferred(
			"reparent",
			hand,
			true
		)

		global_position = hand.global_position


# =========================================================
# PEGAR ARMA COLISÃO
# =========================================================
func _on_area_2d_area_entered(area):

	if area.get_parent().is_in_group(
		"player"
	):

		grab()


# =========================================================
# TIMER
# =========================================================
func _on_timer_timeout():

	can_shoot = true
