## local imports
from quiggle.quiggle import main
from quiggle.server import server

if __name__ == '__main__':
    # main()
    app = server.QuiggleServer(name = 'Helium Rentals')
    try:
        app.start()
    except Exception as e:
        print(f"Server error: {e}")
    finally:
        app.stop()