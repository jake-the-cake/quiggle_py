## local imports
from quiggle.config.read import read_local_file_variables
from quiggle.server.router.folder import FolderRouter
from quiggle.config.root import config_root

def not_set(key: str, filename: str):
    return Exception(f'Please set a { key } in "{ filename }"')

RouterType = FolderRouter

class RouteController:

    # get a list of variables from the config file
    config_file: str = config_root('globals')
    settings:   list = read_local_file_variables(config_file)

    # constant variables to find settings
    router_type = 'ROUTER_TYPE'
    route_folder = 'ROUTE_FOLDER'

    def __init__(self):
        self.router: RouterType = self.set_router_type()

    def set_router_type(self):
        if not self.router_type in self.settings:
            raise not_set(self.router_type, self.config_file)
        if self.settings[self.router_type] == 'folder':
            if not self.route_folder in self.settings:
                raise not_set(self.route_folder, self.config_file)
            return FolderRouter(self.settings[self.route_folder])