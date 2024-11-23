## local imports
from quiggle.tools.logs.presets import questionlog
from quiggle.config import globals

def connected(host: str, port: int, name: str):
	return '{} is live on {}:{}...\n\tPowered by {}.'.format(name, host, port, questionlog('Quiggle v{}'.format(globals.VERSION_NUMBER)))

MESSAGES = {
	'connected': connected
}