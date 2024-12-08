class Reader:

	def __init__(self, path: str) -> None:
		self.path:   str = path
		self.lines: list = []

	def get_lines(self):
		with open(self.path, 'r') as file:
			self.lines = file.readlines()
		return self