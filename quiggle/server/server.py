## local imports
from .controller import HTTPServerController
from .socket import SocketController
from .prompts import MESSAGES
from quiggle.config import globals

## global imports
import socket
import threading
from typing import Callable, List, Tuple


class QuiggleServer:

    def __init__(self, host: str = globals.SERVER_HOST, port: int = globals.SERVER_PORT, name: str = None):
        ''' # set variables '''
        self.host          = host
        self.port          = port
        self.name          = name
        self.server_socket = SocketController(self.host, self.port)
        self.controller    = HTTPServerController(self.server_socket)

        ''' # MIDDLEWARE: need to impliment '''
        self.middlewares: List[Callable[[socket.socket, Tuple[str, int]], None]] = []

    def start(self):
        ''' 
            Start the socket server and accept connections
        '''
        self.server_socket.start_socket()
        print(MESSAGES['connected'](self.host, self.port, self.name))
        self._accept_connections()

    def _accept_connections(self):
        """Accept and handle incoming connections."""
        try:
            while True:
                client_socket, client_address = self.server_socket.accept_connections(self)
                print(f"New connection from {client_address}")
                threading.Thread(
                    target=self._handle_connection, args=(client_socket, client_address)
                ).start()
        except KeyboardInterrupt:
            print("Shutting down server...")
            self.stop()

    def _handle_connection(self, client_socket: socket.socket, client_address: Tuple[str, int]):
        """Handles a single connection."""
        try:
            for middleware in self.middlewares:
                middleware(client_socket, client_address)
        except Exception as e:
            print(f"Error handling connection from {client_address}: {e}")
        finally:
            client_socket.close()

    def use(self, middleware: Callable[[socket.socket, Tuple[str, int]], None]):
        '''
            Allows the user to bind middleware to the server.
            Middleware is a callable that takes (client_socket, client_address).
        '''
        self.middlewares.append(middleware)
        print(f"Middleware added: {middleware.__name__}")

    def stop(self):
        """Stops the server and closes the socket."""
        if self.server_socket:
            self.server_socket.close_socket()
            print("Server stopped")

    def handle_request(self, sock, addr):
        print(sock, addr)



# if __name__ == "__main__":
    # app = QuiggleServer(name='Helium Rentals')
    # print(app)
    # Initialize controllers
    # socket_controller = SocketController()
    # http_server = HTTPServerController()

    # Start the socket
    # socket_controller.start_socket()

    # # Define a connection handler
    # def connection_handler(client_socket, client_address):
    #     http_server.handle_request(client_socket, client_address)

    # # Accept connections
    # try:
    #     socket_controller.accept_connections(connection_handler)
    # except KeyboardInterrupt:
    #     print("Shutting down server...")
    # finally:
    #     socket_controller.server_socket.close()