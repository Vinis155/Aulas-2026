# =========================================================
# PERSONAGEM TOPDOWN
# =========================================================
extends CharacterBody2D


# =========================================================
# VARIÁVEIS EXPORTADAS
# =========================================================

# Define qual jogador controla esse personagem
@export var player_id := 1

# Permite trocar as animações/sprites pelo Inspector
@export var skin_frames : SpriteFrames


# =========================================================
# CONFIGURAÇÕES DO PERSONAGEM
# =========================================================

# Velocidade de movimento
var speed = 50

# Guarda direção atual
var dir = Vector2.ZERO

# Guarda última direção usada
var last_direction = "down"

# Vida do jogador
var health = 3.0

# Dano recebido por hit
var damage_taken = 0.5

# Verifica se personagem está vivo
var is_alive = true

# Evita tomar dano várias vezes seguidas
var can_take_damage = true


# =========================================================
# NODES
# =========================================================

# AnimatedSprite2D
@onready var anim: AnimatedSprite2D = $AnimatedSprite2D

# AnimationPlayer
@onready var animation_player = $AnimationPlayer

# Hand (contém a lanterna)
@onready var hand = $Hand


# =========================================================
# READY
# =========================================================
func _ready():

	# Se existir skin configurada
	# aplica no personagem
	if skin_frames != null:

		anim.sprite_frames = skin_frames

	# Esconde o Sprite2D da lanterna (causa o quadrado visual)
	var lantern_sprite = get_node_or_null("Hand/PointLight2D/Sprite2D")
	if lantern_sprite:
		lantern_sprite.visible = false

	# Luz ambiente fraca ao redor do player
	_add_ambient_light()


# =========================================================
# LUZ AMBIENTE DO PLAYER
# =========================================================
func _add_ambient_light():

	var tex = load("res://sprites/Flashlight_small_range_sprite_sheet/Lanterna ligada.png")
	if tex == null:
		return

	var ambient = PointLight2D.new()
	ambient.texture = tex
	ambient.energy = 0.3
	ambient.color = Color(1.0, 0.9, 0.75)
	ambient.texture_scale = 0.15
	add_child(ambient)


# =========================================================
# PHYSICS PROCESS
# =========================================================
func _physics_process(_delta):


	# =========================================
	# SE ESTIVER MORTO
	# =========================================
	if not is_alive:

		move_and_slide()
		return


	# =========================================
	# MOVIMENTAÇÃO
	# =========================================
	move()


	# =========================================
	# ANIMAÇÕES
	# =========================================
	animations()


	# =========================================
	# LANTERNA - acompanha o mouse
	# =========================================
	rotate_lantern()


# =========================================================
# MOVIMENTAÇÃO
# =========================================================
func move():

	# Vetor de direção
	var input_dir = Vector2.ZERO


	# =====================================================
	# CONTROLES PLAYER 1
	# =====================================================
	if player_id == 1:

		input_dir = Input.get_vector(
			"p1_left",
			"p1_right",
			"p1_up",
			"p1_down"
		)


	# =====================================================
	# CONTROLES PLAYER 2
	# =====================================================
	elif player_id == 2:

		input_dir = Input.get_vector(
			"p2_left",
			"p2_right",
			"p2_up",
			"p2_down"
		)


	# Salva direção
	dir = input_dir


	# Normaliza diagonal
	input_dir = input_dir.normalized()


	# Aplica velocidade
	velocity = input_dir * speed


	# Move personagem
	move_and_slide()


# =========================================================
# LANTERNA - aponta para o mouse
# =========================================================
func rotate_lantern():

	var mouse_pos = get_global_mouse_position()
	var angle = (mouse_pos - global_position).angle()
	hand.rotation = angle


# =========================================================
# ANIMAÇÕES
# =========================================================
func animations():

	# =========================================
	# PERSONAGEM SE MOVENDO
	# =========================================
	if velocity != Vector2.ZERO:


		# =====================================
		# PRIORIDADE VERTICAL
		# =====================================
		if abs(dir.y) > abs(dir.x):


			# =================================
			# BAIXO
			# =================================
			if dir.y > 0:

				anim.play("down")

				last_direction = "down"


			# =================================
			# CIMA
			# =================================
			else:

				anim.play("up")

				last_direction = "up"


		# =====================================
		# LADO
		# =====================================
		else:

			anim.play("side")

			last_direction = "side"


			# =================================
			# FLIP HORIZONTAL
			# =================================

			if dir.x > 0:

				anim.flip_h = false

			elif dir.x < 0:

				anim.flip_h = true


	# =========================================
	# PERSONAGEM PARADO
	# =========================================
	else:


		# =====================================
		# IDLE DOWN
		# =====================================
		if last_direction == "down":

			anim.play("idle_down")


		# =====================================
		# IDLE UP
		# =====================================
		elif last_direction == "up":

			anim.play("up")

			anim.stop()

			anim.frame = 0


		# =====================================
		# IDLE SIDE
		# =====================================
		elif last_direction == "side":

			anim.play("idle_side")


# =========================================================
# RECEBER DANO
# =========================================================
func take_damage():

	# Evita múltiplos hits instantâneos
	if not can_take_damage:

		return


	can_take_damage = false


	# Remove vida
	health -= damage_taken


	# Toca animação de hit
	animation_player.play("hit")


	print(
		"Player ",
		player_id,
		" Vida atual: ",
		health
	)


	# Morre se acabar vida
	if health <= 0:

		die()

		return


	# Tempo de invencibilidade
	await get_tree().create_timer(0.5).timeout

	can_take_damage = true


# =========================================================
# MORTE
# =========================================================
func die():

	# Evita morrer duas vezes
	if not is_alive:
		return


	# Marca morto
	is_alive = false


	# Para movimento
	velocity = Vector2.ZERO


	# Desativa colisão
	$CollisionShape2D.set_deferred(
		"disabled",
		true
	)


	# Toca animação hit
	animation_player.play("hit")


	# Espera animação terminar
	await animation_player.animation_finished


	# Esconde player
	visible = false


	# Verifica game over
	check_game_over()


# =========================================================
# GAME OVER
# =========================================================
func check_game_over():

	# Espera pequeno delay
	await get_tree().create_timer(0.2).timeout


	# Pega jogadores
	var players = get_tree().get_nodes_in_group("player")


	# Verifica vivos
	var alive_count = 0


	for p in players:

		if is_instance_valid(p):

			if p.is_alive:

				alive_count += 1


	# Se ninguém estiver vivo
	if alive_count <= 0:

		await get_tree().create_timer(1.0).timeout

		get_tree().reload_current_scene()
