def trim_array(array, location = 'both'):
	if location == 'start' or 'both':
		while array[0] == '': array = remove_first_item_in_array(array)
	if location == 'end' or 'both':
		while array[-1] == '': array = remove_last_item_in_array(array)
	return array

def remove_first_item_in_array(array):
	return array[1:]

def remove_last_item_in_array(array):
	return array[:-1]

def get_first_item_in_array(array):
	return array[0]

def get_last_item_in_array(array):
	return array[-1]

def all_values_equal(array, value) -> bool:
	for item in array:
		if item != value: return False
	return True

class Array:
	cut_first = remove_first_item_in_array
	cut_last = remove_last_item_in_array
	get_first = get_first_item_in_array
	get_last = get_last_item_in_array
	trim = trim_array
	all_values_equal = all_values_equal