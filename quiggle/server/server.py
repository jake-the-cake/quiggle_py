## local imports
from quiggle.server import config
from quiggle.server.controllers.controller import HTTPServerController
from quiggle.server.controllers.socket import SocketController
from quiggle.server.prompts import MESSAGES
from quiggle.tools.printer import Printer, print_error, print_note
from quiggle.types.server import MiddlewareType, ClientAddressType, ClientSocketType
from quiggle.server.controllers.connection import ConnectionLogger
from quiggle.server.router.controller import RouteController

## global imports
import threading

class QuiggleServer:
	"""
	The QuiggleServer class manages the main server lifecycle, including starting,
	stopping, and handling client connections. It supports middleware and routing,
	and provides structured connection logging.
	"""

	def __init__(self, host: str = config.SERVER_HOST, port: int = config.SERVER_PORT, name: str = 'Server'):
		"""
		Initialize the server with host, port, and server name.

		:param host: Server host address (default from config).
		:param port: Server port (default from config).
		:param name: Name of the server for identification in logs.
		"""
		self.host: str = host
		self.port: int = port
		self.name: str = name
		self.connections: dict[ClientSocketType, ConnectionLogger] = {}
		self.middlewares: list[MiddlewareType] = []

		# Initialize controllers
		self.server_socket = SocketController(self.host, self.port)
		self.router = RouteController()

	def _log_server_start(self) -> None:
		"""
		Log server startup information.
		"""
		Printer(MESSAGES['connected'](self.host, self.port, self.name)).line('white_on_magenta')
		print_note('Listening for incoming connections...')

	def start(self) -> None:
		"""
		Start the server by initializing the socket and accepting connections.
		"""
		try:
			self.server_socket.start_socket()
			self._log_server_start()
			self._accept_connections()
		except Exception as e:
			print_error('Server Error', e)
			self._shutdown_message()

	def _accept_connections(self) -> None:
		"""
		Accept and handle incoming connections using threading.
		"""
		try:
			while True:
				client_socket, client_address = self.server_socket.accept_connections()
				threading.Thread(
					target=self._handle_connection,
					args=(client_socket, client_address),
					daemon=True
				).start()
		except KeyboardInterrupt:
			self._shutdown_message()
			self.stop()

	def _handle_connection(self, client_socket: ClientSocketType, client_address: ClientAddressType) -> None:
		"""
		Handle a single client connection.

		:param client_socket: The socket object for the client.
		:param client_address: The address of the connected client.
		"""
		if client_socket not in self.connections:
			# Log the new connection only once
			self.connections[client_socket] = ConnectionLogger(client_address[0], 8)

		try:
			while True:
				# Process the request with the HTTP controller
				controller = HTTPServerController(client_socket, self.router, self.connections[client_socket])

				# Apply middleware to the request/response cycle
				for middleware in self.middlewares:
					middleware(controller.request, controller.response)

				# Complete the response lifecycle
				controller.end()

		except Exception as e:
			print_error(f"Error handling connection from {client_address[0]}:{client_address[1]}", e)
		finally:
			# Ensure the socket is closed and remove it from active connections
			client_socket.close()
			del self.connections[client_socket]

	def use(self, middleware: MiddlewareType) -> None:
		"""
		Add middleware to the server. Middleware must be callable and takes (request, response).

		:param middleware: Middleware function to add.
		"""
		self.middlewares.append(middleware)
		print_note(f"Middleware added: {middleware.__name__}")

	def stop(self) -> None:
		"""
		Stop the server and close all active connections.
		"""
		if self.server_socket:
			self.server_socket.close_socket()
			self._shutdown_message()

	def _shutdown_message(self) -> None:
		"""
		Log a shutdown message for the server.
		"""
		print_note("Shutting down server...")