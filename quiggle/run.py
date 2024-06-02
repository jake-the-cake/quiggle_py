from config import settings
from typing import Callable

app = None



def incomplete_function( func: Callable[[any], any] ) -> None:
	print(f'{ func.__name__ } is not done')


def use_dev_mode():
	app = None
	incomplete_function(use_dev_mode)

if settings.DEV_MODE == True:	use_dev_mode()