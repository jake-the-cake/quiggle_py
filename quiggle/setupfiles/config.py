'''
GLOBAL Settings:
	>> VERSION_NUMBER: current project version
    >> USE_ADMIN: set True to use built-in GUI admin
'''
USE_ADMIN = True
VERSION_NUMBER = '0.0.1'

'''
SERVER Settings:
	>> ROUTER_TYPE: choose 'folder' or 'custom' (not available) router setting
	>> ROUTE_FOLDER: set root directory for folder router
    >> API_ROUTE_PREFIX: the path prefix for looking up api routes
'''
ROUTER_TYPE = 'folder'
ROUTE_FOLDER = '/routes'
API_ROUTE_PREFIX = 'api'

'''
DATABASE Settings:
	>> DB_SERVICE: the database service being used
'''
DB_SERVICE = 'mongo'
