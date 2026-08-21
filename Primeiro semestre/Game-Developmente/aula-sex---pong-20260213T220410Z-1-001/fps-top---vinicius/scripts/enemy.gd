extends Area2D

# Sinal emitido ao morrer, passa a posição global (usado p/ spawnar loot, por ex.)
signal died(pos: Vector2)

@onready var sprite = $AnimatedSprite2D  # Referência ao sprite animado do inimigo

var speed = 30               # Velocidade de movimento
var velocity = Vector2.ZERO  # Velocidade atual (suavizada pelo lerp)
var life = 90                # Vida atual do inimigo
var is_alive = true          # Flag para evitar processar um inimigo já morto

# =========================================================
# PHYSICS PROCESS — executado a cada frame físico
# =========================================================
func _physics_process(delta: float) -> void:
	# Só move se estiver vivo e ainda na árvore de cenas
	if is_alive and is_inside_tree():
		move(delta)

# =========================================================
# MOVE — persegue o jogador com separação entre inimigos
# =========================================================
func move(delta):
	# Segurança: aborta se o nó foi removido da cena
	if not is_inside_tree():
		return

	# Busca o jogador na cena
	var player = get_tree().get_first_node_in_group("player")
	if not player:
		return

	# Direção básica em linha reta até o jogador
	var direction = global_position.direction_to(player.global_position)

	# ---- Separação entre inimigos (evita empilhamento) ----
	var push = Vector2.ZERO
	for enemy in get_tree().get_nodes_in_group("enemies") if is_inside_tree() else []:
		if enemy != self:
			# Se outro inimigo estiver muito perto (< 40px), aplica repulsão
			if global_position.distance_to(enemy.global_position) < 40:
				push += enemy.global_position.direction_to(global_position)

	# Combina a direção ao jogador com a força de separação e normaliza
	var final_direction = (direction + push).normalized()

	# Suaviza a aceleração com lerp (0.1 = aceleração gradual)
	velocity = velocity.lerp(final_direction * speed, 0.1)

	# Aplica o movimento
	global_position += velocity * delta

	# Espelha o sprite dependendo de qual lado o jogador está
	if global_position.x < player.global_position.x:
		sprite.flip_h = false  # Jogador à direita: sprite normal
	else:
		sprite.flip_h = true   # Jogador à esquerda: sprite espelhado

# =========================================================
# COLISÃO — reage ao contato com balas e com o jogador
# =========================================================
func _on_area_entered(area: Area2D) -> void:
	# ---- Atingido por bala ----
	if area.is_in_group("bullets"):
		$AnimationPlayer.play("hit")  # Toca animação de dano
		life -= area.damage           # Desconta o dano da bala
		area.queue_free()             # Destrói a bala

	# Verifica morte após tomar dano
	if life <= 0:
		die()

	# ---- Colisão com o jogador — mata ambos ----
	if area.get_parent().is_in_group("player"):
		die()
		area.get_parent().die()  # Chama die() no jogador também

# =========================================================
# DIE — lógica de morte do inimigo
# =========================================================
func die():
	# Evita executar die() mais de uma vez (ex: duas colisões simultâneas)
	if not is_alive:
		return

	is_alive = false                   # Marca como morto imediatamente
	sprite.play("death")              # Toca animação de morte
	$CollisionShape2D.queue_free()    # Remove a colisão (não interage mais)
	died.emit(global_position)        # Emite o sinal com a posição (p/ loot etc.)

	# Aguarda 1 segundo (duração da animação) antes de remover da cena
	await get_tree().create_timer(1.0).timeout
	queue_free()
