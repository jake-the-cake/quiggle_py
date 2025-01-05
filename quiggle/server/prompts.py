## local imports
from quiggle.tools.logs.presets import UseColor
from quiggle.config import globals

def connected(host: str, port: int, name: str) -> str:
	return f'\n\t{ name } is live on { UseColor.fg_yellow(f'{ host }:{ port }') + UseColor.fg_white('') }XXXX\n\t--> Powered by { UseColor.fg_brightgreen(f'Quiggle v{ globals.VERSION_NUMBER }') }XX\n'

def connection_closed(connection: str) -> str:
	return f'{ connection } connection closed.'

def parsing_complete(type: str) -> None:
 return (f'{ type } parsing complete.')

def parsing_failed(type: str) -> None:
 return f'{ type } parsing failed.'

MESSAGES = {
	'connected': connected,
	'closed': connection_closed,
	'parsed': parsing_complete,
    'notparsed': parsing_failed
}