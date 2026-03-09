extends RigidBody2D

var speed = 200
var dir = [-1, 1]
var score_p1 = 0
var score_p2 = 0
var game_over = false

# ==============================
# CONTROLE DE TOQUES
# ==============================
var last_player = ""
var hit_count = 0
var last_collider = null   # evita múltiplos contatos no mesmo frame

var speed_multiplier = 2.0
var max_speed = 1500


func _ready() -> void:
	reset()


func _physics_process(delta: float) -> void:
	score()
	_win()

# DETECTA COLISÕES
func _integrate_forces(state):

	for i in range(state.get_contact_count()):

		var collider = state.get_contact_collider_object(i)

		if collider == null:
			continue

		# evita múltiplas leituras do mesmo collider
		if collider == last_collider:
			continue

		last_collider = collider

		# PLAYER 1
		if collider.name == "Player":

			print("Colidiu com Player")

			if last_player == "Player":
				hit_count += 1
			else:
				hit_count = 1

			print("Contador:", hit_count)

			if hit_count == 2:

				print("DOBRANDO VELOCIDADE")

				linear_velocity *= speed_multiplier

				if linear_velocity.length() > max_speed:
					linear_velocity = linear_velocity.normalized() * max_speed

				print("Velocidade atual:", linear_velocity)

				hit_count = 0

			last_player = "Player"

		# PLAYER 2
		elif collider.name == "Player2":

			print("Colidiu com Player2")

			if last_player == "Player2":
				hit_count += 1
			else:
				hit_count = 1

			print("Contador:", hit_count)

			if hit_count == 2:

				print("DOBRANDO VELOCIDADE")

				linear_velocity *= speed_multiplier

				if linear_velocity.length() > max_speed:
					linear_velocity = linear_velocity.normalized() * max_speed

				print("Velocidade atual:", linear_velocity)

				hit_count = 0

			last_player = "Player2"


		else:
			print("Parede - ignorado")


func reset():

	global_position = get_viewport_rect().size / 2
	last_player = ""
	hit_count = 0
	last_collider = null

	freeze = true
	await get_tree().create_timer(1).timeout
	freeze = false

	apply_central_impulse(Vector2(dir.pick_random() * speed, dir.pick_random() * speed))


func score():

	if global_position.x >= get_viewport_rect().size.x:
		reset()
		score_p1 += 1

	if global_position.x <= 0:
		reset()
		score_p2 += 1

	$"../Score".text = str(score_p1) + ":" + str(score_p2)


func _win():

	# Evita verificar vitória no 0x0 inicial
	if score_p1 == 0 and score_p2 == 0:
		return

	# Player 1 vence
	if score_p1 >= 3 and score_p1 - score_p2 >= 2:
		$"../Score2".text = "Player 1 Wins"
		$"../Score2".show()
		freeze = true
		game_over = true

	# Player 2 vence
	if score_p2 >= 3 and score_p2 - score_p1 >= 2:
		$"../Score2".text = "Player 2 Wins"
		$"../Score2".show()
		freeze = true
		game_over = true

	# Reiniciar jogo
	if Input.is_key_pressed(KEY_SPACE) and game_over:
		get_tree().reload_current_scene()
