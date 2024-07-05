# quiggle libraries
from ..config import settings
from ..core.load import load_settings
from ..routing.router import Web_Router
from ..routing.paths import split_path

# python libraries
import os, subprocess, json
from socket import (
	socket,
	AF_INET,
	SOCK_STREAM,
	error as socket_error,
	timeout as socket_timeout
)
from typing import Tuple




#types
from typing import Literal, Optional
Server_Type = Literal['web', 'data', 'auth', 'media', 'admin']
True_Or_None_Type = Optional[True]





#null check
def if_has_value(check_value: any, default_value: any):
	if check_value: return check_value
	return default_value


#
#
#


class Server_Connection:
	def __init__(self, type: Server_Type = 'web', port: int | None = None) -> None:
		self.port = if_has_value(port, Server_Connection.default_ports[type])
		self.host = '127.0.0.1'
		if not self.create_socket(): return print('Could Not Connect')
		self.settings = load_settings('application')
		self.listen(self.socket)

	def listen(self, server_socket = None):
		if not server_socket: server_socket = self.new_socket()
		server_socket.listen(1)
		print('connected on port ' + str(self.port))
		self.continue_to_listen(server_socket)

	def new_socket(self):
		self.socket = socket(AF_INET, SOCK_STREAM)

	def close_socket(self):
		self.socket.close()

	def create_socket(self) -> True_Or_None_Type:
		self.new_socket()
		if not self.check_port():
			if not self.retry_connection(3): return None
		self.bind_socket()
		return True

	def bind_socket(self):
		self.new_socket()
		try:
			self.socket.bind((self.host, self.port))
		except socket_error as e:
			print(e, 'bind_socket')
			self.close_socket()
			return True

	def check_port(self) -> True_Or_None_Type:
		self.new_socket()
		try:
			self.socket.bind((self.host, self.port))
		except (socket_timeout, socket_error):
			print(socket_error, 'check_port')
			return None
		finally:
			self.close_socket()
		return True
	
	def retry_connection(self, attempts: int = 3) -> True_Or_None_Type:
		print(attempts)
		if attempts < 1: return None
		pid = self.find_process_on_port()
		if not pid: return True
		self.kill_process_on_port(pid)
		return self.retry_connection(attempts - 1)
		
	def find_process_on_port(self):
		try:
			result = subprocess.run(['lsof', '-i', ':' + str(self.port)], capture_output = True, text = True)
			for line in result.stdout.splitlines():
				if 'LISTEN' in line:
					parts = line.split()
					return parts[1]
		except Exception as e:
			print(f"Error finding process using port {self.port}: {e}")
		return None
	
	def kill_process_on_port(self, pid):
		if not pid: return
		try:
			print('Process ' + pid + ' @ ' + self.host + ':' + str(self.port) + ' has been ended.')
			os.kill(int(pid), 9)
		except Exception as e:
			print(e, 'kill_process_on_port')

	default_ports = {
		'web': settings.WEB_PORT,
		'data': settings.DATA_PORT,
		'auth': settings.AUTH_PORT,
		'media': 1000,
		'admin': 1001
	}



#
#
#



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

					###
					request = client_socket.recv(1024)
					method, path, version = self.parse_http_req(request.decode())
					###
					
					response = {
						'version': version,
						'method': method,
						'path': path
					}

					response['route'], response['protocol'], response['content-type'], is_found = self.search_for_route(*self.get_protocol(path))
					if is_found == True:
						response['data'] = self.get_data()[response['protocol']][method](request.decode())
						response['status'] = self.use_response_status(200)
						# with open(response['route'], 'r') as file:
						# 	response['data'] = file.read()
					else:
						response['status'] = self.use_response_status(404)
						response['message'] = 'Error 404: Requested Address Was Not Found'
					client_socket.send(self.build_response(response))
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
			# 'idk': self.get_api_data(),
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

	def get_protocol(self, route: str) -> Tuple[str, str]:
		split_value = split_path(route)
		if split_value[0] == 'api': protocol = 'api'
		elif split_value[0] == 'idk': protocol = 'idk'
		else: protocol = 'web'
		return route, protocol
		
	def use_router(self):
		self.router = Web_Router('application/main')
		self.routes = self.router.routes

	def search_for_route(self, route: str, protocol: str):
		if protocol == 'api': content_type = 'application/json'
		else: content_type = 'text/html'
		if self.routes[protocol].get(route) is not None:
			return self.routes[protocol][route], protocol, content_type, True
		else: return None, None, None, None

	def build_response(self, response):
		if response['status']['label'] == 'OK':
			output = response['data']
		else:
			output = json.dumps({'error': response['message']})
		return 'HTTP/1.1 {} {}\r\nContent-Type: {}\r\nContent-Length: {}\r\n\r\n{}'.format(
			response['status']['code'],
			response['status']['label'],
			response['content-type'],
			len(output),
			output
		).encode('utf-8')

	def parse_http_req(self, req):
		lines = req.split('\r\n')
		for l in lines: print(l)
		req_line = lines[0]
		method, path, version = req_line.split(' ')
		return method, path, version