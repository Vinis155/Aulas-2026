extends Node2D

@onready var sprite = $Sprite2D
@onready var player = get_tree().get_first_node_in_group("player")
@onready var bullet_marker = $"Sprite2D/Marker2D-bullet_marker"
@export var bullet_scene : PackedScene

enum State {GROUND, HAND}
var actual_state = State.GROUND

@export_category("Gun Status")
@export var fire_time = 0.5      # Intervalo entre disparos
@export var bullet_speed = 200.0
@export var damage = 10.0
@export var bullet_size = 1.0
@export var pellets = 3          # Quantidade de projéteis por disparo (chumbo)
@export var spread_angle = 20.0  # Ângulo total do cone de dispersão (em graus)

var can_shoot = true

# =========================================================
# PROCESS
# =========================================================
func _process(delta: float) -> void:
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
# SHOOT — dispara múltiplos projéteis em leque (shotgun)
# =========================================================
func shoot():
	if Input.is_action_pressed("shoot") and bullet_scene and can_shoot:
		can_shoot = false
		$Timer.start(fire_time)

		# Cria cada projétil do leque
		for i in pellets:
			var bullet = bullet_scene.instantiate()
			get_tree().current_scene.add_child(bullet)
			bullet.global_position = bullet_marker.global_position

			# Calcula o desvio angular de cada projétil
			# Distribui os pellets simetricamente ao redor do centro:
			# Ex: 3 pellets com spread 20° → offsets: -10°, 0°, +10°
			var angle_offset = deg_to_rad(
				spread_angle * (i - (pellets - 1) / 2.0)
			)
			bullet.global_rotation = global_rotation + angle_offset

			bullet.speed = bullet_speed
			bullet.damage = damage
			bullet.scale = Vector2.ONE * bullet_size

# =========================================================
# GRAB
# =========================================================
func grab():
	var hand = player.get_node("Hand")
	actual_state = State.HAND
	$Area2D.queue_free()

	if player.get_node("Hand").get_child_count() == 0:
		call_deferred("reparent", hand, true)
		global_position = hand.global_position
	elif hand.get_child_count() >= 0:
		# ⚠️ Bug: >= 0 é sempre verdadeiro — deveria ser >= 1
		hand.get_child(0).queue_free()
		call_deferred("reparent", hand, true)
		global_position = hand.global_position

# =========================================================
# COLISÃO — jogador coleta a arma
# =========================================================
func _on_area_2d_area_entered(area: Area2D) -> void:
	if area.get_parent().is_in_group("player"):
		grab()

# =========================================================
# TIMER — libera o próximo disparo
# =========================================================
func _on_timer_timeout() -> void:
	can_shoot = true
