# def print_class_content(c):
	# print(vars(c))

def init_multiple_values(object, keys, value):
	for key in keys:
		object.__setattr__(key, value)