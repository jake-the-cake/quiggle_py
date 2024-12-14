## local imports
from quiggle.tools.logs.presets import infolog, labellog, errorlog
from quiggle.tools.reader.folder import FolderStructure

## global imports
import os

class FolderRouter:

	def __init__(self, base_dir) -> None:
		# set base directory and log
		self.base_dir: str = os.getcwd() + base_dir
		print(infolog(f'Initializing routes in { self.base_dir } folder.'))
		# define routes as a folder structure object
		self.routes:  dict = {}
		self.folders: dict = FolderStructure()
		self.define_route_tree()

	def define_route_tree(self) -> None:
		self.folders.find_contents(self.base_dir, self.routes.value)
		
		# set routes to the object value
		self.routes: dict = self.folders.value
		print(self.routes)

	def find_route(self, request, response):
		self.route = self.base_dir + request.path
		print(self.route)
		contents = self.get_contents()
		if not contents:
			response.status_code = 404
			return response.init_body(response.use_default_page())
		response.status_code = 200
		return response.init_body(response.use_default_page())

	def get_contents(self):
		'''
		Get a list of folders and files in the base path.

		Returns:
				dict: A dictionary with 'folders' and 'files' as keys.
		'''
		if not os.path.isdir(self.route):
			return False
		contents = {'folders': [], 'files': []}
		try:
			for entry in os.listdir(self.route):
				full_path = os.path.join(self.route, entry)
				if os.path.isdir(full_path):
					contents['folders'].append(entry)
				elif os.path.isfile(full_path):
					contents['files'].append(entry)
		except Exception as e:
			print(f"Error reading directory: {e}")
		return contents