## local imports
from quiggle.config.root import get_config
from quiggle.server.router import not_set, RouterType
# from quiggle.server.router import RouterType

class RouteController:

    # get a list of variables from the config file
    settings: list = get_config('server')

    # constant variables to find settings
    router_type = 'ROUTER_TYPE'
    route_folder = 'ROUTE_FOLDER'

    def __init__(self):
        self.router: RouterType = self._set_router_type()

    def _set_router_type(self):
        if not self.router_type in self.settings:
            raise not_set(self.router_type, self.settings['filename'])
        if self.settings[self.router_type] == 'folder':
            if not self.route_folder in self.settings:
                raise not_set(self.route_folder, self.settings['filename'])
            from quiggle.server.router.folder import FolderRouter
            return FolderRouter(self.settings)

    def find(self, request, response) -> None:
        path = self.router.find_route(request.path)
        print(path)