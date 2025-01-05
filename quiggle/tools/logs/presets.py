## local imports
from .colors import Colors

## global imports
import shutil

def useColor(message: str, fg: str = None, bg: str = None, reset: str = False):
	if reset == False: reset = Colors.RESET
	else: reset = ''
	prefix: str = ''
	if fg: prefix += Colors.get_attribute(fg) or ''
	if bg: prefix += Colors.get_attribute('BACKGROUND_' + bg) or ''
	return prefix + message + reset

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
		return useColor(*content, fg='yellow', reset=True)	
	
	@staticmethod
	def fg_red(*content) -> str:
		return useColor(*content, fg='red', reset=True)	
	
	@staticmethod
	def fg_white(*content) -> str:
		return useColor(*content, fg='white', reset=True)	
	
	@staticmethod
	def fg_blue(*content) -> str:
		return useColor(*content, fg='blue', reset=True)	
	
	@staticmethod
	def fg_brightgreen(*content) -> str:
		return useColor(*content, fg='bright_green', reset=True)

	@staticmethod
	def fg_black(*content) -> str:
		return useColor(*content, fg='black', reset=True)

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