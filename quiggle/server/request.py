## local imports
from quiggle.tools.logs.presets import errorlog

class Request:

	def __init__(self, raw_data: str):
		
		# init vars
		self.method: str | None = None
		self.path: str | None   = None
		self.token: str | None  = None
		self.body: str | None   = None
		
		# parse request to fill headers
		self.headers = {}
		self._parse_request(raw_data)

	''' Parses raw HTTP request data. '''
	def _parse_request(self, raw_data: str):
		try:
			lines = raw_data.split("\r\n")
		
			# Parse the request line (e.g., GET / HTTP/1.1)
			request_line = lines[0].split()
			self.method, self.path, _ = request_line

			# Parse headers
			header_lines = lines[1:]
			for line in header_lines:
				if line == "":  # End of headers
					break
				key, value = line.split(":", 1)
				self.headers[key.strip()] = value.strip()

			# Extract body if present
			body_index = lines.index("") + 1
			if body_index < len(lines):
				self.body = "\r\n".join(lines[body_index:])

			# Extract token from Authorization header (if present)
			auth_header = self.headers.get("Authorization", "")
			if auth_header.startswith("Bearer "):
				self.token = auth_header.split(" ")[1]
		except Exception as e:
			print(errorlog('Error parsing request:', e))