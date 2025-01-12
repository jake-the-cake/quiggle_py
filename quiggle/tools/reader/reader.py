## local imports
from quiggle.tools.reader.parser import Parser
from quiggle.tools.printer import Printer

## global imports
from pathlib import Path
import json

class Reader:

	@staticmethod
	def does_file_exist(file_path: Path) -> bool:
		if not file_path.exists():
			Printer(f'Could not find file "{ file_path }"').text('yellow')
			return False
		return True
		
	def __init__(self, file: str) -> None:
		self.file:                 str = file
		self.original_data: str | list = None
		self.updated_data:         str = ''
		self.updated_lines:       list = []
		self.check_valid_path()

	def setup_parent_directories(self, parent_path: Path) -> bool:
		if not parent_path.exists():
			self.setup_parent_directories(parent_path.parent)
			parent_path.mkdir()
			Printer(f'Created directory "{ parent_path }"').text('yellow')
	def check_valid_path(self) -> None:
		file_path = Path(self.file)
		if not Reader.does_file_exist(file_path):
			self.setup_parent_directories(file_path.parent)
			file_path.touch()
			Printer(f'Created file "{ file_path }"').text('yellow')

	def get_lines(self) -> list:
		with open(self.file, 'r') as file:
			self.original_data = []
			for line in file.readlines():
				self.original_data.append(Parser(line, 'text'))
		return self.original_data
	
	def get_json(self):
		with open(self.file, 'r') as file:
			data = file.read()
			if data != '':
				self.original_data = json.loads(data)
				self.updated_data = self.original_data
			else: self.updated_data = { "data": [] }

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