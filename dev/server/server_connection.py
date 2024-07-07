# quiggle libraries
from ..config import settings
from ..core.load import load_settings

# python libraries
import os, subprocess, json
from socket import (
	socket,
	AF_INET,
	SOCK_STREAM,
	SOL_SOCKET,
	SO_REUSEADDR,
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
			self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
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