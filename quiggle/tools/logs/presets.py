## local imports
from .colors import Colors
from quiggle.tools.quiggle import Quiggle

## global imports
import shutil

class ColorPrinter(Quiggle):

	def __init__(self, *message: tuple):
		super().__init__()
		self.message: list = self.toolkit.tuple_to_list(message)
		self._timer = self._start_timer()

	def _start_timer(self):
		timer = self.toolkit.timer.callback_delay(0.1, self._print_message)
		timer.start()
		return timer

	def _cancel_timer(self) -> None:
		if self._timer.is_alive():
			self._timer.cancel()

	def _print_message(self) -> None:
		print(self._color_code + self.message.__str__() + Colors.RESET)

	def _get_colors(self, format: str):
		return getattr(Colors, format.upper())

	def format(self, format: str) -> None:
		self._cancel_timer()
		self._color_code = self._get_colors(format)
		self._timer = self._start_timer()
		# print(Colors.RED + self.message.__str__())

ColorPrinter('this', 'is a message').format('red')

def useColor(message: str, fg: str = None, bg: str = None):
	prefix: str = ''
	if fg: prefix += Colors.get_attribute(fg) or ''
	if bg: prefix += Colors.get_attribute('BACKGROUND_' + bg) or ''
	return prefix + message + Colors.RESET

class UseColor:

	@staticmethod
	def red(*content) -> str:
		return useColor(*content, fg='red')
	
	@staticmethod
	def yellow(*content) -> str:
		return useColor(*content, fg='yellow')
	
	@staticmethod
	def brightgreen(*content) -> str:
		return useColor(*content, fg='bright_green')

	@staticmethod
	def white_on_red(*content) -> str:
		return useColor(*content, fg='white', bg='red')		
	
	@staticmethod
	def white_on_green(*content) -> str:
		return useColor(*content, fg='white', bg='green')		
	
	@staticmethod
	def black_on_yellow(*content) -> str:
		return useColor(*content, fg='black', bg='yellow')		
	
	@staticmethod
	def black_on_lightgray(*content) -> str:
		return useColor(*content, fg='black', bg='light_gray')
	
	@staticmethod
	def black_on_magenta(*content) -> str:
		return useColor(*content, fg='black', bg='magenta')

	@staticmethod
	def white_on_magenta(*content) -> str:
		return useColor(*content, fg='white', bg='magenta')

	@staticmethod
	def fg_yellow(*content) -> str:
		return useColor(*content, fg='yellow')[:-4]	
	
	@staticmethod
	def fg_red(*content) -> str:
		return useColor(*content, fg='red')[:-4]	
	
	@staticmethod
	def fg_white(*content) -> str:
		return useColor(*content, fg='white')[:-4]	
	
	@staticmethod
	def fg_blue(*content) -> str:
		return useColor(*content, fg='blue')[:-4]	
	
	@staticmethod
	def fg_brightgreen(*content) -> str:
		return useColor(*content, fg='bright_green')[:-4]

	@staticmethod
	def fg_black(*content) -> str:
		return useColor(*content, fg='black')[:-4]
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
		print(useColor(*content, fg='blue'))
	
	@staticmethod
	def cyan(*content) -> None:
		print(useColor(*content, fg='cyan'))

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
	return useColor(message, fg='cyan')

def labellog(message: str) -> str:
	return useColor(message, fg='yellow')

def questionlog(message: str) -> str:
	return useColor(message, fg='bright-green')

def errorlog(message: str) -> str:
	return useColor(f' { message } ', fg='white', bg='red')

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