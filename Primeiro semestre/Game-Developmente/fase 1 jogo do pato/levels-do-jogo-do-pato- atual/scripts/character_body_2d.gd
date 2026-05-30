# =========================================================
# SPIDER IA
# =========================================================
extends CharacterBody2D


# =========================================================
# CONFIGURAÇÕES
# =========================================================

# Velocidade da aranha
@export var speed := 40.0

# Tempo mínimo para trocar direção
@export var min_time := 1.0

# Tempo máximo para trocar direção
@export var max_time := 3.0


# =========================================================
# VARIÁVEIS
# =========================================================

# Player perseguido
var target = null

# Direção atual
var direction = Vector2.ZERO

# Timer da patrulha
var timer = 0.0


# =========================================================
# NODES
# =========================================================

@onready var anim = $AnimatedSprite2D


# =========================================================
# READY
# =========================================================
func _ready():

	randomize()

	change_direction()


# =========================================================
# PROCESS
# =========================================================
func _physics_process(delta):


	# =========================================
	# PERSEGUIR PLAYER
	# =========================================
	if target != null:

		direction = (
			target.global_position - global_position
		).normalized()


	# =========================================
	# PATRULHA ALEATÓRIA
	# =========================================
	else:

		timer -= delta

		if timer <= 0:

			change_direction()


	# =========================================
	# MOVIMENTO
	# =========================================
	velocity = direction * speed

	move_and_slide()


	# =========================================
	# COLISÕES
	# =========================================
	if get_slide_collision_count() > 0:

		for i in range(get_slide_collision_count()):

			var collision = get_slide_collision(i)

			var body = collision.get_collider()


			# =====================================
			# PLAYER
			# =====================================
			if body.is_in_group("player"):

				# Mata o player
				body.take_damage()


			# =====================================
			# PAREDE
			# =====================================
			else:

				var normal = collision.get_normal()

				direction = (
					direction + normal * 2.0
				).normalized()


	# =========================================
	# ANIMAÇÕES
	# =========================================
	animations()


# =========================================================
# TROCAR DIREÇÃO
# =========================================================
func change_direction():

	timer = randf_range(
		min_time,
		max_time
	)

	direction = [
		Vector2.LEFT,
		Vector2.RIGHT,
		Vector2.UP,
		Vector2.DOWN
	].pick_random()


# =========================================================
# ANIMAÇÕES
# =========================================================
func animations():

	anim.play("walk")


	# =========================================
	# FLIP HORIZONTAL
	# =========================================

	# DIREITA
	if direction.x > 0:

		anim.flip_h = false


	# ESQUERDA
	elif direction.x < 0:

		anim.flip_h = true


# =========================================================
# PLAYER ENTROU NA VISÃO
# =========================================================
func _on_vision_area_body_entered(body):

	if body.is_in_group("player"):

		target = body


# =========================================================
# PLAYER SAIU DA VISÃO
# =========================================================
func _on_vision_area_body_exited(body):

	if body == target:

		target = null

		change_direction()
