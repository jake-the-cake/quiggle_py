## local imports
from quiggle.server import config
from quiggle.server.controllers.controller import HTTPServerController
from quiggle.server.controllers.socket import SocketController
from quiggle.server.prompts import MESSAGES
from quiggle.tools.printer import Printer, print_error
from quiggle.types.server import MiddlewareListType, MiddlewareType, ClientAddressType, ClientSocketType
from quiggle.server.router.controller import RouteController

## global imports
import threading

class QuiggleServer:

	def __init__(self, host: str = config.SERVER_HOST, port: int = config.SERVER_PORT, name: str = 'Server'):
		# server variables
		self.host: str = host
		self.port: int = port
		self.name: str = name
		# middlewares
		self.middlewares: MiddlewareListType = []
		# objects
		self.server_socket: SocketController = SocketController(self.host, self.port)
		self.router:         RouteController = RouteController()

	def _print_connected(self) -> None:
		Printer(MESSAGES['connected'](self.host, self.port, self.name)).line('white_on_magenta')
		Printer('Listening...').line('note')

	''' Start the socket server and pass to accept connections. '''
	def start(self) -> None:
		try:
			self.server_socket.start_socket()
			self._print_connected()
			self._accept_connections()
		except Exception as e:
			print_error('Server', e)
			print(e)

	''' Accept and handle incoming connections. '''
	def _accept_connections(self):
		try:
			while True:
				threading.Thread(
					target=self._handle_connection,
					args=(self.server_socket.accept_connections())
				).start()
		except KeyboardInterrupt:
			print("Shutting down server...")
			self.stop()

	''' Handles a single connection. '''
	def _handle_connection(self, client_socket: ClientSocketType, client_address: ClientAddressType):
		try:
			controller: HTTPServerController = HTTPServerController(client_socket, client_address, self.router)
			for middleware in self.middlewares:
				middleware(controller.request, controller.response)
			controller.end()
		except Exception as e:
			Printer(f'Error handling connection from { client_address[0] }:', e).line('error')
			raise e
		finally:
			client_socket.close()

	''' Allows the user to bind middleware to the server. '''
	''' Middleware is a callable that takes (request, response). '''
	def use(self, middleware: MiddlewareType):
		self.middlewares.append(middleware)
		print(f"Middleware added: {middleware.__name__}")

	''' Stops the server and closes the socket. '''
	def stop(self):
		if self.server_socket:
			self.server_socket.close_socket()