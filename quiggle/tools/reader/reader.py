## local imports
from quiggle.tools.reader.parser import Parser

## global imports
from pathlib import Path

class Reader:

	def __init__(self, file: str) -> None:
		self.file:            str = file
		self.original_lines: list = []
		self.updated_lines:  list = []
		self.check_valid_path()

	def check_valid_path(self) -> None:
		file_path = Path(self.file)
		if not file_path.exists():
			file_path.touch()

	def get_lines(self) -> list:
		with open(self.file, 'r') as file:
			for line in file.readlines():
				self.original_lines.append(Parser(line, 'text'))
		return self.original_lines
	
	def prewrite_line(self, line: str) -> None:
		self.updated_lines.append(line)

	def write(self) -> None:
		# with open(self.path, 'w') as file:
			print(''.join(self.updated_lines))