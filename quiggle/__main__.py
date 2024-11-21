## local imports
from quiggle.quiggle import main
from quiggle.server import server

if __name__ == '__main__':
    main()
    app = server.QuiggleServer()
    print(app)