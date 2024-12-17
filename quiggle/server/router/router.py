## local imports
from quiggle.config.read import read_local_file_variables
from quiggle.config.root import config_root
from quiggle.server.router.folder import FolderRouter

config_file: str = config_root('globals')
settings:   list = read_local_file_variables(config_file)
r_type:      str = 'ROUTER_TYPE'
r_folder:    str = 'ROUTE_FOLDER'

RouterType = FolderRouter

class Router:

	@staticmethod
	def not_set(key: str):
		return Exception(f'Please set a { key } in "{ config_file }"')

	@staticmethod
	def setup():
		if not r_type in settings:
			raise Router.not_set(r_type)
		if settings[r_type] == 'folder':
			if not r_folder in settings:
				raise Router.not_set(r_folder)
			return FolderRouter(settings[r_folder])