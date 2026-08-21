extends Node2D

# Referência ao sprite visual da arma
@onready var sprite = $Sprite2D

# Referência ao jogador (buscado no início da cena)
@onready var player = get_tree().get_first_node_in_group("player")

# Ponto de origem dos projéteis (ponta do cano)
@onready var bullet_marker = $"Sprite2D/Marker2D-bullet_marker"

# Cena do projétil a ser instanciada
@export var bullet_scene : PackedScene

# Estado da arma: no chão (coletável) ou equipada na mão
enum State {GROUND, HAND}
var actual_state = State.GROUND

@export_category("Gun Status")
@export var fire_time = 0.5     # Intervalo entre disparos (cadência)
@export var bullet_speed = 200.0
@export var damage = 10.0
@export var bullet_size = 1.0

var can_shoot = true  # Bloqueado durante a recarga

# =========================================================
# PROCESS
# =========================================================
func _process(delta: float) -> void:
	# Só mira e atira se o jogador estiver vivo e a arma equipada
	if player.is_alive and actual_state == State.HAND:
		aim()
		shoot()

# =========================================================
# AIM
# =========================================================
func aim():
	# Rotaciona a arma em direção ao cursor do mouse
	look_at(get_global_mouse_position())

	# Espelha o sprite verticalmente quando o mouse está à esquerda
	# (evita que a arma apareça de cabeça para baixo)
	if get_global_mouse_position().x < global_position.x:
		sprite.scale.y = -1
	else:
		sprite.scale.y = 1

# =========================================================
# SHOOT
# =========================================================
func shoot():
	# Dispara enquanto o botão é mantido pressionado (is_action_pressed)
	# Diferente do anterior que usava just_pressed — esta arma é automática
	if Input.is_action_pressed("shoot") and bullet_scene and can_shoot:

		can_shoot = false           # Bloqueia disparo até o timer acabar
		$Timer.start(fire_time)     # Inicia recarga

		var bullet = bullet_scene.instantiate()
		get_tree().current_scene.add_child(bullet)  # Adiciona à cena raiz

		bullet.global_position = bullet_marker.global_position  # Spawn no cano
		bullet.global_rotation = global_rotation                 # Direção do disparo

		bullet.speed = bullet_speed
		bullet.damage = damage
		# Escala não-uniforme: projétil mais largo que alto (ex: bala achatada)
		bullet.scale = Vector2(2, 1) * bullet_size

# =========================================================
# GRAB — equipa a arma na mão do jogador
# =========================================================
func grab():
	var hand = player.get_node("Hand")
	actual_state = State.HAND
	$Area2D.queue_free()  # Remove colisão de coleta

	if player.get_node("Hand").get_child_count() == 0:
		# Mão vazia: apenas reparenta
		call_deferred("reparent", hand, true)
		global_position = hand.global_position

	elif hand.get_child_count() >= 0:
		# ⚠️ Bug potencial: essa condição é sempre verdadeira (>= 0)
		# A intenção provavelmente era (> 0) para substituir arma existente
		hand.get_child(0).queue_free()
		call_deferred("reparent", hand, true)
		global_position = hand.global_position

# =========================================================
# COLISÃO — jogador entra na área de coleta
# =========================================================
func _on_area_2d_area_entered(area: Area2D) -> void:
	if area.get_parent().is_in_group("player"):
		grab()

# =========================================================
# TIMER — libera o disparo após a recarga
# =========================================================
func _on_timer_timeout() -> void:
	can_shoot = true
