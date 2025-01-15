## local imports
from quiggle.tools.codes.create import generate_code
from quiggle.tools.printer import colors, Printer, print_note

## global imports
import datetime, time

class ConnectionLogger:

	PREFIX = {
		'request': colors.red('REQ'),
		'response': colors.red('RES'),
		'connect': 'CONNECT'
	}

	def __init__(self, client_address: str, code_length: int = 12) -> None:
		self.id:        str = generate_code(length=code_length, mode='upper')
		self.address:   str = client_address
		self.timestamp: str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		# self.message = []
		self.start_timer()
		# self.log_connection()
	
	def start_timer(self) -> None:
		self.start_time = time.time()

	def get_elapsed(self, restart: bool = True) -> float:
		start = self.start_time
		if restart: self.start_timer()
		return (time.time() - start) * 1000
	
	def get_milliseconds(self, length: int = 1, format: str = '  ') -> str:
		return str(round(self.get_elapsed(), length)) + 'ms'
	
	def _response_code(self, code: int) -> str:
		"""
		Sets the response code with appropriate color based on its category.

		:param code: HTTP response code as an integer.
		"""
		return {
			'2': colors.white_on_green,
			'3': colors.black_on_yellow,
		}.get(str(code)[0], colors.white_on_red)(f' { code } ')
	
	def _response_message(self, response) -> str:
		return self._response_code(
			response.status_code) + colors.white_on_magenta(
				f' { response.STATUS_MESSAGES[response.status_code] } ')

	def _request_details(self, request) -> str:
		return request.method, request.path
	
	def respond(self, request, response) -> None:
		print_note(self._response_message(response),
			self.timestamp,
			# f'({ self.address })',
			*self._request_details(request),
			f'({ self.get_milliseconds(1) })')
	# def log_response(self, status_code: str, status: str) -> None:
	# 	self._set_response_code(status_code)
	# 	self.message = [self.id] + self.message
	# 	self.message.append(status)
	# 	self.message.append(f'({ self.get_milliseconds(1) })')
	# 	print_note(' '.join(self.message))