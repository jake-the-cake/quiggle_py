## local imports
from quiggle.server.controllers.connection import ConnectionLogger
from quiggle.server.handlers.request import Request
from quiggle.server.handlers.response import HTMLResponse
from quiggle.server.router.controller import RouteController
from quiggle.tools.logs.presets import errorlog
from quiggle.types.server import ClientAddressType, ClientSocketType

class HTTPServerController:
	def __init__(self, client_socket, client_address):
		self.request:                  Request = None
		self.response:            HTMLResponse = None
		self.client_socket:   ClientSocketType = client_socket
		self.client_address: ClientAddressType = client_address
		self.connection:      ConnectionLogger = ConnectionLogger(client_address[0], 10)

	''' Parse request data. '''
	def handle_request(self):
		try:
			data = self.client_socket.recv(1024).decode()
			if data:
				self.request = Request(data)
				self.connection.log_request(self.request.method, self.request.path)
		except Exception as e:
			print(errorlog(f'Error handling request from { self.client_address[0] }:'), e)

	''' Looks up the route. '''
	def handle_routing(self, router):
		router.find_route(self.request, self.response)

	''' Generate an http response. '''
	def choose_protocol(self) -> None:
		split_path = self.request.path.split('/')
		if split_path[0] == 'api':
			self.protocol = 'api'
			# TODO: API protocol
			self.response = None
		else:
			self.protocol = 'html'
			self.response = HTMLResponse(self.client_socket, self.request)

	''' Send final response over. '''
	def send(self):
		self.response.send()
		self.connection.log_response(self.response.status_code, self.response.STATUS_MESSAGES[self.response.status_code])