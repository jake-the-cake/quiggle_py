if __name__ == '__main__':
	from server.web_server import Web_Server
	app = Web_Server()
else:
	from .server.web_server import Web_Server