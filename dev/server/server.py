# quiggle libraries
from config import settings
from core.load import load_settings
from routing.router import Web_Router

# python libraries
import os, subprocess
from socket import (
	socket,
	AF_INET,
	SOCK_STREAM,
	error as socket_error,
	timeout as socket_timeout
)




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
			print(e, 'killed')

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
	def continue_to_listen(self, server_socket):
		if self.settings['USE_AUTO_ROUTER'] == True:
			self.use_router()
		try:
			while True:
				client_socket, client_address = server_socket.accept()
				print(f"Connection from {client_address}")
				with client_socket:
					request = client_socket.recv(1024)
					method, path = self.parse_http_req(request.decode())
					response = self.search_for_route(path)
					print(response)
					if response['status'] == 'OK':
						output = response['data']
					else:
						output = response['message']

					client_socket.send(self.build_response(response, output))
		except KeyboardInterrupt:
			print('\nServer disconnected...')
			self.kill_process_on_port(self.find_process_on_port())
			self.close_socket()
		
	def use_router(self):
		self.router = Web_Router('application/main')
		self.routes = self.router.routes

	def search_for_route(self, route: str):
		data = None
		split_path = route.split('/')
		if split_path[0] == '': split_path = split_path[1:]
		protocol = 'web'
		if split_path[0] == 'api': protocol = 'api'
		if self.routes[protocol].get(route) is not None:
			file_path = self.router.base_path + route + '/page.html'
			with open(file_path, 'r') as file:
				data = file.read()
		if data: return {
			'status_code': 200,
			'status': 'OK',
			'data': data
		}
		else: return {
			'status_code': 404,
			'status': 'fail',
			'message': 'Not Found!!.'
		}

	def build_response(self, response, html):
		status = {
			'code': response['status_code'],
			'value': response['status']
		}
		return 'HTTP/1.1 {} {}\r\nContent-Length: {}\r\n\r\n{}'.format(status['code'], status['value'], len(html), html).encode('utf-8')

	# def receive_request(self):
		# print(x)
		# print(self)

	def parse_http_req(self, req):
		# print(req)
		lines = req.split('\r\n')
		for l in lines: print(l)
		req_line = lines[0]
		method, path, _ = req_line.split(' ')
		return method, path