## local imports
from quiggle.config.read import read_local_file_variables
from quiggle.config.root import config_root

class RouteController:

    # get a list of variables from the config file
    config_file: str = config_root('globals')
    settings:   list = read_local_file_variables(config_file)

    # constant variables to find settings
    router_type = 'ROUTER_TYPE'
    route_folder = 'ROUTE_FOLDER'

    def __init__(self):
        self.router = None

