class Parser:

	def __init__(self, data: str, type: str = 'text') -> None:
		self.original_data: str = data
		self.data:          str = self.original_data
		self.type:          str = type

	def strip_newline_tag(self) -> None:
		self.data = self.data.strip('\n')

	def append_newline_tag(self) -> None:
		self.data = f'{ self.data }\n'

	def starts_with(self, start: str, *callbacks) -> bool:
		if self.data[:len(start)] == start:
			if len(callbacks) > 0:
				for callback in callbacks: callback()
			return True
		return False
	
	def get_value(self, separator: str) -> str:
		return self.data.split(separator)[1].strip()
	
	def set_data(self, value: str, *callbacks) -> None:
		self.data = value
		if len(callbacks) > 0:
			for callback in callbacks: callback()
	
	