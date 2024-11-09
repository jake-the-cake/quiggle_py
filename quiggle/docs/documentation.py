def arg_value_required(value: str) -> Exception:
	raise ValueError('A value is required for {} argument.'.format(value))

class Documentation:

	def __init__(self, name: str = None, description: str = None, **kwargs) -> None:
		
		# check for required values
		if not name:
			arg_value_required('name')
		
		self.name				 = name
		self.description = description
		self.functions   = []
		self.variables   = []
		self.usage       = []

		if 'usage' in kwargs:
			
			print(kwargs.get('usage'))


	def function(self, name: str = None, description: str = None, **kwargs):
		self.functions.append(Documentation(name, description, **kwargs))