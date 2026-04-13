extends CharacterBody2D  # Corpo ideal para player (movimento + colisão pronta)

var speed = 160.0  # Velocidade horizontal do personagem
var dir  # Direção (-1 esquerda, 1 direita, 0 parado)

var jump_velocity = -300.0  # Força do pulo (negativo sobe)

var gravity = 980  # Gravidade aplicada ao personagem

var extra_jumps = 1  # Quantidade de pulos extras (pulo duplo)

var is_alive = true  # Controla se o player está vivo

var coins = 0

@onready var anim: AnimatedSprite2D = $AnimatedSprite2D  
# Referência ao nó de animação
@onready var death_line = $"../DeathLine"
func _ready() -> void:
	pass  # Executa quando o jogo inicia (não usado aqui)
		
		
func _physics_process(delta: float) -> void:
	move(delta)  # Chama função de movimento
	
	if is_alive:
		animations()  # Só anima se estiver vivo
	
	pass
	
func move(delta):
	
	if is_alive:
		dir = Input.get_axis("left", "right")  
		# Retorna -1, 0 ou 1 dependendo da tecla pressionada
	
	# Movimento horizontal
	if dir:
		velocity.x = dir * speed  # Move para esquerda ou direita
	elif dir == 0:
		velocity.x = 0  # Para o personagem
		
	# Gravidade
	if not is_on_floor():
		velocity.y += gravity * delta  # Faz o personagem cair
		
	# Pulo (com pulo duplo)
	if Input.is_action_just_pressed("jump") and extra_jumps > 0 and is_alive:
		velocity.y = jump_velocity  # Aplica força do pulo
		extra_jumps -= 1  # Consome um pulo
		
	# Reset do pulo ao tocar o chão
	if is_on_floor():
		extra_jumps = 1
		
	move_and_slide()  # Aplica o movimento com colisão
	
	if global_position.y >= death_line.global_position.y and is_alive:
		die()
	
	pass
	
func animations():
	# Correndo
	if velocity.x != 0 and is_on_floor():
		anim.play("run")
		
	# Parado
	elif velocity.x == 0 and is_on_floor():
		anim.play("idle")
		
	# Pulando
	if not is_on_floor() and extra_jumps >= 1:
		anim.play("jump")
		
	# Inverte sprite conforme direção
	if dir > 0:
		anim.flip_h = false  # Direita
	elif dir < 0:
		anim.flip_h = true   # Esquerda

	pass


func die ():
	
	if is_alive:
		
		is_alive = false  # Marca como morto
		
		anim.play("hit")  # Animação de dano/morte
		
		$Area2D.queue_free()  # Remove área de colisão (não toma mais dano)
		$CollisionShape2D.queue_free()  # Remove colisão física
		
		velocity.y = jump_velocity -300  # Faz o player "voar" pra cima ao morrer
		
		await get_tree().create_timer(1).timeout  # Espera 1 segundo
		
		get_tree().reload_current_scene()  # Reinicia a fase
	
	pass
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
# 🎮 PLAYER (Personagem)
# Tipo do nó: CharacterBody2D
# Estrutura:
# Player (CharacterBody2D)
# ├── CollisionShape2D   -> colisão do player
# ├── AnimatedSprite2D   -> animações (idle, run, jump, hit)
# ├── Area2D             -> detectar dano/inimigos
# └── Camera2D           -> câmera seguindo o player
#
# Configurações:
# - Adicionar o Player ao grupo "Player"
# - Criar animações no AnimatedSprite2D
# - Mapear inputs: left, right, jump


# =============================

# 🧱 CHÃO / PLATAFORMA
# Tipo do nó: StaticBody2D
# Estrutura:
# StaticBody2D
# └── CollisionShape2D
#
# Função:
# - Serve como chão (player pode pisar)
# - Não se move

# =============================

# ⚙️ SERRA (ARMADILHA)
# Tipo do nó: Area2D
# Estrutura:
# Saw (Area2D)
# ├── CollisionShape2D   -> área de dano
# └── AnimatedSprite2D   -> animação girando
#
# Configurações:
# - Conectar sinal: area_entered
# - Criar script para:
#     - Movimento automático
#     - Inverter direção
#     - Detectar player e dar dano

# =============================

# 🎯 LÓGICA IMPORTANTE (PROVA)

# ✔ Movimento:
# position += direção * velocidade * delta

# ✔ Gravidade:
# velocity.y += gravity * delta

# ✔ Pulo:
# velocity.y = -força

# ✔ Detectar chão:
# is_on_floor()

# ✔ Dano:
# area_entered → chamar função die()

# ✔ Inverter direção:
# dir = -dir

# ✔ Reset fase:
# get_tree().reload_current_scene()

# =============================

# 🧠 DICA FINAL (SE TRAVAR NA PROVA)
# SEMPRE LEMBRE:
# - Player → CharacterBody2D
# - Chão → StaticBody2D
# - Armadilha → Area2D
#
# Isso sozinho já resolve metade da questão.
# =========================================
