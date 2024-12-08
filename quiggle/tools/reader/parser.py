class Parser:

	def __init__(self, data: str, type: str = 'text') -> None:
		self.data: str = data
		self.type: str = type

	def strip_newline_tag(self) -> None:
		self.data = self.data.replace('\n', '')

	def append_newline_tag(self) -> None:
		self.data = self.data + '\n'

	def starts_with(self, start: str) -> bool:
		if self.data[:len(start)] == start: return True
		return False
	
	def get_value(self, separator: str) -> str:
		return self.data.split(separator)[1].strip()
	
	