## local imports
from quiggle.tools.printer.colors import colors
from quiggle.tools.quiggle import Quiggle

## global imports
import shutil
import re

class Printer(Quiggle):

	def __init__(self, *message: tuple):
		super().__init__()
		self._colors:  str = colors.RESET
		self._message: str = self.toolkit.tuple_to_str(message)
		self._timer = self._start_timer()

	def line(self, scheme: str) -> None:
		self.text(scheme, True)

	def text(self, scheme: str, padded: bool = False) -> None:
		self._cancel_timer()
		self._set_colors(scheme)
		self._reset_colors()
		if padded == True:
			self._pad_text()
		self._print_message()

	def _pad_text(self):
		lines = self._get_text_lines()
		terminal_width = shutil.get_terminal_size().columns
		self._parse_lines(lines, terminal_width)

	def _parse_lines(self, lines: list, width: int):
		for index, line in enumerate(lines):
			w = width
			line = self._count_hidden_chars(line)
			while w < len(line): w += w
			characters = re.compile(r'\033\[[0-9;]*[A-Za-z]').findall(line)
			lines[index] = line.ljust(w + sum(len(chars) for chars in characters) - (7 * line.count('\t')))
			self._message = '\n'.join(lines)

	def _count_hidden_chars(self, line: str) -> str:
		return line

	def _get_text_lines(self) -> list:
		return self._message.split('\n')

	def _reset_colors(self) -> None:
		self._message = self._message.replace(colors.RESET, self._colors)

	def _set_colors(self, scheme: str) -> None:
		if hasattr(colors, scheme):
			self._scheme = getattr(colors, scheme)
			self._colors += self._scheme('split').split('split')[0]

	def _start_timer(self):
		timer = self.toolkit.timer.callback_delay(0.1, self._print_message)
		timer.start()
		return timer

	def _cancel_timer(self) -> None:
		if self._timer.is_alive():
			self._timer.cancel()

	def _print_message(self) -> None:
		print(self._colors + self._message + colors.RESET)

# shortcut functions
def print_error(error_type: str, exception: Exception) -> str:
    Printer(f'{ colors.white_on_red(" " + error_type + " Error: ") } { exception }')

def print_note(*message: str) -> str:
    Printer(f'* { " ".join(message) }').line('lightgray_on_black')