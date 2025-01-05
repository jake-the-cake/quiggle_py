## local imports
from quiggle.server.controllers.connection import ConnectionLogger
from quiggle.server.handlers.request import Request
from quiggle.server.handlers.response import Response
from quiggle.tools.logs.presets import Printline
from quiggle.server.router.controller import RouteController

class HTTPServerController:
	def __init__(self, client_socket, client_address, router):
		self.connection: ConnectionLogger = ConnectionLogger(client_address[0], 10)
		self.request:             Request = self._handle_request(client_socket)
		self.response:           Response = Response(client_socket)
		self.response.endpoint            = self._load_endpoint(router)
	
	''' Parse request data. '''
	def _handle_request(self, client_socket) -> None:
		try:
			data = client_socket.recv(1024).decode()
			if data:
				request = Request(data)
				self.connection.add_request_info(request.method, request.path)
				return request
			raise LookupError('Could not find request data.')
		except Exception as e:
			Printline.error(f'Error handling request from { self.client_address[0] }:', e)
	
	def _load_endpoint(self, router: RouteController) -> None:
		self.response.protocol = self.request.accept()
		return router.find_route(self.request)

	''' Execute the located method '''
	def _use_endpoint(self) -> None:
		self.response.endpoint(self.request, self.response)
	
	''' Triggers a default page for misc status codes or a route method to be executed. '''
	def end(self) -> None:
		if isinstance(self.response.endpoint, int):
			self.response.status_code = self.response.endpoint
			self.response.default(self.response.endpoint)
		else: 
			self._use_endpoint()
		self.connection.log_response(self.response.status_code, self.response.STATUS_MESSAGES[self.response.status_code])