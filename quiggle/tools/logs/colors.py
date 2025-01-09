class Colors:

	BACKGROUND_BLACK = '\033[40m'
	BACKGROUND_RED = '\033[41m'
	BACKGROUND_GREEN = '\033[42m'
	BACKGROUND_YELLOW = '\033[43m'
	BACKGROUND_BLUE = '\033[44m'
	BACKGROUND_MAGENTA = '\033[45m'
	BACKGROUND_CYAN = '\033[46m'
	BACKGROUND_LIGHTGRAY = '\033[47m'
	BACKGROUND_DARKGRAY = '\033[100m'
	BACKGROUND_BRIGHTRED = '\033[101m'
	BACKGROUND_BRIGHTGREEN = '\033[102m'
	BACKGROUND_BRIGHTYELLOW = '\033[103m'
	BACKGROUND_BRIGHTBLUE = '\033[104m'
	BACKGROUND_BRIGHTMAGENTA = '\033[105m'
	BACKGROUND_BRIGHTCYAN = '\033[106m'
	BACKGROUND_WHITE = '\033[107m'

	BLACK = '\033[30m'
	RED = '\033[31m'
	GREEN = '\033[32m'
	YELLOW = '\033[33m'
	BLUE = '\033[34m'
	MAGENTA = '\033[35m'
	CYAN = '\033[36m'
	LIGHTGRAY = '\033[37m'
	DARKGRAY = '\033[90m'
	BRIGHTRED = '\033[91m'
	BRIGHTGREEN = '\033[92m'
	BRIGHTYELLOW = '\033[93m'
	BRIGHTBLUE = '\033[94m'
	BRIGHTMAGENTA = '\033[95m'
	BRIGHTCYAN = '\033[96m'
	WHITE = '\033[97m'

	RESET = '\033[0m'

	def __init__(self):
		self._build_methods()

	def _build_methods(self) -> None:
		for color_name, color_code in self._parse_properties().items():
			def _base_method(message: str, color_code: str = color_code) -> str:
				return color_code + message + Colors.RESET
			setattr(self, color_name.lower(), _base_method)

	def _parse_properties(self) -> dict:
		properties: dict = {}
		for name, value in vars(self.__class__).items():
			if isinstance(value, str):
				if 'BACKGROUND_' in name:
					name = name.replace('BACKGROUND_', '_on_')
				properties[name] = value
		return properties

	@staticmethod
	def get_color(value: str) -> str:
		value = value.upper().replace('-', '_')
		if value in Colors.__dict__.keys():
			return Colors.__dict__[value]
	
colors = Colors()
# print(colors.red('test'))/
print(colors._on_red('test'))