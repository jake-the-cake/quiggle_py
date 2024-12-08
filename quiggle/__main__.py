## local imports
from quiggle.server import server
from quiggle.cli.cli import CliController

def cli(): CliController()

if __name__ == '__main__':
    app = server.QuiggleServer(name = 'Angieland')
    try:
        app.start()
    except Exception as e:
        print(f"Server error: {e}")