def cli(): 
    from quiggle.cli import CliController
    CliController()

if __name__ == '__main__':
    from quiggle.server import server
    app = server.QuiggleServer(name = 'Angieland')
    app.start()