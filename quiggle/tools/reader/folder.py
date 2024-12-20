## global imports
from pathlib import Path

class FolderStructure:
	
	def __init__(self, tree = {}):
		self.tree:  dict = self._validate_tree(tree)
		self.path_list: list = []

	def parse(self, parent, dictionary = None) -> None:
		parent = Path(parent)
		if dictionary == None: dictionary = self.tree
		for item in parent.iterdir():
			if item.is_file():
				dictionary[item.name] = None
			if item.is_dir():
				dictionary[item.name] = {}
				self.parse(item, dictionary[item.name])
		return self.tree

	def paths(self, path = Path('/'), dictionary = None) -> list:
		if dictionary == None: dictionary = self.tree
		for key in dictionary.keys():
			if dictionary[key] == None:
				file_path = path.__str__()
				if file_path not in self.path_list:
					self.path_list.append(file_path)				
			if isinstance(dictionary[key], dict):
				self.paths(path / key, dictionary[key])
		return self.path_list

	def _check_string(self, value) -> None:
		if not isinstance(value, str): 
			raise Exception('Tree key must be a string.')
	
	def _check_value(self, value) -> None:
		if value == None: return None
		if isinstance(value, dict):
			return self._check_dirs(value)
		raise Exception('Invalid tree format.')
	
	def _check_dirs(self, parent) -> bool:
		for key in parent.keys():
			self._check_string(key)
			self._check_value(parent[key])

	def _validate_tree(self, tree: dict):
		self._check_dirs(tree)
		return tree