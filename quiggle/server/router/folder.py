## local imports
from quiggle.tools.logs.presets import infolog, labellog, errorlog
from quiggle.tools.reader.folder import FolderStructure
from quiggle.server.router import Router, MESSAGES, parsing_complete

## global imports
import os
from pathlib import Path

class FolderRouter(Router):

	def __init__(self, route_dir) -> None:
		self.route_dir: str = str(Path.cwd()) + route_dir
		print(self.route_dir)
		print(infolog(f'-- Initializing routes in { self.route_dir } folder.'))
		super().__init__()

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
		if path.startswith('/api/') or path == '/api':
			stripped_path = path.replace('/api', '') or '/'
			if stripped_path in self.routes['api']['static']: return stripped_path
			
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