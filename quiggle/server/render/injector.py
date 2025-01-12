## local imports
from quiggle.tools.printer import Printer

class HTMLInjector:
	
	def __init__(self, html: str, variables: dict = None):
		self._init_html(html)
		self.variables: dict = variables
		self.position: int   = 0
		self.hold_pos: int   = 0
		self.instances: dict = {}
		self.tags            = { 
				'use': self.use_use
			}
		
	def _init_html(self, html: str) -> None:
		self.original_html = html
		self.updated_html = html

	def use_use(self, variable, attributes):
		values = []
		if variable in self.variables: values.append(self.variables[variable])
		else: values.append('')

		def strip_quotes(string: str) -> str:
			if string[0] == '"' or string[0] == "'":
				return string[1:-1]

		def use_properties(attributes):
			if len(attributes) < 2: return
			if attributes[0].lower() == 'or':
				if values[-1] == '':
					values[-1] = strip_quotes(attributes[1])
			if attributes[0].lower() == 'and':
				if attributes[1] in self.variables:
					values.append(self.variables[attributes[1]])
				else:
					values.append('')
			use_properties(attributes[2:])
		use_properties(attributes)
		return values

	def is_position_lt_len(self) -> bool:
		return len(self.original_html) - 1 > self.position

	def get_char(self) -> str:
		return self.original_html[self.position]

	def get_next_char(self) -> str:
		if self.is_position_lt_len():
			return self.original_html[self.position + 1]
		return self.get_char()
	
	def increment_positions(self) -> None:
		if self.is_position_lt_len():
			self.position += 1
			self.hold_pos = self.position

	def find_tags(self) -> None:
		while self.position < len(self.original_html) - 1:
			self.find_open_tag('<')

	def find_open_tag(self, tag: str) -> None:
		if not self.get_char() == tag:
			return self.increment_positions()
		self.find_next_blank()

	def find_next_blank(self):
		self.position += 1
		if self.get_char() == '>':
			return self.increment_positions() 
		if self.get_char() != ' ':
			return self.find_next_blank()
		tag = self.original_html[self.hold_pos + 1 : self.position]
		if tag in self.tags.keys():
			if tag not in self.instances.keys():
				self.instances[tag] = []
			return self.find_closing_tag(tag)
		return self.increment_positions()

	def find_closing_tag(self, tag: str):
		self.position += 1
		if self.get_char() == '/' and self.get_next_char() == '>':
			self.instances[tag].append(self.original_html[self.hold_pos : self.position + 2])
			return self.increment_positions()
		return self.find_closing_tag(tag)

	def inject(self) -> None:

		def clean_attributes(attributes: list):
			attributes = [item for item in attributes if item != '']
			
			def find_end_of_string(quote: str, index: int, start: int):
				if attributes[index][-1] != quote:
					return find_end_of_string(quote, index + 1, start)
				return attributes[:start] + [' '.join(attributes[start:index + 1])] + attributes[index + 1:]
			
			while True:
				length: int = len(attributes)
				for index, item in enumerate(attributes):
					if item[0] == "'" or item[0] == '"':
						attributes = find_end_of_string(item[0], index, index)
				if len(attributes) == length:	break
			return attributes

		self.find_tags()
		for tag in self.instances.keys():
			for instance in self.instances[tag]:
				try:	
					split_string  = instance[1:-2].split(' ')
					variable      = split_string[1]
					attributes = clean_attributes(' '.join(split_string[2:]).replace('=', ' ').split(' '))
					values = self.tags[tag](variable, attributes)
					self.updated_html = self.updated_html.replace(instance, ' '.join(values))
				except Exception as e:
					Printer(f'Could not parse "{ tag }" tag:', e).line('error')
		return self.updated_html