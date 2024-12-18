## local imports
from quiggle.tools.reader.folder import FolderStructure

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

	def _set_tree(self):
		print('super', self._set_tree.__name__)

	def _set_routes(self):
		pass

	def check_route(self):
		pass

	def check_dynamic_route(self):
		pass
