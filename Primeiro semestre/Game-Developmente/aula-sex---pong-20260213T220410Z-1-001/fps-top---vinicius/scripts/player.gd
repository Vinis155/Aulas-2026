# Faz esse script controlar um personagem com física 2D
extends CharacterBody2D

# Pega automaticamente o nó AnimatedSprite2D da cena
# para controlar as animações do personagem
@onready var sprite = $AnimatedSprite2D

# Velocidade de movimentação do personagem
var speed = 60

# Armazena a direção atual do movimento (parado inicialmente)
var direction = Vector2.ZERO

# Controla se o personagem está vivo
var is_alive = true


# Função executada automaticamente a cada frame de física
func _physics_process(delta: float) -> void:

	# Só permite mover e animar se estiver vivo
	if is_alive:
		move()
		anim()


# Responsável pela movimentação do personagem
func move():

	# Captura entrada do jogador
	# left = esquerda
	# right = direita
	# up = cima
	# down = baixo
	direction = Input.get_vector("left", "right", "up", "down")

	# Se alguma direção foi pressionada
	if direction != Vector2.ZERO:

		# Define velocidade baseada na direção
		velocity = direction * speed

	else:
		# Faz o personagem desacelerar suavemente até parar
		velocity = velocity.move_toward(Vector2.ZERO, speed)

	# Move o personagem considerando colisões
	move_and_slide()

	# Impede sair dos limites horizontais do mapa
	# Mantém X entre 8 e 320
	global_position.x = clamp(global_position.x, 8, 320)

	# Impede sair dos limites verticais do mapa
	# Mantém Y entre 0 e 160
	global_position.y = clamp(global_position.y, 0, 160)


# Controla qual animação será exibida
func anim():

	# Se estiver parado
	if direction == Vector2.ZERO:

		# Executa animação parado
		sprite.play("idle")

	else:

		# Verifica se movimento horizontal é maior que vertical
		if abs(direction.x) > abs(direction.y):

			# Toca animação lateral
			sprite.play("walk_side")

			# Se estiver indo para esquerda
			if direction.x < 0:

				# Espelha o sprite
				sprite.flip_h = true

			else:

				# Mantém olhando para direita
				sprite.flip_h = false

		# Se estiver descendo
		elif direction.y > 0:

			# Toca animação andando para baixo
			sprite.play("walk_down")

		else:

			# Caso contrário está subindo
			sprite.play("walk_up")


# Função chamada quando o personagem morre
func die():

	# Evita executar morte mais de uma vez
	if is_alive:

		# Marca personagem como morto
		is_alive = false

		# Executa animação de morte
		sprite.play("death")

		# Espera 3 segundos
		await get_tree().create_timer(3.0).timeout

		# Reinicia a cena atual
		get_tree().reload_current_scene()
