## local imports
from .colors import Colors
from quiggle.tools.quiggle import Quiggle

## global imports
import shutil

class ColorPrinter(Quiggle):

	ON = '_on_'
	WITH = '_with_'

	def __init__(self, *message: tuple):
		super().__init__()
		self._colors:        str = Colors.RESET
		self._message:      list = self.toolkit.tuple_to_list(message)
		self._final_message: str = ''
		self._timer = self._start_timer()

	def line(self, scheme: str) -> None:
		self._build_message(scheme, self._print_full_line)

	def text(self, scheme: str) -> None:
		self._build_message(scheme)

	def _message_to_string(self) -> None:
		self._final_message = ' '.join(self._message)

	def _build_message(self, scheme: str = '', *callbacks: tuple[callable]) -> None:
		self._cancel_timer()
		if scheme != '': self._set_colors(scheme)
		self._message_to_string()
		self._reset_colors()
		for callback in  callbacks:
			callback()
		self._print_message()

	def _print_full_line(self):
		lines = self._get_text_lines()
		terminal_width = shutil.get_terminal_size().columns
		self._parse_lines(lines, terminal_width)

	def _parse_lines(self, lines: list, width: int):
		for index, line in enumerate(lines):
			w = width
			line = self._count_hidden_chars(line)
			while w < len(line): w += w
			lines[index] = line.ljust(w)
			self._final_message = '\n'.join(lines)

	def _count_hidden_chars(self, line: str) -> str:
		return line

	def _get_text_lines(self) -> list:
		return self._final_message.split('\n')

	def _reset_colors(self) -> None:
		self._final_message = self._final_message.replace(Colors.RESET, self._colors)

	def _set_colors(self, scheme: str) -> None:
		split_on, split_with = self._parse_colors(scheme)
		colors = [split_on[0]] + split_with + ['', '']
		self._add_colors(colors[:2])

	def _parse_colors(self, scheme: str) -> tuple:
		split_on = scheme.split(self.ON)
		split_with = split_on[-1].split(self.WITH)
		if len(split_on) == 1 and len(split_with) == 1:	split_with = []
		return split_on, split_with

	def _add_colors(self, colors: list) -> None:
		self._set_color(colors[0])
		self._set_background(colors[1])

	def _set_color(self, value: str) -> None:
		value = value.upper()
		if hasattr(Colors, value):
			self._colors += Colors.get_attribute(value)

	def _set_background(self, value: str) -> None:
		self._set_color('BACKGROUND_' + value)

	def _start_timer(self):
		timer = self.toolkit.timer.callback_delay(0.1, self._print_message)
		timer.start()
		return timer

	def _cancel_timer(self) -> None:
		if self._timer.is_alive():
			self._timer.cancel()

	def _print_message(self) -> None:
		print(self._colors + self._final_message.__str__() + Colors.RESET)

ColorPrinter('this', 'is', Colors.BLUE, 'a', Colors.RESET, 'message').text('red_on_white')
ColorPrinter('this', 'is', Colors.RED, 'a\n', Colors.RESET, 'message').line('white_on_green')

def useColor(message: str, foreground: str = None, background: str = None):
	prefix: str = ''
	if foreground: prefix += Colors.get_attribute(foreground) or ''
	if background: prefix += Colors.get_attribute('BACKGROUND_' + background) or ''
	return prefix + message + Colors.RESET

