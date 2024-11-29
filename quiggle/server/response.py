## local imports
from .headers import Headers
from quiggle.tools.logs.presets import errorlog
from quiggle.config import globals
from quiggle.controller.render.injector import HTMLInjector

class HTMLResponse(Headers):

	def __init__(self, client_socket):
		super().__init__()
		self.client_socket = client_socket
		self.status_code   = 500
		self.body          = ''
		# Default headers
		self.set("Content-Type", "text/html")
		self.set("Connection", "close")

	''' Returns html from file. '''
	def use_default_page(self, code: int = 999) -> str:
		with open(globals.QUIGGLE_DIR + f'/static/{ code }.html') as file:
			return file.read().replace('\n', '').replace('\t', '')

	def render_html():
		pass

	''' Sends the HTTP response. '''
	def send(self):
		try:
			# Get the status message
			status_message = Headers.get_status_message(self.status_code)
			
			# temp injections
			self.status_code = 404
			self.body = self.use_default_page(self.status_code)

			# injector = HTMLInjector({
			# 	'status_code': 'y'
			# })

			# print(injector.inject(self.body))

			# inject content and variables
			injector = HTMLInjector({
				'status_code': 'y',
				# 'status_code': str(self.status_code),
				'status_message': 'n'
				# 'status_message': self.STATUS_MESSAGES[str(self.status_code)]
			})
			# print(self.body)
			self.body = injector.inject(self.body)
			# print(self.body)

			# Format headers
			self.set('Content-Length', len(self.body))
			header_str = self.format()

			# Construct the response
			response = (
					f'HTTP/1.1 {self.status_code} {status_message}\r\n'
					f'{header_str}\r\n\r\n'
					f'{self.body}'
			)
			print(response)
			self.client_socket.sendall(response.encode())
		except Exception as e:
			print(errorlog('Error sending response:'), e)