''' /quiggle/server/router '''

## local imports
from .router import Router
from quiggle.tools.logs.presets import labellog

def parsing_complete(type: str) -> None:
 return labellog(f'-- { type } parsing complete.')

MESSAGES = {
	'parsed': parsing_complete
}