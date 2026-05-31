# =========================================================
# PERSONAGEM TOPDOWN
# =========================================================
extends CharacterBody2D


# =========================================================
# VARIÁVEIS EXPORTADAS
# =========================================================

# Define qual jogador controla o personagem
@export var player_id := 1

# Permite trocar sprites/animações pelo Inspector
@export var skin_frames : SpriteFrames


# =========================================================
# CONFIGURAÇÕES DO PERSONAGEM
# =========================================================

# Velocidade do personagem
var speed = 20

# Guarda direção atual
var dir = Vector2.ZERO

# Guarda última direção usada
# Serve para o idle correto
var last_direction = "down"

# Verifica se personagem está vivo
var is_alive = true


# =========================================================
# NODES
# =========================================================

# Referência automática do AnimatedSprite2D
@onready var anim: AnimatedSprite2D = $AnimatedSprite2D


# =========================================================
# READY
# =========================================================
func _ready():

	# Se existir skin configurada
	# aplica automaticamente
	if skin_frames != null:
		anim.sprite_frames = skin_frames


# =========================================================
# PHYSICS PROCESS
# =========================================================
func _physics_process(_delta):

	# Faz movimentação
	move()

	# Atualiza animações
	if is_alive:
		animations()


# =========================================================
# MOVIMENTAÇÃO
# =========================================================
func move():

	# =========================================
	# SE ESTIVER MORTO
	# =========================================
	if not is_alive:

		# Para movimento
		velocity = Vector2.ZERO

		move_and_slide()
		return


	# Vetor de direção
	var input_dir = Vector2.ZERO


	# =========================================
	# PLAYER 1
	# =========================================
	if player_id == 1:

		input_dir = Input.get_vector(
			"p1_left",
			"p1_right",
			"p1_up",
			"p1_down"
		)


	# =========================================
	# PLAYER 2
	# =========================================
	elif player_id == 2:

		input_dir = Input.get_vector(
			"p2_left",
			"p2_right",
			"p2_up",
			"p2_down"
		)


	# Guarda direção atual
	dir = input_dir


	# Normaliza diagonal
	# Evita diagonal mais rápida
	input_dir = input_dir.normalized()


	# Aplica velocidade
	velocity = input_dir * speed


	# Move personagem
	move_and_slide()


# =========================================================
# ANIMAÇÕES
# =========================================================
func animations():

	# =========================================
	# PERSONAGEM ANDANDO
	# =========================================
	if velocity != Vector2.ZERO:

		# PRIORIDADE VERTICAL
		if abs(dir.y) > abs(dir.x):

			# BAIXO
			if dir.y > 0:

				anim.play("down")
				last_direction = "down"

			# CIMA
			else:

				anim.play("up")
				last_direction = "up"


		# =====================================
		# LADO
		# =====================================
		else:

			anim.play("side")
			last_direction = "side"

			# DIREITA
			if dir.x > 0:
				anim.flip_h = false

			# ESQUERDA
			elif dir.x < 0:
				anim.flip_h = true


	# =========================================
	# PERSONAGEM PARADO
	# =========================================
	else:

		# DOWN
		if last_direction == "down":

			anim.play("down")
			anim.stop()
			anim.frame = 0


		# UP
		elif last_direction == "up":

			anim.play("up")
			anim.stop()
			anim.frame = 0


		# SIDE
		elif last_direction == "side":

			anim.play("idle_side")
			anim.stop()
			anim.frame = 0

# =========================================================
# MORTE
# =========================================================
func die():

	# Evita morrer duas vezes
	if not is_alive:
		return


	# Marca como morto
	is_alive = false


	# Toca animação de hit
	anim.play("hit")


	# Desativa colisão
	$CollisionShape2D.set_deferred("disabled", true)


	# Verifica game over
	check_game_over()


# =========================================================
# GAME OVER
# =========================================================
func check_game_over():

	# Espera meio segundo
	await get_tree().create_timer(0.5).timeout


	# Pega todos jogadores
	var players = get_tree().get_nodes_in_group("player")


	# Verifica se existe alguém vivo
	var alguem_vivo = false


	# Percorre jogadores
	for p in players:

		if is_instance_valid(p) and p is CharacterBody2D and "is_alive" in p:

			if p.is_alive:
				alguem_vivo = true
				break


	# Se todos morreram
	if not alguem_vivo:

		# Espera 1 segundo
		await get_tree().create_timer(1.0).timeout

		# Reinicia cena
		get_tree().reload_current_scene()
