## local imports
from quiggle.tools.codes.create import generate_code
from quiggle.tools.printer import colors, Printer

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
		self.message = []
		self.start_timer()
		self.log_connection()
	
	def start_timer(self) -> None:
		self.start_time = time.time()

	def get_elapsed(self, restart: bool = True) -> float:
		start = self.start_time
		if restart: self.start_timer()
		return (time.time() - start) * 1000
	
	def get_milliseconds(self, length: int = 1, format: str = '  ') -> str:
		return str(round(self.get_elapsed(), length)) + 'ms'
	
	def log_connection(self) -> None:
		Printer(f'{ self.timestamp } >>> Connection { self.id } established from { self.address }').line('note')

	def _set_response_code(self, code: int) -> None:
		x = str(code)[0]
		if x == '2':
			self.message = [colors.white_on_green((f' { str(code) } '))[:-4] + colors.black_on_lightgray('')[:-4]] + self.message 
		elif x == '3':
			self.message = [colors.black_on_yellow((f' { str(code) } '))[:-4] + colors.black_on_lightgray('')[:-4]] + self.message
		else:
			self.message = [colors.white_on_red((f' { str(code) } '))[:-4] + colors.black_on_lightgray('')[:-4]] + self.message

	def add_request_info(self, method: str, path: str) -> None:
		self.message.append(method)
		self.message.append(path)
	
	def log_response(self, status_code: str, status: str) -> None:
		self._set_response_code(status_code)
		self.message = [self.id] + self.message
		self.message.append(status)
		self.message.append(f'({ self.get_milliseconds(1) })')
		Printer(' '.join(self.message)).line('note')