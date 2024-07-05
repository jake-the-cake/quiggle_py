def unstring_value(value):
	if value == 'True' or value == 'False':
		return bool(value)
	
def remove_text(original_value: str, remove_value: str) -> str:
	return original_value.replace(remove_value, '')