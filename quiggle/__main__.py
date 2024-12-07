## local imports
from quiggle.server import server
from quiggle.cli.version import update_version
from quiggle.config.globals import QUIGGLE_DIR

def cli():
    print('cli')
    update_version(QUIGGLE_DIR + '/config/globals.py')

if __name__ == '__main__':
    app = server.QuiggleServer(name = 'Angieland')
    try:
        app.start()
    except Exception as e:
        print(f"Server error: {e}")