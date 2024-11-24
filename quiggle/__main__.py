## local imports
from quiggle.quiggle import main
from quiggle.server import server

if __name__ == '__main__':
    # main()
    app = server.QuiggleServer(name = 'Angieland')
    try:
        app.start()
    except Exception as e:
        print(f"Server error: {e}")