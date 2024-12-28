## local imports
from quiggle.server.controllers.connection import ConnectionLogger
from quiggle.server.handlers.request import Request
from quiggle.server.handlers.response import Response
from quiggle.tools.logs.presets import errorlog
from quiggle.types.server import ClientAddressType, ClientSocketType
from quiggle.server.router import RouterType
from quiggle.server.router.controller import RouteController

class HTTPServerController:
	def __init__(self, client_socket, client_address):
		self.client_socket:   ClientSocketType = client_socket
		self.client_address: ClientAddressType = client_address
		# self.request:                  Request = Request()
		self.request:                  Request = self._handle_request(client_socket)
		# self.response:                Response = Response(self.client_socket)
		self.response:                Response = Response(client_socket)
		self.connection:      ConnectionLogger = ConnectionLogger(client_address[0], 10)
		
		self.endpoint:                     any = None

	# def setup(self, router: RouteController) -> None:
	# 	self._handle_request()
	# 	self.response.endpoint = self._load_endpoint(router)

	
	def end(self) -> None:
		if isinstance(self.response.endpoint, int):
			self.response.status_code = self.response.endpoint
		self.response.init_body(self.response.use_default_page())


	def load_endpoint(self, router: RouteController) -> None:
		if router.find_route('/'):
			endpoint = router.find_endpoint(self.request.method)
			if endpoint:
				return endpoint
			return 405
		return 404
		# router.find('/', 'get')

	''' Parse request data. '''
	def _handle_request(self, client_socket) -> None:
		try:
			data = client_socket.recv(1024).decode()
			print(data)
			if data:
				request = Request().load(data)
				# self.request.load(data)
				print(request.__dict__)
				self.connection.add_request_info(self.request.method, self.request.path)
				return request
		except Exception as e:
			print(errorlog(f'Error handling request from { self.client_address[0] }:'), e)

	''' Looks up the route. '''
	def handle_routing(self, router):
		router.set_response_type(self.request.accept())
		router.find(self.request.path, self.request.method)
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