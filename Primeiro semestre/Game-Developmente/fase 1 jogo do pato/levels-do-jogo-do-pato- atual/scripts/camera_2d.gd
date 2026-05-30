# =========================================================
# CAMERA COOP TOPDOWN
# =========================================================
extends Camera2D


# =========================================================
# CONFIGURAÇÕES
# =========================================================

const SMOOTH_SPEED := 8.0
const ZOOM_CLOSE := 2.0   # zoom quando players estão juntos
const ZOOM_FAR := 1.5     # zoom quando players estão longe


# =========================================================
# VARIÁVEIS
# =========================================================

var players = []


# =========================================================
# READY
# =========================================================
func _ready():
	enabled = true
	zoom = Vector2(ZOOM_CLOSE, ZOOM_CLOSE)
	players = get_tree().get_nodes_in_group("player")


# =========================================================
# PROCESS
# =========================================================
func _process(delta):
	if players.size() == 0:
		return

	# =========================================
	# FILTRA APENAS PLAYERS VIVOS
	# =========================================
	var alive_players = []
	for p in players:
		if is_instance_valid(p) and p.is_alive:
			alive_players.append(p)

	if alive_players.size() == 0:
		return

	# =========================================
	# CENTRO DOS PLAYERS VIVOS
	# =========================================
	var center = Vector2.ZERO
	for p in alive_players:
		center += p.global_position
	center /= alive_players.size()

	# =========================================
	# MOVE CÂMERA SUAVEMENTE
	# =========================================
	global_position = global_position.lerp(center, SMOOTH_SPEED * delta)

	# =========================================
	# ZOOM DINÂMICO
	# =========================================
	var target_zoom := ZOOM_CLOSE

	if alive_players.size() >= 2:
		var dist = alive_players[0].global_position.distance_to(
			alive_players[1].global_position
		)
		# Começa a abrir o zoom a partir de 100px de distância
		target_zoom = clamp(
			ZOOM_CLOSE - (dist - 100.0) / 300.0,
			ZOOM_FAR,
			ZOOM_CLOSE
		)

	var new_zoom = lerp(zoom.x, target_zoom, SMOOTH_SPEED * delta)
	zoom = Vector2(new_zoom, new_zoom)
