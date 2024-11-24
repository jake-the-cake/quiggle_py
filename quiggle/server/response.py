## local imports
from .headers import Headers
from quiggle.tools.logs.presets import errorlog

# class DefaultPages:
	
# 	@staticmethod
# 	def _404():
# 		with open('/static/404.html') as file:
# 			return file.read()
		

class HTMLResponse(Headers):

	# DEFAULT_PAGES = {
		# 404: DefaultPages._404()
	# }

	def __init__(self, client_socket):
		super().__init__()
		self.client_socket = client_socket
		self.status_code   = 404
		self.body          = ''
		# Default headers
		self.set("Content-Type", "text/html")
		self.set("Connection", "close")


	def render_html():
		pass

	''' Sends the HTTP response. '''
	def send(self):
		try:
			# Get the status message
			status_message = Headers.get_status_message(self.status_code)
			self.set('Content-Length', len(self.body))
			# self.body = self.DEFAULT_PAGES[self.status_code]

			# Format headers
			header_str = self.format()

			# Construct the response
			response = (
					f'HTTP/1.1 {self.status_code} {status_message}\r\n'
					f'{header_str}\r\n\r\n'
					f'{self.body}'
			)
			self.client_socket.sendall(response.encode())
		except Exception as e:
			print(errorlog('Error sending response:'), e)