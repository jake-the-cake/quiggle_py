## local imports
from .controller import HTTPServerController
from .socket import SocketController
from .prompts import MESSAGES
from quiggle.config import globals
from quiggle.tools.logs.presets import errorlog

## global imports
import socket
import threading
from typing import Callable, List, Tuple

MiddlewareType = Callable[[socket.socket, Tuple[str, int]], None]
MiddlewareListType = List[MiddlewareType]

class QuiggleServer:

	def __init__(self, host: str = globals.SERVER_HOST, port: int = globals.SERVER_PORT, name: str = None):
		self.host: str = host
		self.port: int = port
		self.name: str = name
		self.middlewares: MiddlewareListType = []
		self.server_socket: SocketController = SocketController(self.host, self.port)

	''' Start the socket server and pass to accept connections. '''
	def start(self) -> None:
		self.server_socket.start_socket()
		print(MESSAGES['connected'](self.host, self.port, self.name))
		self._accept_connections()

	''' Accept and handle incoming connections. '''
	def _accept_connections(self):
		try:
			while True:
				client_socket, client_address = self.server_socket.accept_connections()
				threading.Thread(
					target=self._handle_connection, args=(client_socket, client_address)
				).start()
		except KeyboardInterrupt:
			print("Shutting down server...")
			self.stop()

	''' Handles a single connection. '''
	def _handle_connection(self, client_socket: socket.socket, client_address: Tuple[str, int]):
		controller: HTTPServerController = HTTPServerController()
		try:
			controller.handle_request(client_socket, client_address)
			
			# -> TODO: Route
			# -> TODO: Determine API vs HTML
			
			controller.generate_response()

			# -> TODO: MIDDLEWARE: need to impliment
			
			for middleware in self.middlewares:
				middleware(controller.request, controller.response)
			controller.send()
		except Exception as e:
			print(errorlog(f'Error handling connection from { client_address[0] }:'), e)
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