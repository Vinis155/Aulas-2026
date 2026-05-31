extends Camera2D

@export var player1: Node2D
@export var player2: Node2D

@export var max_distance := 600.0
@export var min_zoom := 0.8  # Mais longe (mostra mais do mapa)
@export var max_zoom := 1.5  # Mais perto (foco nos players)
@export var smooth_speed := 5.0 # Aumentei para uma resposta mais rápida no delta

func _process(delta):
	var targets = []
	
	# 🔍 Verifica quem está disponível e vivo
	if player1 and player1.get("is_alive"):
		targets.append(player1.global_position)
	if player2 and player2.get("is_alive"):
		targets.append(player2.global_position)
	
	# ❌ Ninguém vivo: não faz nada
	if targets.size() == 0:
		return

	# 🎯 Cálculo da posição alvo (Média entre os vivos)
	var target_pos = Vector2.ZERO
	for p in targets:
		target_pos += p
	target_pos /= targets.size()
	
	# Suaviza o movimento da posição
	global_position = global_position.lerp(target_pos, smooth_speed * delta)
	
	# 🔍 Cálculo do Zoom
	var target_zoom_val = max_zoom # Padrão: zoom próximo
	
	if targets.size() > 1:
		var dist = targets[0].distance_to(targets[1])
		# Quanto maior a distância, MENOR o valor do zoom (para afastar)
		# Usamos o inverse_lerp para mapear a distância no intervalo do zoom
		var zoom_factor = clamp(1.0 - (dist / max_distance), 0.0, 1.0)
		target_zoom_val = lerp(min_zoom, max_zoom, zoom_factor)
	
	var target_zoom = Vector2(target_zoom_val, target_zoom_val)
	zoom = zoom.lerp(target_zoom, smooth_speed * delta)
