## local imports
from quiggle.tools.reader.parser import Parser
from quiggle.tools.logs.presets import infolog

## global imports
from pathlib import Path
import json

class Reader:

	@staticmethod
	def does_file_exist(file_path: Path) -> bool:
		if not file_path.exists():
			print(infolog(f'Could not find "{ file_path }"'))
			return False
		return True
		
	def __init__(self, file: str) -> None:
		self.file:            str = file
		self.original_data:   str = ''
		self.updated_data:    str = ''
		self.original_lines: list = []
		self.updated_lines:  list = []
		self.check_valid_path()

	def setup_parent_directories(self, parent_path: Path) -> bool:
		if not parent_path.exists():
			self.setup_parent_directories(parent_path.parent)
			parent_path.mkdir()
			print(infolog(f'Created directory "{ parent_path }"'))

	def check_valid_path(self) -> None:
		file_path = Path(self.file)
		if not Reader.does_file_exist(file_path):
			self.setup_parent_directories(file_path.parent)
			file_path.touch()
			print(infolog(f'Created file "{ file_path }".'))

	def get_lines(self) -> list:
		with open(self.file, 'r') as file:
			for line in file.readlines():
				self.original_lines.append(Parser(line, 'text'))
		return self.original_lines
	
	def get_json(self):
		with open(self.file, 'r') as file:
			self.original_data = json.load()

	def get_data(self) -> str:
		with open(self.file, 'r') as file:
			self.original_data = file.read()
		return self.original_data
	
	def prewrite_line(self, line: str) -> None:
		self.updated_lines.append(line)

	def write(self, mode = 'lines') -> None:
		with open(self.file, 'w') as file:
			if mode == 'lines':
				file.write(''.join(self.updated_lines))
			elif mode == 'data':
				file.write(self.updated_data)