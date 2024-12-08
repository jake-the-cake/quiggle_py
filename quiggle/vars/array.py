class Array:

	def __init__(self, value: any, **kwargs) -> None:
		if 'split' in kwargs:
			if isinstance(value, str): value = value.split(kwargs['split'])
			else: print('Can only split a string.')
		if 'items' in kwargs:
			while len(value) < kwargs['items']:
				value.append('')
			value = value[:kwargs['items']]
		self.values = value
	
	def change_value_by_index(self, index: int, value: int):
		return {
			'=': str(value),
			'+': str(int(self.values[index]) + value),
			'-': str(int(self.values[index]) - value),
		}
	
	def to_string(self, join: str = ''):
		return join.join(self.values)