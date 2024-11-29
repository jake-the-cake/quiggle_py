## local imports
from quiggle.config import globals
from quiggle.tools.logs.presets import errorlog
from .prompts import MESSAGES

## global imports
import socket
from typing import Tuple

sock_addr_type = Tuple[socket.socket, Tuple[str, int]]

class SocketController:

	'''
		The SocketController class is responsible for managing and controlling socket-based 
		communication for the QuiggleServer. It serves as the foundational component for 
		handling both HTTP requests and WebSocket connections.
	'''

	def __init__(self, host: str = globals.SERVER_HOST, port: int = globals.SERVER_PORT):
		self.host: str     = host
		self.port: int     = port
		self.server_socket = None

	''' Create a new socket instance '''
	def create_socket(self) -> None:
		self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	''' Start listening on specified port '''
	def start_socket(self) -> None:
			self.create_socket()
			self.server_socket.bind((self.host, self.port))
			self.server_socket.listen(5)

	''' Accept incoming connections and return data '''
	def accept_connections(self) -> None | sock_addr_type:
		while True:
			try:
				client_socket, client_address = self.server_socket.accept()
				return client_socket, client_address
			except Exception as e:
				print(errorlog(f'Error accepting connections:'), e)

	''' Start listening on specified port '''
	def close_socket(self) -> None:
		if self.server_socket:
			self.server_socket.close()
			print(MESSAGES['closed'](self.__class__.__name__))