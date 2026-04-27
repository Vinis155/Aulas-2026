extends CharacterBody2D

var speed = 160.0
var dir

var jump_velocity = -300.0

var gravity = 980

var extra_jumps = 1

@onready var anim: AnimatedSprite2D = $AnimatedSprite2D
@onready var death_line = $"../deathline"

var is_alive = true

func _ready() -> void:
	pass

func _physics_process(delta: float) -> void:
	move(delta)
	
	if is_alive:
		animations()
	
	pass

func move(delta):
	if is_alive:
		dir = Input.get_axis("left", "right")
	if dir:
		velocity.x = dir * speed
	elif dir == 0:
		velocity.x = 0
		
	if not is_on_floor():
		velocity.y += gravity * delta
		
	if Input.is_action_just_pressed("jump") and extra_jumps > 0 and is_alive:
		velocity.y = jump_velocity
		extra_jumps -= 1
		
	if is_on_floor():
		extra_jumps = 1
	
	if global_position.y >= death_line.global_position.y and is_alive:
		die()
	
	move_and_slide()
	pass

func animations():
	if velocity.x != 0 and is_on_floor():
		anim.play("run")
	elif velocity.x == 0 and is_on_floor():
		anim.play("idle")
		
	if not is_on_floor() and extra_jumps >= 1:
		anim.play("jump")
		
	if dir > 0:
		anim.flip_h = false
	elif dir < 0:
		anim.flip_h = true

	pass

func die():
	if is_alive:
		is_alive = false
		anim.play("hit")
	
		$Area2D.queue_free()
		$CollisionShape2D.queue_free()
		velocity.y = jump_velocity - 100
		
		await get_tree().create_timer(1).timeout
		get_tree().reload_current_scene()
	
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
