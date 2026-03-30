extends Area2D  # Área que detecta colisão (não usa física como corpo)

@export_category("Moviment Settings")  
# Cria uma categoria no Inspector (organização visual)

@export_enum("Up", "Down", "Left", "Right")
var move_dir: int  
# Permite escolher direção no editor (0=Up, 1=Down, 2=Left, 3=Right)

@export var speed: float = 100  
# Velocidade da serra

@export_range(50.0,500.0,5.0, "Distancia maxima da serra")
var distance: float = 50.0  
# Distância máxima que a serra percorre antes de inverter

var dir: Vector2  # Direção atual do movimento (vetor)

@onready var start_position = global_position  
# Guarda a posição inicial da serra

func _ready() -> void:
	set_dir()  # Define direção inicial com base no move_dir
	pass
	
	
func _physics_process(delta: float) -> void:
	move(delta)  # Executa movimento a cada frame da física
	pass
	
func move(delta):
	
	global_position += dir * speed * delta  
	# Move a serra na direção escolhida
	
	# Verifica se atingiu a distância máxima
	if global_position.distance_to(start_position) >= distance:
		dir = -dir  # Inverte direção
		start_position = global_position  # Atualiza ponto de referência
	
	pass
	
func set_dir():
	dir = Vector2()  # Reseta direção
	
	# Define direção com base no valor escolhido no Inspector
	match move_dir:
		0:
			dir = Vector2(0,-1)  # Cima
		1:
			dir = Vector2(0,1)   # Baixo
		2:
			dir = Vector2(-1,0)  # Esquerda
		3:
			dir = Vector2(1,0)   # Direita
	
	pass


func _on_area_entered(area: Area2D) -> void:
	
	# Verifica se o objeto que entrou pertence ao grupo "Player"
	if area.get_parent().is_in_group("Player"):
		area.get_parent().die()  # Chama função de morte do player
	
	pass  # Pode remover
	
