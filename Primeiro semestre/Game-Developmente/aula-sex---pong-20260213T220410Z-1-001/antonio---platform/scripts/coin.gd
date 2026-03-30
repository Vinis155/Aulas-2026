extends Area2D  # Área que detecta colisão (coleta)



@onready var anim: AnimatedSprite2D = $AnimatedSprite2D  # Animação da moeda

func _ready():
	anim.play("idle")  # Animação girando da moeda


func _on_area_entered(area: Area2D) -> void:
	
	# Verifica se quem entrou é o Player
	if area.get_parent().is_in_group("Player"):
		
		print("Pegou moeda!")  # Debug
		
		# Aqui você pode somar ponto (exemplo simples)
		# area.get_parent().score += 1
		
		anim.play("collect")  # Animação de coleta
		
		$CollisionShape2D.disabled = true  # Evita coletar mais de uma vez
		
		await anim.animation_finished  # Espera animação terminar
		
		queue_free()  # Remove a moeda da cena
		
		area.get_parent().coins += 1
