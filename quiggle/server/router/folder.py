## local imports
from quiggle.tools.logs.presets import infolog, labellog, errorlog
from quiggle.tools.reader.folder import FolderStructure
from quiggle.server.router import Router

## global imports
import os

class FolderRouter(Router):

	def __init__(self, route_dir) -> None:
		# set base directory and log
		self.route_dir: str = os.getcwd() + route_dir
		print(infolog(f'-- Initializing routes in { self.route_dir } folder.'))
		# folder structure object
		self.folders:  dict = FolderStructure()
		super().__init__()

	def _set_tree(self):
		return super()._set_tree()

	def define_route_tree(self) -> None:
		self.folders.parse(self.route_dir, self.folders.value)
		self.routes = self.folders.value
		print(labellog('-- Folder router parsing complete.'))

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

	# def get_contents(self, route: str):
	# 	'''
	# 	Get a list of folders and files in the base path.

	# 	Returns:
	# 			dict: A dictionary with 'folders' and 'files' as keys.
	# 	'''
	# 	if not os.path.isdir(route):
	# 		return False
	# 	contents = {'folders': [], 'files': []}
	# 	try:
	# 		for entry in os.listdir(route):
	# 			full_path = os.path.join(route, entry)
	# 			if os.path.isdir(full_path):
	# 				contents['folders'].append(entry)
	# 			elif os.path.isfile(full_path):
	# 				contents['files'].append(entry)
	# 	except Exception as e:
	# 		print(f"Error reading directory: {e}")
	# 	return contents