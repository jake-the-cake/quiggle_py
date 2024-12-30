## local imports
from quiggle.server.handlers.headers import Headers
from quiggle.tools.logs.presets import errorlog
from quiggle.config import globals
from quiggle.server.render.injector import HTMLInjector

class Response(Headers):

	def __init__(self, client_socket):
		super().__init__()
		self.client_socket    = client_socket
		self.status_code: int = 500
		self.body:       dict = { 'raw': '', 'final': '' }
		# Default headers
		self.set("Connection", "close")

	def default(self, status: int = None) -> None:
		if status != None: self.status_code = status
		self.init_body(self._use_default_page())
		self.send()

	''' Returns html from default status pages. '''
	def _use_default_page(self) -> str:
		# TODO: check if another default page is being used
		with open(globals.QUIGGLE_DIR + f'/static/status.html') as file:
			return file.read().replace('\n', '').replace('\t', '')

	def html(self, path: str, variables: dict = {}):
		self.send()

	def render_html():
		pass

	''' Set the body data for both raw and final '''
	def init_body(self, value: str) -> None:
		self.body['raw'] = value
		self.body['final'] = value


	''' Sends the HTTP response. '''
	def send(self):
		try:
			status_message = Headers.get_status_message(self.status_code)
			# self.init_body(self.use_default_page())

			# inject content and variables
			variables = {
				'status_code': str(self.status_code),
				'status_message': status_message
			}
			injector = HTMLInjector(variables)
			injector.inject(self.body)

			# Format headers
			self.set('Content-Length', len(self.body['final']))
			header_str = self.format()

			# Construct the response
			response = (
					f'HTTP/1.1 { self.status_code } { status_message }\r\n'
					f'{ header_str }\r\n\r\n'
					f'{ self.body['final'] }'
			)

			self.client_socket.sendall(response.encode())
		except Exception as e:
			print(errorlog('Error sending response:'), e)