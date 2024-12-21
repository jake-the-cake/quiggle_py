''' /quiggle/server/router '''

## local imports
from .router import Router
from quiggle.tools.logs.presets import labellog

def parsing_complete(type: str) -> None:
 return labellog(f'-- { type } parsing complete.')

def not_set(key: str, filename: str):
    return Exception(f'Please set { key } in "{ filename }"')

MESSAGES = {
	'parsed': parsing_complete
}