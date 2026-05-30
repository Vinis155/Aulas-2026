# =========================================================
# SPIDER SPAWNER
# =========================================================
extends Node2D
# =========================================================
# CONFIGURAÇÕES
# =========================================================
var spider_scene : PackedScene = preload("res://prefebs/spider.tscn")
var spider_shoot_scene : PackedScene = preload("res://prefebs/spider_shoot.tscn")
@export var max_spiders := 15
@export var spawn_interval := 5.0
@export var min_distance_from_player := 100.0
@export var deaths_to_respawn := 4
var deaths_since_last_spawn := 0
var last_spider_count := 0
var valid_spawn_cells : Array = []
# =========================================================
# NODES
# =========================================================
@onready var tilemap : TileMap = get_parent().get_node("TileMap")
# =========================================================
# READY
# =========================================================
func _ready():
	await get_tree().process_frame
	_build_valid_cells()
	spawn_all()
	last_spider_count = get_spider_count()
# =========================================================
# MONTAR LISTA DE CÉLULAS VÁLIDAS
# =========================================================
func _build_valid_cells():
	var all_cells = tilemap.get_used_cells(0)
	var cell_set = {}
	for cell in all_cells:
		cell_set[cell] = true

	valid_spawn_cells.clear()
	for cell in all_cells:
		# Célula é válida só se tiver vizinhos em TODAS as 8 direções
		# Isso garante que é uma célula interior (chão), não borda (parede)
		var is_interior = true
		for dx in range(-1, 2):
			for dy in range(-1, 2):
				if dx == 0 and dy == 0:
					continue
				if not cell_set.has(cell + Vector2i(dx, dy)):
					is_interior = false
					break
			if not is_interior:
				break

		if is_interior:
			valid_spawn_cells.append(cell)

	print("Células de spawn válidas: ", valid_spawn_cells.size())
# =========================================================
# CONTAR ARANHAS VIVAS
# =========================================================
func get_spider_count() -> int:
	var count = 0
	for node in get_tree().get_nodes_in_group("enemy"):
		if is_instance_valid(node):
			count += 1
	return count
# =========================================================
# PEGAR POSIÇÃO ALEATÓRIA VÁLIDA
# =========================================================
func get_random_spawn_position() -> Vector2:
	if valid_spawn_cells.is_empty():
		return Vector2.ZERO
	var players = get_tree().get_nodes_in_group("player")
	var attempts = 30
	for i in range(attempts):
		var random_cell = valid_spawn_cells[randi() % valid_spawn_cells.size()]
		var world_pos = tilemap.map_to_local(random_cell)
		var too_close = false
		for player in players:
			if is_instance_valid(player) and player.is_alive:
				if world_pos.distance_to(player.global_position) < min_distance_from_player:
					too_close = true
					break
		if not too_close:
			return world_pos
	return Vector2.ZERO
# =========================================================
# SPAWNAR TODAS ATÉ O MÁXIMO
# =========================================================
func spawn_all():
	var current = get_spider_count()
	var to_spawn = max_spiders - current
	print("Spawning ", to_spawn, " aranhas (total atual: ", current, ")")
	for i in range(to_spawn):
		spawn_spider()
	last_spider_count = get_spider_count()
# =========================================================
# SPAWNAR UMA ARANHA
# =========================================================
func spawn_spider():
	var spawn_pos = get_random_spawn_position()
	if spawn_pos == Vector2.ZERO:
		return
	var scene = spider_scene if randf() < 0.5 else spider_shoot_scene
	if scene == null:
		return
	var spider = scene.instantiate()
	get_parent().add_child(spider)
	spider.global_position = spawn_pos
