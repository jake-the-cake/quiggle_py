class Colors:
    """
    A utility class for handling ANSI color codes for foregrounds, backgrounds, 
    and text formatting. Dynamically creates methods for color and style combinations.
    """

    # Background colors
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

    # Foreground colors
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

    # Special features
    RESET = '\033[0m'

    def __init__(self):
        """
        Initialize the Colors class by dynamically generating methods for all
        color combinations and variations.
        """
        self.colors = self._extract_colors()
        self.foregrounds = [name for name in self.colors if not name.startswith('BACKGROUND')]
        self.backgrounds = [name for name in self.colors if name.startswith('BACKGROUND')]
        self._generate_color_methods()

    def _extract_colors(self) -> dict:
        """
        Extract all ANSI color codes defined in the class.
        Returns:
            dict: A dictionary of property names and their corresponding ANSI codes.
        """
        return {name: value for name, value in vars(self.__class__).items() if isinstance(value, str)}

    def _generate_color_methods(self) -> None:
        """
        Dynamically create methods for:
        1. Foreground colors
        2. Background colors
        3. Foreground on background combinations
        """
        for fg in self.foregrounds:
            self._add_color_method(fg.lower(), self.colors[fg])

            for bg in self.backgrounds:
                method_name = f"{fg.lower()}_on_{self._format_background_name(bg)}"
                self._add_color_method(method_name, self.colors[fg] + self.colors[bg])

        for bg in self.backgrounds:
            method_name = f"on_{self._format_background_name(bg)}"
            self._add_color_method(method_name, self.colors[bg])

    def _add_color_method(self, name: str, code: str) -> None:
        """
        Add a color method to the class.
        Args:
            name (str): The name of the method.
            code (str): The ANSI code the method represents.
        """
        setattr(self, name, lambda message, c=code: f"{c}{message}{self.RESET}")

    @staticmethod
    def _format_background_name(name: str) -> str:
        """
        Format a background property name to make it readable in method names.
        Args:
            name (str): The original property name (e.g., 'BACKGROUND_RED').
        Returns:
            str: A formatted name (e.g., 'red').
        """
        return name.replace('BACKGROUND_', '').lower()

    @staticmethod
    def get_color(value: str) -> str:
        """
        Retrieve the ANSI code for a given color name.
        Args:
            value (str): The name of the color (case-insensitive, hyphen allowed).
        Returns:
            str: The corresponding ANSI code or an empty string if not found.
        """
        key = value.upper().replace('-', '_')
        return getattr(Colors, key, '')

# compiled color object
colors = Colors()