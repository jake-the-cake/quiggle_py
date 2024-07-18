class Headers:
	
	new_line = '\r\n'
	new_section = '\r\n\r\n'
	req_line = None
	headers = None
	body = None
	
	def __init__(self, request) -> None:
		sections = request.split(self.new_section)
		variables = ['headers', 'body']
		for i in range(len(sections)):
			try:
				self._methods()[variables[i]](sections[i])
			except IndexError as e:
				print('No {}'.format(variables[i]))
			except Exception as e:
				print('@ Headers Init', e)

	# Get variables, or all values
	def get_req_line(self):	return self.req_line
	def get_headers(self): return self.headers
	def get_body(self): return self.body
	def get_values(self):	return self.req_line, self.headers, self.body

	# Shortcut method dictionary
	def _methods(self):
		return {
			'headers': self.set_headers,
			'body': self.set_body
		}
	
	def set_body(self, body):
		self.body = body

	def set_headers(self, headers):
		self.headers = {}
		self.parse_headers(headers)

	def parse_headers(self, headers):
		split_char = ': '
		lines = self.split_header_lines(headers)
		self.req_line = lines[0]
		lines = lines[1:]
		for line in lines:
			split_line = line.split(split_char)
			self.headers[split_line[0]] = split_char.join(split_line[1:])

	def split_header_lines(self, headers):
		return headers.split(self.new_line)