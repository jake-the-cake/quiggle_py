

# def useColor(message: str, foreground: str = None, background: str = None):
# 	prefix: str = ''
# 	if foreground: prefix += Colors.get_color(foreground) or ''
# 	if background: prefix += Colors.get_color('BACKGROUND_' + background) or ''
# 	return prefix + message + Colors.RESET

# class UseColor:

# 	@staticmethod
# 	def red(*content) -> str:
# 		return useColor(*content, foreground='red')
	
# 	@staticmethod
# 	def yellow(*content) -> str:
# 		return useColor(*content, foreground='yellow')
	
# 	@staticmethod
# 	def brightgreen(*content) -> str:
# 		return useColor(*content, foreground='brightgreen')

# 	@staticmethod
# 	def white_on_red(*content) -> str:
# 		return useColor(*content, foreground='white', background='red')		
	
# 	@staticmethod
# 	def white_on_green(*content) -> str:
# 		return useColor(*content, foreground='white', background='green')		
	
# 	@staticmethod
# 	def black_on_yellow(*content) -> str:
# 		return useColor(*content, foreground='black', background='yellow')		
	
# 	@staticmethod
# 	def black_on_lightgray(*content) -> str:
# 		return useColor(*content, foreground='black', background='lightgray')
	
# 	@staticmethod
# 	def black_on_magenta(*content) -> str:
# 		return useColor(*content, foreground='black', background='magenta')

# 	@staticmethod
# 	def white_on_magenta(*content) -> str:
# 		return useColor(*content, foreground='white', background='magenta')

# 	@staticmethod
# 	def foreground_yellow(*content) -> str:
# 		return useColor(*content, foreground='yellow')[:-4]	
	
# 	@staticmethod
# 	def foreground_red(*content) -> str:
# 		return useColor(*content, foreground='red')[:-4]	
	
# 	@staticmethod
# 	def foreground_white(*content) -> str:
# 		return useColor(*content, foreground='white')[:-4]	
	
# 	@staticmethod
# 	def foreground_blue(*content) -> str:
# 		return useColor(*content, foreground='blue')[:-4]	
	
# 	@staticmethod
# 	def foreground_brightgreen(*content) -> str:
# 		return useColor(*content, foreground='bright_green')[:-4]

# 	@staticmethod
# 	def foreground_black(*content) -> str:
# 		return useColor(*content, foreground='black')[:-4]
# class Print:

# 	@staticmethod
# 	def error(error: str, *content) -> None:
# 		print(UseColor.white_on_red(error), *content)
	
# 	@staticmethod
# 	def note(*content) -> None:
# 		print(UseColor.black_on_lightgray('* ' + ' '.join(content)))

# 	@staticmethod
# 	def branded(*content) -> None:
# 		print(UseColor.black_on_magenta(*content))

# 	@staticmethod
# 	def white_on_red(*content) -> None:
# 		print(UseColor.white_on_red(*content))

# 	@staticmethod
# 	def yellow(*content) -> None:
# 		print(UseColor.yellow(*content))
	
# 	@staticmethod
# 	def brightgreen(*content) -> None:
# 		print(UseColor.brightgreen(*content))
	
# 	@staticmethod
# 	def blue(*content) -> None:
# 		print(useColor(*content, foreground='blue'))
	
# 	@staticmethod
# 	def cyan(*content) -> None:
# 		print(useColor(*content, foreground='cyan'))

# 	@staticmethod
# 	def black_on_magenta(*content) -> None:
# 		print(UseColor.black_on_magenta(*content))

# 	@staticmethod
# 	def white_on_green(*content) -> None:
# 		print(UseColor.white_on_green(*content))

# 	@staticmethod	
# 	def black_on_yellow(*content) -> None:
# 		print(UseColor.black_on_yellow(*content))

# 	@staticmethod
# 	def white_on_magenta(*content) -> None:
# 		print(UseColor.white_on_magenta(*content))

# class Printline(Print):

# 	@staticmethod
# 	def full(method: str, *content: tuple) -> None:
# 		if hasattr(Print, method):
# 			padded_text = Printline._pad_text(' '.join(content))
# 			if method == 'note':
# 				padded_text = padded_text[:-2]
# 			getattr(Print, method)(padded_text)

# 	@staticmethod
# 	def _pad_text(text: str) -> str:
# 		terminal_width = shutil.get_terminal_size().columns
# 		lines = text.split('\n')
# 		for i, line in enumerate(lines):
# 			line = line.replace('\t', '        ').replace('!5', '          ')
# 			tw = terminal_width
# 			while len(line) > tw:
# 				tw += tw
# 			lines[i] = line.ljust(tw).replace('XX', '       ')
# 		return ''.join(lines)




# def infolog(message: str) -> str:
# 	return useColor(message, foreground='cyan')

# def labellog(message: str) -> str:
# 	return useColor(message, foreground='yellow')

# def questionlog(message: str) -> str:
# 	return useColor(message, foreground='bright-green')

# def errorlog(message: str) -> str:
# 	return useColor(f' { message } ', foreground='white', background='red')

# def buglog(message: str) -> None:
# 	return (
# 		Colors.BACKGROUND_BLACK + 
# 		Colors.GREEN +
# 		' >>> ' + 
# 		Colors.BACKGROUND_GREEN + 
# 		Colors.BLACK + 
# 		' ' +
# 		message +
# 		' ' +
# 		Colors.RESET
# 	)