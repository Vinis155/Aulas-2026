extends Node2D

# Referência ao sprite visual da arma
@onready var sprite = $Sprite2D

# Referência ao jogador
@onready var player = get_tree().get_first_node_in_group("player")

# Ponto de spawn do kunai (ponta da arma)
@onready var bullet_marker = $"Sprite2D/Marker2D-bullet_marker"

# Cena do kunai a ser instanciada
@export var kunai_scene : PackedScene

# Estado: no chão ou equipada
enum State {GROUND, HAND}
var actual_state = State.GROUND

@export_category("Gun Status")
@export var kunai_speed = 250.0
@export var damage = 20.0
@export var kunai_size = 1.0

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
# SHOOT — arma de uso único: atira e se destrói
# =========================================================
func shoot():
	# just_pressed = disparo único por clique (não automático)
	if Input.is_action_just_pressed("shoot") and kunai_scene:
		var kunai = kunai_scene.instantiate()
		get_tree().current_scene.add_child(kunai)

		kunai.global_position = bullet_marker.global_position
		kunai.global_rotation = global_rotation
		kunai.speed = kunai_speed
		kunai.damage = damage
		kunai.scale = Vector2.ONE * kunai_size

		# Após atirar, a arma some — kunai é descartável
		queue_free()

# =========================================================
# GRAB — equipa na mão do jogador
# =========================================================
func grab():
	var hand = player.get_node("Hand")
	actual_state = State.HAND
	$Area2D.queue_free()  # Remove colisão de coleta

	# Se já houver uma arma equipada, descarta antes de equipar esta
	if hand.get_child_count() >= 1:
		hand.get_child(0).queue_free()

	# Reparenta para a mão (deferred evita crash durante física)
	call_deferred("reparent", hand, true)
	global_position = hand.global_position

# =========================================================
# COLISÃO — usa body_entered (detecta CharacterBody2D do jogador)
# em vez de area_entered, pois o jogador não é uma Area2D
# =========================================================
func _on_area_2d_body_entered(body: Node2D) -> void:
	if body.is_in_group("player"):
		grab()
