'''
	The Response class handles how the server handles the request.
'''

# quiggle libraries
from ..routing.paths import split_path
from ..core.utils.array import Array

# python libraries
from typing import Tuple

class Response:
	def __init__(self, request, router) -> None:
		if not request:
			return {'error': 'Error'}
		self.request = request
		self.router = router
		if not Array.all_values_equal([
			self.read_headers(),
			self.get_protocol(),
			self.get_filename(),
			self.get_route(),
			self.set_response_headers(),
			self.set_response(),
		], True): raise self.caught_error
		print(vars(self))
		self.x = b'HTTP/1.1 200 OK\r\nContent-Length: 1\r\n\r\nA'
	
	response_code = {
		'200': 'OK',
		'404': 'NOT FOUND'
	}

	def get_filename(self):
		try:
			filename = Array.get_last(split_path(self.path))
			if len(filename.split('.')) < 2:
				self.filename = None
			else:
				self.filename = filename
				self.path = '/' + '/'.join(Array.cut_last(split_path(self.path)))
			return True
		except Exception as e:
			self.caught_error = e
			return False 
		
	def set_response_headers(self):
		try:
			self.response_header = '\r\n'.join([
				' '.join([
					self.version,
					str(self.status['code']),
					self.status['label'],
				]),
				'Content-Type: ' + self.content_type,
				'Content-Length: '
			])
			return True
		except Exception as e:
			self.caught_error = e
			return False
	
	def set_status(self, code):
		self.status = {
			'code': code,
			'label': self.response_code[str(code)]
		}

	def set_response(self):
		self.content = '<p>Hello!</p>'
		try:
			self.response = self.response_header + str(len(self.content)) + '\r\n\r\n' + self.content
			return True
		except Exception as e:
			self.caught_error = e
			return False

	def get_route(self):
		try:
			self.route = self.router.routes[self.protocol].get(self.path)
			self.set_status(200)
			return True
		except Exception as e:
			self.set_status(404)
			self.caught_error = e
			return False

	def get_protocol(self) -> bool:
		protocol = Array.get_first(split_path(self.path))
		if protocol == 'api':
			self.protocol = 'api'
			self.content_type = 'application/json'
		else:
			self.protocol = 'web'
			self.content_type = 'text/html'
		if not self.protocol: 
			self.caught_error = Exception('Sysyem Error Has Occurred @ {}'.format('get_protocol'))
			return False
		return True

	def read_headers(self) -> bool:
		try:
			self.method, self.path, self.version = self.request.parse_req_line()
			print(self.path)
			return True
		except Exception as e:
			self.caught_error = e
			print(e)
			return False