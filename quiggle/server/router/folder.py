## local imports
from quiggle.server.prompts import MESSAGES
from quiggle.server.router import Router
from quiggle.tools.printer import Printer, print_note
from quiggle.tools.reader.folder import FolderStructure

## global imports
import os
from pathlib import Path
import importlib.util

class FolderRouter(Router):

	def __init__(self, settings: dict) -> None:
		self.settings = settings
		self._check_required_settings()
		self.route_dir: str = str(Path.cwd()) + '/server' + self.settings['ROUTE_FOLDER']
		print_note(f'Initializing routes in { self.route_dir } folder.')
		super().__init__()

	def _check_required_settings(self):
		keys = [
			'API_ROUTE_PREFIX',
		]
		for key in keys:
			if key not in self.settings:
				from quiggle.server.router import not_set
				raise not_set(key, self.settings['filename'])

	def _set_tree(self):
		tree = FolderStructure().parse(self.route_dir)
		print_note(MESSAGES['parsed']('Folder'))
		return super()._set_tree(tree)

	def _set_routes(self):
		self._add_protocol('html')
		self._add_protocol('api')
		routes: list = super()._set_routes()
		for route in routes:
			if os.path.exists(self.route_dir + route + '/view.py'):
				self._sort_route(route, 'html')
			if os.path.exists(self.route_dir + route + '/api.py'):
				self._sort_route(route, 'api')
		print_note(MESSAGES['parsed']('Route'))

	def _get_callable(self, page_name: str, prefix: str, endpoint: Path):
		file_path = endpoint / f'{ page_name }.py'
		if endpoint.__str__() in self.routes[prefix]['static']:
			module_name = file_path.stem
			spec = importlib.util.spec_from_file_location(module_name, self.route_dir + file_path.__str__())
			module = importlib.util.module_from_spec(spec)
			spec.loader.exec_module(module)
			return module

	def find_route(self, request) -> str:
		module = None
		method = request.method
		prefix = self.settings['API_ROUTE_PREFIX']

		if self._has_special_prefix(request.path, prefix):
			method = method.lower()
			module = self._get_callable(prefix, prefix, Path(request.path.replace(f'/{ prefix }', '') or '/'))
		else:
			method = 'view'
			module = self._get_callable('view', 'html', Path(request.path))

		if module == None:
			return 404
		elif hasattr(module, method):
			return getattr(module, method)
		else:
			return 405