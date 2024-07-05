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

def get_last_item_in_array(array):
	return array[-1]

class Array:
	cut_first = remove_first_item_in_array
	cut_last = remove_last_item_in_array
	get_last = get_last_item_in_array
	trim = trim_array