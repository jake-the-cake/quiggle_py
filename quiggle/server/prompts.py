## local imports
from quiggle.tools.logs.presets import questionlog, labellog
from quiggle.config import globals

def connected(host: str, port: int, name: str) -> str:
	return f'\n\t{ name } is live on { labellog(f'{ host }:{ port }') }\n\t--> [Powered by { questionlog(f'Quiggle v{ globals.VERSION_NUMBER }') }]\n'

def connection_closed(connection: str) -> str:
	return f'{ connection } connection closed.'

def parsing_complete(type: str) -> None:
 return labellog(f'-- { type } parsing complete.')

MESSAGES = {
	'connected': connected,
	'closed': connection_closed,
	'parsed': parsing_complete
}