## global imports
from pathlib import Path

class FolderStructure:
	
	@staticmethod
	def new_dir() -> dict:
		return { '__main__': [] }
	
	def __init__(self):
		self.value = FolderStructure.new_dir()

	def find_contents(self, parent, dictionary) -> None:
		parent = Path(parent)
		for item in parent.iterdir():
			if item.is_file():
				dictionary['__main__'].append(item.name)
			else:
				dictionary[item.name] = FolderStructure.new_dir()
				self.find_contents(item, dictionary[item.name])