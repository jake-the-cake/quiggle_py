## local imports
from quiggle.config import globals

## global imports
import socket
import threading

class SocketController:

    def __init__(self, host=globals.SERVER_HOST, port=globals.SERVER_PORT):
        self.host          = host
        self.port          = port
        self.server_socket = None

    def start_socket(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)

    def accept_connections(self):
        """Accept and handle incoming connections."""
        while True:
            try:
                client_socket, client_address = self.server_socket.accept()
                return client_socket, client_address
            except Exception as e:
                print(f"Error accepting connections: {e}")

    def close_socket(self):
        if self.server_socket:
            self.server_socket.close()
            print("Socket closed")
