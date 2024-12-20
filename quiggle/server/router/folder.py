## local imports
from quiggle.tools.logs.presets import infolog, labellog, errorlog
from quiggle.tools.reader.folder import FolderStructure
from quiggle.server.router import Router, MESSAGES, parsing_complete

## global imports
import os

class FolderRouter(Router):

	def __init__(self, route_dir) -> None:
		self.route_dir: str = os.getcwd() + route_dir
		print(infolog(f'-- Initializing routes in { self.route_dir } folder.'))
		super().__init__()

	def _set_tree(self):
		tree = FolderStructure().parse(self.route_dir)
		print(MESSAGES['parsed']('Folder'))
		return super()._set_tree(tree)

	def _set_routes(self):
		routes: list = super()._set_routes()
		for route in routes:
			if os.path.exists(self.route_dir + route + '/view.py'):
				print('has view')
			if os.path.exists(self.route_dir + route + '/api.py'):
				print('has api')
		print(MESSAGES['parsed']('Route'))

	def check_route(self, routes: dict, keys: list) -> bool:
		if keys[0] == '': keys = keys[1:]
		for key in routes.keys():
			if key == keys[0]:
				if len(keys) == 1: return True
				return self.check_route(routes[key], keys[1:])
		return False

	def find_route(self, request, response):
		keys = (request.path.split('/') + ['__main__'])[1:]
		if not self.check_route(self.routes, keys):
			response.status_code = 404
			return response.init_body(response.use_default_page())
		response.status_code = 200
		return response.init_body(response.use_default_page())