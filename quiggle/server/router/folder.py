## local imports
from quiggle.tools.logs.presets import infolog, labellog, errorlog
from quiggle.tools.reader.folder import FolderStructure
from quiggle.vars.array import Array

## global imports
import os

class FolderRouter:

	def __init__(self, base_dir) -> None:
		# set base directory and log
		self.base_dir: str = os.getcwd() + base_dir
		print(infolog(f'Initializing routes in { self.base_dir } folder.'))
		# define routes as a folder structure object
		self.folders: dict = FolderStructure()
		self.routes:  dict = {}
		self.define_route_tree()

	def define_route_tree(self) -> None:
		self.folders.find_contents(self.base_dir, self.folders.value)
		self.routes = self.folders.value
		print(labellog('Folder router parsing complete.'))

	def check_route(self, routes: dict, keys: list) -> bool:
		return True
		# if keys[0] == '': keys = keys[1:]
		# query = None
		# alternates = []
		# for key in routes.keys():
		# 	if key[0] == '$':
		# 		alternates.append(routes[key])
		# 	if key == keys[0]:
		# 		query = routes[key]
		# if not query:
		# 	if len(alternates) == 0 or len(keys) == 1: return False
		# 	if len(alternates) == 1: return self.check_route(alternates[0], keys[1:])
		# 	print('handle multiple alternates')
		# 	return False
		# if len(keys) == 1: return True
		# return self.check_route(query, keys[1:])

	def find_route(self, request, response):
		keys = (request.path.split('/') + ['__main__'])[1:]
		contents = None
		if self.check_route(self.routes, keys):
			contents = True
		route = self.base_dir + request.path

		if not contents:
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