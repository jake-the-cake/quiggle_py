from .colors import Colors

def useColor(message: str, fg: str = None, bg: str = None):
	prefix: str = ''
	if fg: prefix += Colors.get_attribute(fg) or ''
	if bg: prefix += Colors.get_attribute('BACKGROUND_' + bg) or ''
	return prefix + message + Colors.RESET

class Print:

	@staticmethod
	def error(error: str, *content) -> None:
		print(useColor(error, fg='white', bg='red'), *content)

	@staticmethod
	def yellow(*content) -> None:
		print(useColor(*content, fg='yellow'))
	
	@staticmethod
	def green(*content) -> None:
		print(useColor(*content, fg='green'))
	
	@staticmethod
	def blue(*content) -> None:
		print(useColor(*content, fg='blue'))
	
	@staticmethod
	def cyan(*content) -> None:
		print(useColor(*content, fg='cyan'))

class UseColor:

	@staticmethod
	def red(*content) -> None:
		return useColor(*content, fg='red')




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