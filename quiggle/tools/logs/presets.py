from .colors import Colors

def useColor(message: str, fg: str = None, bg: str = None):
	prefix: str = ''
	if fg: prefix += Colors.get_attribute(fg) or ''
	if bg: prefix += Colors.get_attribute('BACKGROUND_' + bg) or ''
	return prefix + message + Colors.RESET

def infolog(message: str) -> str:
	return useColor(message, fg='cyan')