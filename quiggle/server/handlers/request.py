## local imports
from quiggle.tools.printer import Printer
from quiggle.server.prompts import MESSAGES

class Request:

	_joint = '\r\n'

	def __init__(self, data: str = None):
		self.path:     str = None
		self.method:   str = None
		self.body:     str = None
		self.args:    dict = {}
		self.headers: dict = {}
		try:
			self._parse_request(data)
		except Exception as e:
			Printer(MESSAGES['notparsed']('Request'), e).error()
			raise Exception(e)

	'''
	[accept]
		Return the "Accept" header, or "application/json" by default.
		(args): 
		... return string '''
	def accept(self):
		if 'Accept' in self.headers: return self.headers['Accept']
		return 'application/json'

	def _split_data(self, data: str) -> list:
		return data.split(self._joint)
	
	''' Parses HTTP headers from the request data. '''
	def _parse_headers(self, header_lines) -> None:
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
		lines = self._split_data(raw_data)
		self.method, self.path, _ = lines[0].split()
		self._parse_headers(lines[1:])
		self._parse_body(lines.index("") + 1, lines)
		# TODO: Extract token from Authorization header (if present)
			# auth_header = self.headers.get("Authorization", "")
			# if auth_header.startswith("Bearer "):
			# 	self.token = auth_header.split(" ")[1]