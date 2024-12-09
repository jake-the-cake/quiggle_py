from quiggle.tools.reader.parser import Parser

class Reader:

	def __init__(self, path: str) -> None:
		self.path:            str = path
		self.original_lines: list = []
		self.updated_lines:  list = []

	def get_lines(self) -> list:
		with open(self.path, 'r') as file:
			for line in file.readlines():
				self.original_lines.append(Parser(line, 'text'))
		return self.original_lines
	
	def prewrite_line(self, line: str) -> None:
		self.updated_lines.append(line)

	def write(self) -> None:
		print(''.join(self.updated_lines))