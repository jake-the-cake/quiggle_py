## local imports
from quiggle.tools.logs.presets import errorlog

class Request:

	'''
		This class parses raw HTTP request data and extracts key components such as headers, HTTP method, request path, and the request body. It also provides functionality for handling authentication tokens, if included in the headers.
	'''

	def __init__(self):

		# Initialize request variables
		self.path:     str = None
		self.method:   str = None
		self.body:     str = None
		self.headers: dict = {}

	def load(self, data: str) -> None:
		self._parse_request(data)

	''' Parses HTTP headers from the request data. '''
	def _parse_headers(self, header_lines) -> None:
		# Loop through each header line and extract key-value pairs
		for line in header_lines:
			if line == "":
				break
			key, value = line.split(":", 1)
			self.headers[key.strip()] = value.strip()

	''' Extracts the body of the request if present. '''
	def _parse_body(self, body_index: int, lines: list) -> None:
		if body_index < len(lines):
			self.body = "\r\n".join(lines[body_index:])

	''' Parses the raw HTTP request data and populates attributes. '''
	def _parse_request(self, raw_data: str):
		try:
			# Split raw data into lines
			lines = raw_data.split("\r\n")
			
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