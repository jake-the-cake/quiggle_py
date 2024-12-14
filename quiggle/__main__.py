## local imports
from quiggle.server import server
from quiggle.cli import CliController

def cli(): CliController()

if __name__ == '__main__':
    app = server.QuiggleServer(name = 'Angieland')
    app.start()