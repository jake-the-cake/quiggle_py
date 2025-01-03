class Headers:
	
	''' Common HTTP status messages. '''
	STATUS_MESSAGES = {
		200: "OK",
		201: "Created",
		204: "No Content",
		400: "Bad Request",
		401: "Unauthorized",
		403: "Forbidden",
		404: "Not Found",
		405: "Method Not Allowed",
		500: "Internal Server Error",
	}

	_joint = '\r\n'

	def __init__(self):
		self.headers = {}
		self.code(500)
			
	''' Sets a header key-value pair. '''
	def header(self, key: str, value: str = True) -> str:
		if value == False:
			return self.remove(key)
		if value != True:
			self.headers[key] = value
		return self.get(key)

	''' Gets the value of a header key. '''
	def get(self, key: str) -> str:
		return self.headers.get(key, "")

	''' Removes a header. '''
	def remove(self, key: str) -> None:
		if key in self.headers:
			del self.headers[key]

	''' Formats headers as an HTTP-compatible string. '''
	def format(self) -> str:
		return self._joint.join(f"{key}: {value}" for key, value in self.headers.items()) + self._joint
	
	def _get_status_message(self, code):
		if code in self.STATUS_MESSAGES.keys():
			return self.STATUS_MESSAGES[code]
		return 'Unknown Status'
	
	def _default_headers(self) -> None:
		self.header('Content-Type', self.protocol)
		self.header("Connection", "close")
		self.header('Content-Length', len(self.body))

	def code(self, code: int):
		try:
			code = int(code)
			self.status_code = code
			self.status_message = self._get_status_message(code)
			return self
		except:
			raise ValueError('Status code must be an integer.')