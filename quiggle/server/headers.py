class Headers:
	# Common HTTP status messages
	STATUS_MESSAGES = {
		200: "OK",
		201: "Created",
		204: "No Content",
		400: "Bad Request",
		401: "Unauthorized",
		403: "Forbidden",
		404: "Not Found",
		500: "Internal Server Error",
	}

	def __init__(self):
		self.headers = {}
			
	''' Sets a header key-value pair. '''
	def set(self, key: str, value: str):
		self.headers[key] = value

	''' Gets the value of a header key.'''
	def get(self, key: str) -> str:
		return self.headers.get(key, "")

	''' Removes a header. '''
	def remove(self, key: str):
		if key in self.headers:
			del self.headers[key]

	''' Formats headers as an HTTP-compatible string. '''
	def format(self) -> str:
		return "\r\n".join(f"{key}: {value}" for key, value in self.headers.items())

	''' Returns the status message for a given status code. '''
	@classmethod
	def get_status_message(cls, status_code: int) -> str:
		return cls.STATUS_MESSAGES.get(status_code, "Unknown Status")
