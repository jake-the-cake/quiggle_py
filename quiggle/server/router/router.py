## local imports
from quiggle.tools.reader.folder import FolderStructure
from quiggle.tools.logs.presets import errorlog, labellog, infolog

class Router:

	def __init__(self):
		self.routes: dict = {
			'api': {
				'static': [],
				'dynamic': []
			},
			'html': {
				'static': [],
				'dynamic': []
			}
		}
		self.tree: dict = self._set_tree()
		self._set_routes()

	def _set_tree(self, tree = None):
		if tree == None:
			raise Exception(f'{ errorlog(f'No tree found.') } >>> { Router._set_tree.__str__() }')	
		return tree
		
	def _set_routes(self) -> list:
		print(infolog('-- Sorting routes.'))
		routes: list = FolderStructure(self.tree).paths()
		return routes

	def is_dynamic_route(self, dictionary: dict) -> bool:
		return True

	def check_route(self):
		pass

	def check_dynamic_route(self):
		pass
