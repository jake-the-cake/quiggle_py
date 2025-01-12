from .colors import colors
from .printer import Printer

def print_error(error_type: str, *message: tuple) -> str:
    print(error_type, message)
    Printer(f'{ colors.white_on_red(" " + error_type + " Error: ") } { message }')