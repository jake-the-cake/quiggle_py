## local imports
from quiggle.tools.printer.colors import colors
from quiggle.tools.quiggle import Quiggle

## global imports
import shutil

class Printer(Quiggle):

	ON = '_on_'
	WITH = '_with_'

	def __init__(self, *message: tuple):
		super().__init__()
		self._colors:        str = colors.RESET
		self._message:      list = self.toolkit.tuple_to_list(message)
		# self._final_message: str = ''
		self._message_to_string()
		self._timer = self._start_timer()

	def line(self, scheme: str) -> None:
		if hasattr(colors, scheme):
			print(getattr(colors, scheme)('test'))
		self._build_message(scheme, self._print_full_line)

	def text(self, scheme: str) -> None:
		self._build_message(scheme)
	   
	def _message_to_string(self) -> None:
		self._final_message = ' '.join(self._message)

	def _build_message(self, scheme: str = '', *callbacks: tuple[callable]) -> None:
		if scheme == '': return
		self._cancel_timer()
		if scheme == 'error':
			self._message[0] = colors.white_on_red(self._message[0])
		else:
			# if hasattr(colors, scheme): getattr(colors, scheme)()
			self._set_colors(scheme)
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
		self._final_message = self._final_message.replace(colors.RESET, self._colors)

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
		if hasattr(colors, value):
			self._colors += colors.get_color(value)

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
		print(self._colors + self._final_message.__str__() + colors.RESET)

Printer('this', 'is', colors.blue_on_red('a'), 'message').text('red_on_white')
Printer('this', 'is', colors.white_on_black('a\n'), 'message').line('white_on_green')
Printer('test', 'error').line('error')


# shortcut functions

def print_error(error_type: str, exception: Exception) -> str:
    Printer(f'{ colors.white_on_red(" " + error_type + " Error: ") } { exception }')

def print_note(*message: str) -> str:
    Printer(f'* { " ".join(message) }').line('on_blue')