## local imports
from quiggle.tools.logs.presets import questionlog
from quiggle.config import globals

def connected(host: str, port: int, name: str) -> str:
	return f'\n\t{ name } is live on { host }:{ port }\n\t--> [Powered by { questionlog(f'Quiggle v{ globals.VERSION_NUMBER }') }]\n'

def closed(connection: str) -> str:
	return f'{ connection } connection closed.'

MESSAGES = {
	'connected': connected,
	'closed': closed
}