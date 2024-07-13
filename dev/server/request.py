'''
	The Request class handles request parsing.
'''

# quiggle libraries
from ..core.utils.object import init_multiple_values

# python libraries
from urllib.parse import urlparse, parse_qs

class Request:
	def __init__(self, connection, address) -> None:
		self.connection = connection
		self.address = address
		self.headers = {}
		init_multiple_values(self, [
			'method', 'path', 'query', 'body'
		], None)
		print(vars(self))
		try:
			self.parse_request()
		except Exception as e:
			print('E: ' + str(e))

	def parse_request(self):
		request = self.connection.recv(1024).decode()
		print(request)
		print(self.connection)
		# lines = request.split('\r\n')
		# # Parse the request line
		# request_line = lines[0].split(' ')
		# # print(request_line)
		# self.method = request_line[0]
		# parsed_url = urlparse(request_line[1])
		# self.path = parsed_url.path
		# self.query = parse_qs(parsed_url.query)
		
		# # Parse the headers
		# i = 1
		# while lines[i] != '':
		# 	header_line = lines[i].split(': ', 1)
		# 	self.headers[header_line[0]] = header_line[1]
		# 	i += 1
		
		# # Parse the body if there is one
		# print(len(lines))
		# self.body = '\r\n'.join(lines[i+1:])

	def get_method(self):
		return self.method

	def get_path(self):
		return self.path

	def get_query(self):
		return self.query

	def get_headers(self):
		return self.headers

	def get_body(self):
		return self.body