## local imports
from quiggle.server import config
from quiggle.server.prompts import MESSAGES
from quiggle.tools.printer import Printer
from quiggle.types.server import SocketAddressType, ClientSocketType
from quiggle.server.controllers.connection import ConnectionLogger

## global imports
import socket
import psutil  # To detect processes using the port

class SocketController:
    """
    SocketController manages and controls socket-based communication for the QuiggleServer.
    It handles:
      - HTTP requests
      - WebSocket connections
      - Port management and connection lifecycle
    """

    def __init__(self, host: str = config.SERVER_HOST, port: int = config.SERVER_PORT):
        """
        Initialize the SocketController.

        :param host: Host address to bind the socket (default from config).
        :param port: Port number to bind the socket (default from config).
        """
        self.host: str = host
        self.port: int = port
        self.server_socket: ClientSocketType = None

    def create_socket(self) -> None:
        """
        Create a new socket instance using IPv4 and TCP protocols.
        """
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def check_and_kill_port(self) -> None:
        """
        Check if the requested port is in use. If so, attempt to terminate the process using it.

        Raises:
            RuntimeError: If unable to terminate or identify the process on the port.
        """
        for conn in psutil.net_connections(kind='inet'):
            if conn.laddr.port == self.port and conn.status == 'LISTEN':
                try:
                    process = psutil.Process(conn.pid)
                    if 'http' in process.name().lower() or 'socket' in process.name().lower():
                        process.terminate()
                        process.wait(timeout=5)
                        Printer(f"Terminated process '{process.name()}' using port {self.port}.").line('note')
                        return
                    else:
                        raise RuntimeError(
                            f"Port {self.port} is in use by {process.name()} (PID {process.pid}) and cannot be terminated."
                        )
                except (psutil.AccessDenied, psutil.NoSuchProcess) as e:
                    raise RuntimeError(
                        f"Unable to access or terminate the process on port {self.port}: {str(e)}"
                    )
        Printer(f"Port {self.port} is not in use or could not be resolved.").line('note')

    def start_socket(self) -> None:
        """
        Start the socket server. If the requested port is unavailable, attempt to resolve it.

        Raises:
            RuntimeError: If unable to bind the socket after resolving port issues.
        """
        attempt = 0
        while attempt < 2:  # Retry once after killing a potential conflict
            try:
                self.create_socket()
                self.server_socket.bind((self.host, self.port))
                self.server_socket.listen(5)
                Printer(f"Socket server started on {self.host}:{self.port}").line('note')
                return
            except socket.error as e:
                Printer(f"Error starting socket on port {self.port}: {e}").line('error')
                if attempt == 0:
                    self.check_and_kill_port()  # Attempt to resolve the conflict
                else:
                    raise RuntimeError(
                        f"Failed to start socket server on {self.host}:{self.port}. Details: {e}"
                    )
            finally:
                attempt += 1

    def accept_connections(self) -> None | SocketAddressType:
        """
        Accept incoming connections and return the client socket and address.

        :return: A tuple (client_socket, client_address) if a connection is established.
        """
        try:
            client_socket, client_address = self.server_socket.accept()
            Printer(f"Accepted connection from {client_address}").line('note')
            return client_socket, client_address
        except Exception as e:
            Printer(f"Error accepting connections: {str(e)}").line('error')
            return None

    def close_socket(self) -> None:
        """
        Close the server socket and release the bound port.
        """
        if self.server_socket:
            self.server_socket.close()
            self.server_socket = None
            Printer(MESSAGES['closed'](self.__class__.__name__)).line('note')