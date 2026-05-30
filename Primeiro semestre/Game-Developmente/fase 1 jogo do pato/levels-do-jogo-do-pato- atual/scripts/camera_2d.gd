# =========================================================
# CAMERA PVP TOPDOWN
# =========================================================
extends Camera2D


# =========================================================
# CONFIGURAÇÕES
# =========================================================

# Suavidade da câmera
@export var smooth_speed := 3.0

# Zoom fixo da câmera
@export var camera_zoom := 0.6


# =========================================================
# VARIÁVEIS
# =========================================================

# Lista de jogadores
var players = []


# =========================================================
# READY
# =========================================================
func _ready():

	# Ativa câmera
	enabled = true

	# Define zoom inicial
	zoom = Vector2(camera_zoom, camera_zoom)

	# Pega todos jogadores do grupo "player"
	players = get_tree().get_nodes_in_group("player")


# =========================================================
# PROCESS
# =========================================================
func _process(delta):

	# Se não existir player
	if players.size() == 0:
		return


	# =========================================
	# CENTRO DOS PLAYERS
	# =========================================
	var center = Vector2.ZERO

	var valid_players = 0


	# Soma posição dos jogadores
	for p in players:

		if is_instance_valid(p):

			center += p.global_position

			valid_players += 1


	# Evita divisão por zero
	if valid_players == 0:
		return


	# Média das posições
	center /= valid_players


	# =========================================
	# MOVE CÂMERA SUAVEMENTE
	# =========================================
	global_position = global_position.lerp(
		center,
		smooth_speed * delta
	)
