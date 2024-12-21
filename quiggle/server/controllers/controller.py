## local imports
from quiggle.server.controllers.connection import ConnectionLogger
from quiggle.server.handlers.request import Request
from quiggle.tools.logs.presets import errorlog
from quiggle.types.server import ClientAddressType, ClientSocketType

class HTTPServerController:
	def __init__(self, client_socket, client_address):
		self.request:                  Request = None
		self.response:                     any = None
		self.endpoint:                     any = None
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
		self.endpoint, response = router.find(self.request.path, self.request.method)
		self.response = response(self.client_socket, self.request)
		if self.endpoint == None:
			self.response.status_code = 404
			return
		if isinstance(self.endpoint, int):
			self.response.status_code = self.endpoint
			self.endpoint = None
		
	def use_endpoint(self):
		self.response.init_body(self.response.use_default_page())
		if self.endpoint != None:
			self.endpoint(self.request, self.response)

	''' Send final response over. '''
	def send(self):
		self.response.send()
		self.connection.log_response(self.response.status_code, self.response.STATUS_MESSAGES[self.response.status_code])