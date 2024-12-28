## local imports
from quiggle.server import server
from quiggle.tools.logs.presets import errorlog

if __name__ == '__main__':
    app = server.QuiggleServer(name = 'My Server', port = 6047)
    try:
        app.start()
    except Exception as e:
        print(errorlog(f"Server error: {e}"))