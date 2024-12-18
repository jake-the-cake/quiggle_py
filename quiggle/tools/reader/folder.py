## global imports
from pathlib import Path

class FolderStructure:
	
	def __init__(self):
		self.value = {}

	def parse(self, parent, dictionary) -> None:
		parent = Path(parent)
		for item in parent.iterdir():
			if item.is_file():
				dictionary[item.name] = None
			if item.is_dir():
				dictionary[item.name] = {}
				self.find_contents(item, dictionary[item.name])