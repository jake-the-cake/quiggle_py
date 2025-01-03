## local imports
from quiggle.server.handlers.headers import Headers
from quiggle.tools.logs.presets import Print, UseColor
from quiggle.config import globals
from quiggle.server.render.injector import HTMLInjector

## global imports
import json

class Response(Headers):

	DEFAULT_PAGE = globals.QUIGGLE_DIR + f'/static/status.html'
	
	@staticmethod
	def _trim_html(html: str) -> str:
		return html.replace('\n', '').replace('\t', '')

	def __init__(self, client_socket):
		super().__init__()
		self.client_socket            = client_socket
		self.body:                str = ''
		self.protocol:            str = None
		self.endpoint: callable | int = None

	def _inject(self, html: str, variables: dict = {}):
		injector = HTMLInjector(html, variables)
		self.body = injector.inject()

	def html(self, html: str, variables: dict = {}):
		self.protocol = 'text/html'
		self._inject(html, variables)
		self.send()

	def default(self, code: int = None) -> None:
		if code != None: self.code(code)
		variables = self._default_variables()
		if 'html' in self.protocol:
			# TODO: check if another default page is being used
			self.html(self._use_default_page(), variables)
		else: self.json(variables)

	''' Returns html from default quiggle status pages. '''
	def _use_default_page(self) -> str:
		with open(self.DEFAULT_PAGE) as file:
			return Response._trim_html(file.read())
	
	def _default_variables(self) -> dict:
		return { 'status_code': str(self.status_code),
				'status_message': self.status_message }

	def render(self, path: str, variables: dict = {}) -> None:
		html = ''
		self.html(html, variables)

	def json(self, data: dict) -> None:
		self.protocol = 'application/json'
		self.body = json.dumps(data)
		self.send()

	def _get_status_line(self) -> str:
		return f'HTTP/1.1 { self.status_code } { self.status_message }'
	
	def _build_response(self) -> str:
		self._default_headers()
		return self._joint.join([self._get_status_line(), self.format(), self.body])

	''' Sends the HTTP response. '''
	def send(self):
		try:
			response = self._build_response()
			self.client_socket.sendall(response.encode())
		except Exception as e:
			Print.error('Error sending response', e)