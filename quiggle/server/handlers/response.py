## local imports
from quiggle.server.handlers.headers import Headers
from quiggle.tools.logs.presets import errorlog
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
		self.client_socket = client_socket
		self.body:     str = ''
		self.header("Connection", "close")

	def _inject(self, html: str, variables: dict = {}):
		injector = HTMLInjector(html, variables)
		self.body = injector.inject()

	def html(self, html: str, variables: dict = {}):
		self.header('Content-Type', 'text/html')
		self._inject(html, variables)
		self.send()

	def default(self, code: int = None) -> None:
		if code == None: code = self.status_code
		self.code(code)
		# TODO: check if another default page is being used
		self.html(self._use_default_page(), {
			'status_code': str(self.status_code),
			'status_message': self.status_message })

	''' Returns html from default quiggle status pages. '''
	def _use_default_page(self) -> str:
		with open(self.DEFAULT_PAGE) as file:
			return Response._trim_html(file.read())
		
	def render(self, path: str, variables: dict = {}) -> None:
		html = ''
		self.html(html, variables)

	def json(self, data: dict) -> None:
		self.header('Content-Type', 'application/json')
		self.body = json.dumps(data)
		self.send()

	''' Sends the HTTP response. '''
	def send(self):
		try:
			self.header('Content-Length', len(self.body))
			status_line = f'HTTP/1.1 { self.status_code } { self.status_message }'
			response = self._joint.join([status_line, self.format(), self.body])
			self.client_socket.sendall(response.encode())
		except Exception as e:
			print(errorlog('Error sending response:'), e)