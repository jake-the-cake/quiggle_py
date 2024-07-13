'''
	The Web_Server class is an extension of Server_Connection, and handles incoming http requests.
'''

# quiggle libraries
from ..routing.router import Web_Router
from .server_connection import Server_Connection
from .response import Response
from .request import Request

# python libraries
import json
from socket import	error as socket_error

# Web_Server class
class Web_Server(Server_Connection):
	def __init__(self):
		super().__init__('web')
	
	http_status = {
		'200': 'OK',
		'404': 'NOT FOUND'
	}

	def continue_to_listen(self, server_socket):
		if self.settings['USE_AUTO_ROUTER'] == True:
			self.use_router()
		try:
			while True:
				client_socket, client_address = server_socket.accept()
				print(f"Connection from {client_address}")
				with client_socket:
					# request = client_socket.recv(1024)
					req = Request(client_socket, client_address)
					
					response = Response(req, self.router)
					# print(vars(response))

					# if is_found == True:
					# 	response['data'] = self.get_data()[response['protocol']][method](request.decode())
					# 	response['status'] = self.use_response_status(200)
					# 	# with open(response['route'], 'r') as file:
					# 	# 	response['data'] = file.read()
					# else:
					# 	response['status'] = self.use_response_status(404)
					# 	response['message'] = 'Error 404: Requested Address Was Not Found'
					client_socket.send(response.x)
					# client_socket.send(response.response.encode())
		except (KeyboardInterrupt, socket_error) as e:
			print('\nServer Disconnection: [{}]'.format(e))
			self.kill_process_on_port(self.find_process_on_port())
			self.close_socket()
	
	def use_response_status(self, code: int):
		return {
			'code': code,
			'label': self.http_status[str(code)]
		}

	def get_data(self):
		return {
			'api': self.get_api_data(),
			'web': self.get_web_data()
		}
	
	def get_web_data(self):
		def GET(request):
			return '<p>Paragraph</p>'
		
		return {
			'GET': GET
		}

	def get_api_data(self):
		def GET(request):
			return json.dumps({'data': 'info'})

		return {
			'GET': GET
		}
		
	def use_router(self):
		self.router = Web_Router('application/main')
		self.routes = self.router.routes