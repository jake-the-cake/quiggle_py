'''
	The Request class handles request parsing.
'''

# quiggle libraries
from ..core.utils.object import init_multiple_values
from .headers import Headers

# python libraries

class Request:

	def __init__(self, connection, address) -> None:
		self.connection = connection
		self.address = address
		init_multiple_values(self, [
			'method', 'path', 'query', 'body'
		], None)
		try:
			self.parse_request()
		except Exception as e:
			print('E: ' + str(e))
		print(vars(self))

	def parse_request(self):
		request = self.connection.recv(1024).decode()
		self.req_line, self.headers, self.body = Headers(request).get_values()

	def parse_req_line(self):
		return self.req_line.split(' ')

	def get_method(self):
		return self.method

	def get_version(self):
		return self.version
	
	def get_path(self):
		return self.path

	def get_query(self):
		return self.query

	def get_headers(self):
		return self.headers

	def get_body(self):
		return self.body