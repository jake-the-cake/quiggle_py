class Array:

	def __init__(self, value: any, **kwargs) -> None:
		if 'split' in kwargs:
			if isinstance(value, str): value = value.split(kwargs['split'])
			else: print('Can only split a string.')
		if 'items' in kwargs:
			while len(value) < kwargs['items']:
				value.append('')
			value = value[:kwargs['items']]
		
		self.array = list(value)
		
		self.NUMERIC_METHODS = {
			'+': self.increase_numeric_value_by_index,
			'-': self.decrease_numeric_value_by_index,
			'=': self.change_numeric_value_by_index
		}

	def increase_numeric_value_by_index(self, index: int, value: int = 1):
		self.array[index] = str(int(self.array[index]) + value)
	
	def decrease_numeric_value_by_index(self, index: int, value: int = 1):
		self.array[index] = str(int(self.array[index]) - value)
		
	def change_numeric_value_by_index(self, index: int, value: int = 1):
		self.array[index] = str(value)

	def edit_numeric_value_by_index(self, index: int, value: int, operator: str = '=') -> None:
		self.NUMERIC_METHODS[operator](index, value)
	
	def to_string(self, joint: str = ''):
		return joint.join(self.array)