def control():
	command = int(input("chose default: 1 or custom: 2 or exit: 3"))
	while command != 3:
		if command == 1:
			init_default_hex()
			break
		elif command == 2:
			init_custom_hex()
			break
	command = input("chose: forward, back, left, right, fast, slow, stop, exit\n")
	while command != "exit":
		if command == "forward":
			move_forward()
		elif command == "back":
			move_back()
		elif command == "left":
			change_curvature()
		elif command == "right":
			change_curvature()
		elif command == "fast":
			change_speed()
		elif command == "slow":
			change_speed()
		elif command == "stop":
			default_pos()
		elif command == "exit":
			break
		command = input("chose: forward, back, left, right, fast, slow, stop, exit\n")