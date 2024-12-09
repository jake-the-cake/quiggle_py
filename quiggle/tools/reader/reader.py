from quiggle.tools.reader import Parser

class Reader:

	def __init__(self, path: str) -> None:
		self.path:            str = path
		self.original_lines: list = []
		self.updated_lines:  list = []

	def get_lines(self):
		with open(self.path, 'r') as file:
			self.original_lines = file.readlines()
			for line in self.original_lines:
				line = Parser(line, 'text')
		return self.original_lines
	
	def write(self):
		print(''.join(self.updated_lines))