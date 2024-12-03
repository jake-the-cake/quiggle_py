## global imports
import os

base_dir = os.getcwd()

def read_local_file_variables(filename: str):
	with open(os.path.join(base_dir, filename)) as file:
		data = {}
		exec(file.read(), data)
		return data