## local imports
from .controller import HTTPServerController
from .socket import SocketController
from .prompts import MESSAGES
from quiggle.config import globals

## global imports
import socket
import threading
from typing import Callable, List, Tuple

mw_type = Callable[[socket.socket, Tuple[str, int]], None]
mw_list_type = List[mw_type]

class QuiggleServer:

    def __init__(self, host: str = globals.SERVER_HOST, port: int = globals.SERVER_PORT, name: str = None):
        ''' # set variables '''
        self.host          = host
        self.port          = port
        self.name          = name
        self.server_socket = SocketController(self.host, self.port)
        self.controller    = HTTPServerController(self.server_socket)

        ''' # MIDDLEWARE: need to impliment '''
        self.middlewares: mw_list_type = []

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
                client_socket, client_address = self.server_socket.accept_connections() or (None, None)
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
            self.http_handler(client_socket, client_address)
            for middleware in self.middlewares:
                middleware(client_socket, client_address)
        except Exception as e:
            print(f"Error handling connection from {client_address}: {e}")
        finally:
            client_socket.close()

    def use(self, middleware: mw_type):
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
    
    def http_handler(self, client_socket, client_address):
        """Middleware to handle HTTP requests."""
        try:
            data = client_socket.recv(1024).decode()
            if data:
                # Extract the request path (e.g., GET /favicon.ico)
                request_line = data.split("\r\n")[0]
                method, path, _ = request_line.split(" ")

                # Log only the first request from the client
                if path != "/favicon.ico":
                    print(f"HTTP Request from {client_address}: {request_line}")

                # Generate a response
                if path == "/favicon.ico":
                    # Send an empty response for favicon.ico requests
                    response = (
                        "HTTP/1.1 204 No Content\r\n"
                        "Connection: close\r\n\r\n"
                    )
                else:
                    response_body = "Hello, World!"
                    response = (
                        "HTTP/1.1 200 OK\r\n"
                        "Content-Type: text/plain\r\n"
                        f"Content-Length: {len(response_body)}\r\n"
                        "Connection: close\r\n\r\n"
                        f"{response_body}"
                    )
                client_socket.sendall(response.encode())
        except Exception as e:
            print(f"Error handling HTTP request: {e}")
        finally:
            client_socket.close()