## local imports
from quiggle.tools.reader.folder import FolderStructure
from quiggle.tools.printer import Printer,print_note

class Router:

	def __init__(self):
		self.routes: dict = {}
		self.tree:   dict = self._set_tree()
		self._set_routes()

	def _has_special_prefix(self, path: str, prefix: str) -> bool:
		return path.startswith(f'/{ prefix }/') or path == f'/{ prefix }'

	def _set_tree(self, tree = None):
		if tree == None: raise Exception('No folder tree found.')
		return tree
		
	def _set_routes(self) -> list:
		print_note('Sorting routes.')
		return FolderStructure(self.tree).paths()

	def _is_dynamic_route(self, route: str) -> bool:
		return any(segment.startswith('$') for segment in route.split('/'))

	def _sort_route(self, route: str, protocol: str):
		if self._is_dynamic_route(route):
			self.routes[protocol]['dynamic'].append(route)
		else: self.routes[protocol]['static'].append(route)

	def _add_protocol(self, protocol: str):
		self.routes[protocol] = self._protocol_dict()

	def _protocol_dict(self):
		return { 'static': [], 'dynamic': [] }

	def check_route(self):
		pass

	def check_dynamic_route(self):
		pass
