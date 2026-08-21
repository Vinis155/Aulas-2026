extends Node2D

# Referência ao Sprite2D filho (visual da arma)
@onready var sprite = $Sprite2D

# Referência ao primeiro nó no grupo "player" na cena
@onready var player = get_tree().get_first_node_in_group("player")

# Marker2D usado como ponto de origem dos projéteis (cano da arma)
@onready var bullet_marker = $"Sprite2D/Marker2D-bullet_marker"

# Cena do projétil a ser instanciada ao atirar
@export var bullet_scene : PackedScene

# Estados possíveis da arma: no chão (coletável) ou na mão do jogador
enum State {GROUND, HAND}
var actual_state = State.GROUND

# =========================================================
# GUN STATUS
# =========================================================
@export_category("Gun Status")

# Tempo de recarga entre disparos (em segundos)
@export var fire_time = 1.5

# Velocidade do projétil
@export var bullet_speed = 400.0

# Dano causado por projétil
@export var damage = 25.0

# Escala visual do projétil
@export var bullet_size = 1.0

# Controla se a arma pode atirar agora (false durante recarga)
var can_shoot = true

# =========================================================
# PROCESS — executado a cada frame
# =========================================================
func _process(_delta):
	# Se o jogador não existe, não faz nada
	if player == null:
		return
	# Só mira e atira se o jogador estiver vivo e a arma estiver na mão
	if player.is_alive and actual_state == State.HAND:
		aim()
		shoot()

# =========================================================
# AIM — faz a arma apontar para o mouse
# =========================================================
func aim():
	# Rotaciona o Node2D inteiro em direção ao cursor
	look_at(get_global_mouse_position())

	# Espelha o sprite verticalmente quando o mouse está à esquerda
	# (evita que o sprite fique de cabeça para baixo)
	if get_global_mouse_position().x < global_position.x:
		sprite.scale.y = -1
	else:
		sprite.scale.y = 1

# =========================================================
# SHOOT — lógica de disparo
# =========================================================
func shoot():
	if (
		Input.is_action_just_pressed("shoot") # Botão de tiro pressionado
		and bullet_scene                       # Cena do projétil foi atribuída
		and can_shoot                          # Arma não está em recarga
	):
		can_shoot = false          # Bloqueia novos disparos
		$Timer.start(fire_time)    # Inicia o timer de recarga

		# Instancia o projétil a partir da cena exportada
		var bullet = bullet_scene.instantiate()

		# Adiciona o projétil como filho da cena atual (não da arma)
		get_tree().current_scene.add_child(bullet)

		# Posiciona o projétil no ponto do cano da arma
		bullet.global_position = bullet_marker.global_position

		# Herda a rotação atual da arma (direção do disparo)
		bullet.global_rotation = global_rotation

		# Passa os atributos configurados para o projétil
		bullet.speed = bullet_speed
		bullet.damage = damage
		bullet.scale = Vector2.ONE * bullet_size  # Aplica tamanho uniforme

# =========================================================
# GRAB — equipa a arma na mão do jogador
# =========================================================
func grab():
	# Obtém o nó "Hand" dentro do jogador (ponto de ancoragem da arma)
	var hand = player.get_node("Hand")

	# Muda o estado para "na mão"
	actual_state = State.HAND

	# Remove a Area2D de coleta (arma não pode mais ser coletada)
	$Area2D.queue_free()

	if hand.get_child_count() == 0:
		# Mão vazia: reparenta a arma para a mão sem resetar a transform global
		call_deferred("reparent", hand, true)
		global_position = hand.global_position
	else:
		# Já havia uma arma na mão: descarta a anterior e equipa esta
		hand.get_child(0).queue_free()
		call_deferred("reparent", hand, true)
		global_position = hand.global_position

# =========================================================
# COLISÃO — detecta quando o jogador entra na área de coleta
# =========================================================
func _on_area_2d_area_entered(area):
	# Verifica se a área pertence a um nó do grupo "player"
	if area.get_parent().is_in_group("player"):
		grab()  # Equipa a arma

# =========================================================
# TIMER — chamado quando o tempo de recarga termina
# =========================================================
func _on_timer_timeout():
	can_shoot = true  # Libera o disparo novamente
