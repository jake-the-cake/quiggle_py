class Colors:
	BACKGROUND_BLACK = '\033[40m'
	BACKGROUND_RED = '\033[41m'
	BACKGROUND_GREEN = '\033[42m'
	BACKGROUND_YELLOW = '\033[43m' # orange on some systems
	BACKGROUND_BLUE = '\033[44m'
	BACKGROUND_MAGENTA = '\033[45m'
	BACKGROUND_CYAN = '\033[46m'
	BACKGROUND_LIGHT_GRAY = '\third-party033[47m'
	BACKGROUND_DARK_GRAY = '\033[100m'
	BACKGROUND_BRIGHT_RED = '\033[101m'
	BACKGROUND_BRIGHT_GREEN = '\033[102m'
	BACKGROUND_BRIGHT_YELLOW = '\033[103m'
	BACKGROUND_BRIGHT_BLUE = '\033[104m'
	BACKGROUND_BRIGHT_MAGENTA = '\033[105m'
	BACKGROUND_BRIGHT_CYAN = '\033[106m'
	BACKGROUND_WHITE = '\033[107m'

	BLACK = '\033[30m'
	RED = '\033[31m'
	GREEN = '\033[32m'
	YELLOW = '\033[33m' # orange on some systems
	BLUE = '\033[34m'
	MAGENTA = '\033[35m'
	CYAN = '\033[36m'
	LIGHT_GRAY = '\033[37m'
	DARK_GRAY = '\033[90m'
	BRIGHT_RED = '\033[91m'
	BRIGHT_GREEN = '\033[92m'
	BRIGHT_YELLOW = '\033[93m'
	BRIGHT_BLUE = '\033[94m'
	BRIGHT_MAGENTA = '\033[95m'
	BRIGHT_CYAN = '\033[96m'
	WHITE = '\033[97m'

	RESET = '\033[0m' # called to return to standard terminal text color

def log_bug(message: str) -> None:
	print(
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