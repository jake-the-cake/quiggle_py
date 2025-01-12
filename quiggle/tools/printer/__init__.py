from .colors import colors
from .printer import Printer

def print_error(error_type: str, exception: Exception) -> str:
    Printer(f'{ colors.white_on_red(" " + error_type + " Error: ") } { exception }')

def print_note(*message: str) -> str:
    Printer(f'* { " ".join(message) }').line('brightblue_on_lightgray')