extends Node

var player_devices := {1: -1, 2: -1}
var debug_label : Label

func _ready():
	Input.joy_connection_changed.connect(_on_joy_connection_changed)

	debug_label = Label.new()
	debug_label.position = Vector2(10, 10)
	debug_label.z_index = 100
	get_tree().root.call_deferred("add_child", debug_label)

func _process(_delta):
	# Tenta detectar sempre, pois no navegador demora para aparecer
	_assign_connected_joypads()

	var joypads = Input.get_connected_joypads()
	if debug_label:
		debug_label.text = "Joypads: " + str(joypads) + "\nDevices: " + str(player_devices)

func _assign_connected_joypads():
	var joypads = Input.get_connected_joypads()
	for i in joypads.size():
		var device = joypads[i]
		if i == 0:
			player_devices[1] = device
		elif i == 1:
			player_devices[2] = device

func _on_joy_connection_changed(device: int, connected: bool):
	if connected:
		_assign_connected_joypads()
	else:
		for pid in player_devices:
			if player_devices[pid] == device:
				player_devices[pid] = -1

func get_device(player_id: int) -> int:
	return player_devices.get(player_id, -1)
