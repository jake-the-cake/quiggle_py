## local imports
from quiggle.server import server

if __name__ == '__main__':
	app = server.QuiggleServer(name = 'My Server', port = 6047)
	app.start()