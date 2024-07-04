def unstring_value(value):
	if value == 'True' or value == 'False':
		return bool(value)