class UseColor:

	@staticmethod
	def red(*content) -> str:
		return useColor(*content, foreground='red')
	
	@staticmethod
	def yellow(*content) -> str:
		return useColor(*content, foreground='yellow')
	
	@staticmethod
	def brightgreen(*content) -> str:
		return useColor(*content, foreground='brightgreen')

	@staticmethod
	def white_on_red(*content) -> str:
		return useColor(*content, foreground='white', background='red')		
	
	@staticmethod
	def white_on_green(*content) -> str:
		return useColor(*content, foreground='white', background='green')		
	
	@staticmethod
	def black_on_yellow(*content) -> str:
		return useColor(*content, foreground='black', background='yellow')		
	
	@staticmethod
	def black_on_lightgray(*content) -> str:
		return useColor(*content, foreground='black', background='lightgray')
	
	@staticmethod
	def black_on_magenta(*content) -> str:
		return useColor(*content, foreground='black', background='magenta')

	@staticmethod
	def white_on_magenta(*content) -> str:
		return useColor(*content, foreground='white', background='magenta')

	@staticmethod
	def foreground_yellow(*content) -> str:
		return useColor(*content, foreground='yellow')[:-4]	
	
	@staticmethod
	def foreground_red(*content) -> str:
		return useColor(*content, foreground='red')[:-4]	
	
	@staticmethod
	def foreground_white(*content) -> str:
		return useColor(*content, foreground='white')[:-4]	
	
	@staticmethod
	def foreground_blue(*content) -> str:
		return useColor(*content, foreground='blue')[:-4]	
	
	@staticmethod
	def foreground_brightgreen(*content) -> str:
		return useColor(*content, foreground='bright_green')[:-4]

	@staticmethod
	def foreground_black(*content) -> str:
		return useColor(*content, foreground='black')[:-4]
class Print:

	@staticmethod
	def error(error: str, *content) -> None:
		print(UseColor.white_on_red(error), *content)
	
	@staticmethod
	def note(*content) -> None:
		print(UseColor.black_on_lightgray('* ' + ' '.join(content)))

	@staticmethod
	def branded(*content) -> None:
		print(UseColor.black_on_magenta(*content))

	@staticmethod
	def white_on_red(*content) -> None:
		print(UseColor.white_on_red(*content))

	@staticmethod
	def yellow(*content) -> None:
		print(UseColor.yellow(*content))
	
	@staticmethod
	def brightgreen(*content) -> None:
		print(UseColor.brightgreen(*content))
	
	@staticmethod
	def blue(*content) -> None:
		print(useColor(*content, foreground='blue'))
	
	@staticmethod
	def cyan(*content) -> None:
		print(useColor(*content, foreground='cyan'))

	@staticmethod
	def black_on_magenta(*content) -> None:
		print(UseColor.black_on_magenta(*content))

	@staticmethod
	def white_on_green(*content) -> None:
		print(UseColor.white_on_green(*content))

	@staticmethod	
	def black_on_yellow(*content) -> None:
		print(UseColor.black_on_yellow(*content))

	@staticmethod
	def white_on_magenta(*content) -> None:
		print(UseColor.white_on_magenta(*content))

class Printline(Print):

	@staticmethod
	def full(method: str, *content: tuple) -> None:
		if hasattr(Print, method):
			padded_text = Printline._pad_text(' '.join(content))
			if method == 'note':
				padded_text = padded_text[:-2]
			getattr(Print, method)(padded_text)

	@staticmethod
	def _pad_text(text: str) -> str:
		terminal_width = shutil.get_terminal_size().columns
		lines = text.split('\n')
		for i, line in enumerate(lines):
			line = line.replace('\t', '        ').replace('!5', '          ')
			tw = terminal_width
			while len(line) > tw:
				tw += tw
			lines[i] = line.ljust(tw).replace('XX', '       ')
		return ''.join(lines)




def infolog(message: str) -> str:
	return useColor(message, foreground='cyan')

def labellog(message: str) -> str:
	return useColor(message, foreground='yellow')

def questionlog(message: str) -> str:
	return useColor(message, foreground='bright-green')

def errorlog(message: str) -> str:
	return useColor(f' { message } ', foreground='white', background='red')

def buglog(message: str) -> None:
	return (
		Colors.BACKGROUND_BLACK + 
		Colors.GREEN +
		' >>> ' + 
		Colors.BACKGROUND_GREEN + 
		Colors.BLACK + 
		' ' +
		message +
		' ' +
		Colors.RESET
	)