# from core.dev import incomplete_function
from server.response import Response
import socket

#
#
#
#
#

from config.settings import DEV_MODE, BETA_PORT, DIST_PORT, BETA_HOST, DIST_HOST

class Server:
	def __init__(self):
		self.port: int = Server.get_port()
		self.host: str = Server.get_host()
		self.status: str = 'disconnected'
		self.connection = None
		try:
			self.connection = self.connect()
			self.status = 'connected'
		except Exception as e:
			print(e)

	@staticmethod
	def get_port():
		if DEV_MODE == False: return DIST_PORT
		return BETA_PORT
	
	@staticmethod
	def get_host():
		if DEV_MODE == False: return DIST_HOST
		return BETA_HOST

	def check_port_number(self):
		pass

	def connect(self):
		self.socket = self.create_socket()
		print(self.socket)
		return 'Hi'
	
	def create_socket(self) -> socket:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		return s


#
#
#
#
#
#

def handle_request(request):
	headers = request.split('\r\n')
	method, path, _ = headers[0].split()

	if path == '/json':
		response_body = Response('').json
		content_type = 'application/json'
	else:
		response_body = Response('').html
		content_type = 'text/html'

	response = f'HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\nContent-Length: {len(response_body)}\r\n\r\n{response_body}'
	return response

def start_server(host='localhost', port=3000):
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
		server_socket.bind((host, port))
		server_socket.listen(5)
		print(f'Serving on port {port}...')

		while True:
			client_socket, addr = server_socket.accept()
			with client_socket:
				request = client_socket.recv(1024).decode()
				response = handle_request(request)
				client_socket.sendall(response.encode())

