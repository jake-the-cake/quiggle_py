## local imports
from quiggle.server import server
from quiggle.cli.version import update_version

def cli():
    print('cli')
    update_version()

if __name__ == '__main__':
    app = server.QuiggleServer(name = 'Angieland')
    try:
        app.start()
    except Exception as e:
        print(f"Server error: {e}")