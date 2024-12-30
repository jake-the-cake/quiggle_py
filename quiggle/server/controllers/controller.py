## local imports
from quiggle.server.controllers.connection import ConnectionLogger
from quiggle.server.handlers.request import Request
from quiggle.server.handlers.response import Response
from quiggle.tools.logs.presets import errorlog
from quiggle.server.router.controller import RouteController

class HTTPServerController:
	def __init__(self, client_socket, client_address, router):
		self.connection: ConnectionLogger = ConnectionLogger(client_address[0], 10)
		self.request:             Request = self._handle_request(client_socket)
		self.response:           Response = Response(client_socket)
		self.endpoint:     callable | int = self._load_endpoint(router)
	
	''' Parse request data. '''
	def _handle_request(self, client_socket) -> None:
		try:
			data = client_socket.recv(1024).decode()
			if data:
				request = Request()
				request.load(data)
				self.connection.add_request_info(request.method, request.path)
				return request
			raise LookupError('Could not find request data.')
		except Exception as e:
			print(errorlog(f'Error handling request from { self.client_address[0] }:'), e)
	
	def _load_endpoint(self, router: RouteController) -> None:
		if router.find_route(self.request.path):
			endpoint = router.find_endpoint(self.request.method)
			if endpoint:
				return endpoint
			return 405
		return 404

	''' Execute the located method '''
	def _use_endpoint(self) -> None:
		self.endpoint(self.request, self.response)
	
	''' Triggers a default page for misc status codes or a route method to be executed. '''
	def end(self) -> None:
		if isinstance(self.endpoint, int):
			self.response.status_code = self.endpoint
			self.response.default(self.endpoint)
		else: 
			self._use_endpoint()
		self.connection.log_response(self.response.status_code, self.response.STATUS_MESSAGES[self.response.status_code])