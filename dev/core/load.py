import os
from core.utils.string import unstring_value

def load_settings(search_path = '/'):
	settings = {}
	main_folder_content = os.listdir(search_path)
	if 'config' in main_folder_content:
		config_path = search_path + '/config'
		if 'settings.py' in os.listdir(config_path):
			with open(config_path + '/settings.py', 'r') as file:
				for line in file:
					equal_sign_index = line.find('=')
					if equal_sign_index == -1: continue
					value = line[equal_sign_index + 1:].strip()
					settings[line[:equal_sign_index].strip()] = unstring_value(value)
	print(settings)
	return settings