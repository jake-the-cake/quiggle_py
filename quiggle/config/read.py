def read_local_file_variables(filename: str):
	with open(filename) as file:
		data = {}
		exec(file.read(), data)
		return data