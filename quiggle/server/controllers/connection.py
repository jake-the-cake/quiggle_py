## local imports
from quiggle.tools.codes.create import generate_code
from quiggle.tools.logs.presets import infolog, buglog, labellog

## global imports
import datetime, time

class ConnectionLogger:

	PREFIX = {
		'request': infolog('REQ'),
		'response': labellog('RES'),
		'connect': 'CONNECT'
	}

	def __init__(self, client_address: str, code_length: int = 12) -> None:
		self.id:        str = generate_code(length=code_length, mode='upper')
		self.address:   str = client_address
		self.timestamp: str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
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
		print(buglog(' '.join([self.PREFIX['connect'], self.address,'::', self.id, self.timestamp])))

	def log_request(self, method: str, path: str) -> None:
		print(infolog(self.PREFIX['request']), self.id, method, path, self.get_milliseconds(1))
	
	def log_response(self, status_code: str, status: str) -> None:
		print(labellog(self.PREFIX['response']), self.id, status_code, status, self.get_milliseconds(1))