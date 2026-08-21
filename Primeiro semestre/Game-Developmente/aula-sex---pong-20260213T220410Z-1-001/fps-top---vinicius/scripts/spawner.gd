extends Node2D

# Cena do inimigo a ser instanciada nas waves
@export var enemy_scene : PackedScene

# =========================================================
# MAPA — limites do campo de jogo em pixels
# =========================================================
@export_category("Mapa (limites em pixels)")
@export var map_x_min : float = 8.0
@export var map_x_max : float = 320.0
@export var map_y_min : float = 0.0
@export var map_y_max : float = 160.0

# =========================================================
# WAVES — configuração de dificuldade progressiva
# =========================================================
@export_category("Wave Config")
@export var enemies_first_wave : int = 3           # Inimigos na wave 1
@export var enemies_per_wave_increase : int = 1    # Inimigos extras por wave
@export var time_between_waves : float = 3.0       # Pausa entre waves

# =========================================================
# SPAWN — zona de segurança ao redor do jogador
# =========================================================
@export_category("Spawn Config")
@export var safe_radius : float = 40.0  # Inimigos não spawnam dentro desse raio

# =========================================================
# LOOT — chance de arma cair ao matar inimigo
# =========================================================
@export_category("Loot Config")
@export var drop_chance : float = 0.5  # 0.0 = nunca, 1.0 = sempre

# Todas as armas possíveis no loot aleatório
var weapon_scenes = [
	"res://prefabs/crossbow.tscn",
	"res://prefabs/Kunai.tscn",
	"res://prefabs/machine_gun.tscn",
	"res://prefabs/pistol.tscn",
	"res://prefabs/Shotgun.tscn"
]

# Armas que podem aparecer no início (sem kunai — muito forte de início)
var starter_weapons = [
	"res://prefabs/crossbow.tscn",
	"res://prefabs/machine_gun.tscn",
	"res://prefabs/pistol.tscn",
	"res://prefabs/Shotgun.tscn"
]

var current_wave := 0     # Número da wave atual
var enemies_alive := 0    # Contador de inimigos restantes na wave
var wave_label : Label    # Label criado via código para mostrar "Wave X"

# =========================================================
# READY — inicializa o jogo
# =========================================================
func _ready():
	randomize()  # Garante aleatoriedade diferente a cada execução

	# Cria um CanvasLayer separado para a UI (layer 10 = acima do jogo)
	var canvas = CanvasLayer.new()
	canvas.layer = 10
	add_child(canvas)

	# Cria e configura o label de wave via código
	wave_label = Label.new()
	wave_label.visible = false
	wave_label.position = Vector2(100, 60)
	wave_label.add_theme_color_override("font_color", Color.RED)
	wave_label.add_theme_font_size_override("font_size", 32)

	# Carrega fonte customizada se disponível
	var font = load("res://fonts/RubikWetPaint-Regular.ttf")
	if font:
		wave_label.add_theme_font_override("font", font)

	canvas.add_child(wave_label)

	# Aguarda um frame para garantir que a cena está pronta
	await get_tree().process_frame

	# Spawna arma inicial no centro do mapa
	var center = Vector2(
		(map_x_min + map_x_max) / 2,
		(map_y_min + map_y_max) / 2
	)
	drop_starter_weapon(center)

	# Pequena pausa antes da primeira wave
	await get_tree().create_timer(1).timeout
	start_next_wave()

# =========================================================
# GET PLAYER — retorna o primeiro jogador do grupo
# =========================================================
func get_player():
	var players = get_tree().get_nodes_in_group("player")
	if players.size() > 0:
		return players[0]
	return null

# =========================================================
# GET SAFE SPAWN POSITION
# Tenta até 20 vezes achar posição longe do jogador.
# Se não conseguir, retorna posição aleatória sem verificação.
# =========================================================
func get_safe_spawn_position():
	var player = get_player()

	for i in range(20):
		var pos = Vector2(
			randf_range(map_x_min, map_x_max),
			randf_range(map_y_min, map_y_max)
		)
		# Aceita a posição se não há jogador ou se está fora do raio seguro
		if player == null or pos.distance_to(player.global_position) >= safe_radius:
			return pos

	# Fallback: após 20 tentativas, spawna em qualquer lugar
	return Vector2(
		randf_range(map_x_min, map_x_max),
		randf_range(map_y_min, map_y_max)
	)

# =========================================================
# DROP STARTER WEAPON — spawna arma inicial no centro
# =========================================================
func drop_starter_weapon(pos):
	var path = starter_weapons.pick_random()
	if !ResourceLoader.exists(path):
		return
	var packed = load(path)
	if packed == null:
		return
	var weapon = packed.instantiate()
	# Deferred evita adicionar filho durante _ready de outro nó
	call_deferred("add_weapon_to_scene", weapon, pos)

# =========================================================
# DROP RANDOM WEAPON — loot ao matar inimigo
# =========================================================
func drop_random_weapon(pos):
	var path = weapon_scenes.pick_random()
	if !ResourceLoader.exists(path):
		return
	var packed = load(path)
	if packed == null:
		return
	var weapon = packed.instantiate()
	call_deferred("add_weapon_to_scene", weapon, pos)

# =========================================================
# ADD WEAPON TO SCENE — adiciona arma na posição correta
# =========================================================
func add_weapon_to_scene(weapon, pos):
	if weapon == null:
		return
	add_child(weapon)
	weapon.global_position = pos

# =========================================================
# START NEXT WAVE — avança wave, mostra label e spawna inimigos
# =========================================================
func start_next_wave():
	current_wave += 1

	# Fórmula de escalonamento: wave 1 = base, cada wave seguinte += incremento
	var enemy_count = (
		enemies_first_wave + (current_wave - 1) * enemies_per_wave_increase
	)

	# Exibe "Wave X" na tela
	wave_label.text = "Wave %d" % current_wave
	wave_label.visible = true

	# Pausa antes de spawnar
	await get_tree().create_timer(time_between_waves).timeout

	# Fade out do label via Tween (alpha de 1 → 0 em 0.5s)
	var tween = create_tween()
	tween.tween_property(wave_label, "modulate:a", 0, 0.5)
	await tween.finished

	wave_label.visible = false
	spawn_enemies(enemy_count)

# =========================================================
# SPAWN ENEMIES — instancia e conecta sinal de cada inimigo
# =========================================================
func spawn_enemies(count):
	if enemy_scene == null:
		push_error("enemy_scene não configurado!")
		return

	enemies_alive = count

	for i in range(count):
		var enemy = enemy_scene.instantiate()
		add_child(enemy)
		enemy.global_position = get_safe_spawn_position()

		# Conecta o sinal "died" para rastrear quantos ainda estão vivos
		if enemy.has_signal("died"):
			enemy.died.connect(_on_enemy_died)

# =========================================================
# ON ENEMY DIED — atualiza contador e spawna loot/próxima wave
# =========================================================
func _on_enemy_died(pos):
	enemies_alive -= 1

	# Chance de dropar arma na posição onde o inimigo morreu
	if randf() <= drop_chance:
		call_deferred("drop_random_weapon", pos)

	# Se todos morreram, inicia próxima wave após pausa
	if enemies_alive <= 0:
		if !is_inside_tree():
			return
		await get_tree().create_timer(1.5).timeout
		start_next_wave()
