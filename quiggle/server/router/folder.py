## local imports
from quiggle.tools.logs.presets import infolog
from quiggle.tools.reader.folder import FolderStructure
from quiggle.server.router import Router, MESSAGES
from quiggle.config.root import get_config

## global imports
import os
from pathlib import Path

class FolderRouter(Router):

	def __init__(self, settings: dict) -> None:
		self.settings = settings
		self._check_required_settings()
		self.route_dir: str = str(Path.cwd()) + self.settings['ROUTE_FOLDER']
		print(infolog(f'-- Initializing routes in { self.route_dir } folder.'))
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
		print(MESSAGES['parsed']('Folder'))
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
		print(MESSAGES['parsed']('Route'))

	def find_route(self, path: str) -> str:
		prefix = self.settings['API_ROUTE_PREFIX']
		if self._has_special_prefix(path, prefix):
			stripped_path = path.replace(f'/{ prefix }', '') or '/'
			if stripped_path in self.routes[prefix]['static']: return stripped_path
			
		''' find the matching path '''

		if self._is_dynamic_route(path):
			return 'dynamic'
		return 'path'


	# def check_route(self, request, keys: list) -> bool:



	# 	if keys[0] == '': keys = keys[1:]
	# 	for key in routes.keys():
	# 		if key == keys[0]:
	# 			if len(keys) == 1: return True
	# 			return self.check_route(routes[key], keys[1:])
	# 	return False

	# def find_route(self, request, response):
	# 	keys = (request.path.split('/') + ['__main__'])[1:]
	# 	if not self.check_route(self.routes, keys):
	# 		response.status_code = 404
	# 		return response.init_body(response.use_default_page())
	# 	response.status_code = 200
	# 	return response.init_body(response.use_default_page())