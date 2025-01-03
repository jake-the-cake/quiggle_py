## local imports
from quiggle.tools.logs.presets import errorlog

class Request:

	_joint = '\r\n'

	def __init__(self, data: str = ''):
		# Initialize request variables
		self.path:     str = None
		self.method:   str = None
		self.body:     str = None
		self.headers: dict = {}
		self._parse_request(data)

	# def load(self, data: str):
	# 	self._parse_request(data)

	'''	[accept]
	
		Return the "Accept" header, or "application/json" by default.
		# args: None
		# return: string '''
	def accept(self):
		if 'Accept' in self.headers: return self.headers['Accept']
		return 'application/json'

	def _split_data(self, data: str) -> list:
		return data.split(self._joint)
	
	''' Parses HTTP headers from the request data. '''
	def _parse_headers(self, header_lines) -> None:
		# Loop through each header line and extract key-value pairs
		for line in header_lines:
			if line == "": break
			key, value = line.split(":", 1)
			self.headers[key.strip()] = value.strip()

	''' Extracts the body of the request if present. '''
	def _parse_body(self, body_index: int, lines: list) -> None:
		if body_index < len(lines):
			self.body = self._joint.join(lines[body_index:])

	''' Parses the raw HTTP request data and populates attributes. '''
	def _parse_request(self, raw_data: str):
		try:
			# Split raw data into lines
			lines = self._split_data(raw_data)
			
			# Parse the request line (e.g., "GET /index.html HTTP/1.1")
			self.method, self.path, _ = lines[0].split()
			
			# Parse headers and body
			self._parse_headers(lines[1:])
			self._parse_body(lines.index("") + 1, lines)

			# TODO: Extract token from Authorization header (if present)
				# auth_header = self.headers.get("Authorization", "")
				# if auth_header.startswith("Bearer "):
				# 	self.token = auth_header.split(" ")[1]

		except Exception as e:
			print(errorlog('Error parsing request:', e))