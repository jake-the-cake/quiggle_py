## local imports
from quiggle.server.controllers.connection import ConnectionLogger
from quiggle.server.handlers.request import Request
from quiggle.server.handlers.response import Response
from quiggle.tools.printer import print_error
from quiggle.server.router.controller import RouteController

class HTTPServerController:
	def __init__(self, client_socket, router, connection):
		self.connection: ConnectionLogger = connection
		self.request:             Request = self._handle_request(client_socket)
		self.response:           Response = Response(client_socket)
		self._load_endpoint(router)
	
	''' Parse request data. '''
	def _handle_request(self, client_socket) -> None:
		try:
			while True:
				data = client_socket.recv(1024).decode()
				if data:
					request = Request(data)
					# self.connection.add_request_info(request.method, request.path)
					return request
				raise LookupError('Could not find request data.')
		except Exception as e:
			print_error(f'Request { self.connection.id }', e)
	
	def _load_endpoint(self, router: RouteController) -> None:
		self.response.protocol = self.request.accept()
		self.response.endpoint = router.find_route(self.request)

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
		self.connection.respond(self.request, self.response)