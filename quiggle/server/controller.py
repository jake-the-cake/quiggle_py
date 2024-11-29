## local imports
from .request import Request
from .response import HTMLResponse
from quiggle.tools.logs.presets import errorlog, infolog, labellog

class HTTPServerController:
    def __init__(self):
        self.request: Request | None = None
        self.response                = None

    ''' Parse request data. '''
    def handle_request(self, client_socket, client_address):
        self.client_address = client_address
        self.client_socket  = client_socket
        print(f"New connection from {self.client_address}")
        try:
            data = self.client_socket.recv(1024).decode()
            if data:
                self.request = Request(data)
                print(infolog(f'REQUEST <-- { self.client_address[0] }:'), self.request.method, self.request.path)
        except Exception as e:
            print(errorlog(f'Error handling request from { self.client_address[0] }:'), e)

    ''' Generate an http response. '''
    def generate_response(self):
        self.response = HTMLResponse(self.client_socket)
        print(labellog(
            f'RESPONSE -> { self.client_address[0] }:'),
            self.response.status_code,
            self.response.STATUS_MESSAGES[self.response.status_code] or 'Unknown'
        )

    ''' Send final response over. '''
    def send(self):
        self.response.send()
