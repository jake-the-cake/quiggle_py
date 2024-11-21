import io

class HTTPServerController:
    def __init__(self, socket_controller):
        self.socket_controller = socket_controller

    def handle_request(self, client_socket, client_address):
        try:
            data = client_socket.recv(1024).decode()
            if data:
                print(f"Received request from {client_address}:\n{data}")
                response = self.generate_response(data)
                client_socket.sendall(response)
        except Exception as e:
            print(f"Error handling request from {client_address}: {e}")
        finally:
            client_socket.close()

    def generate_response(self, request_data):
        """Generate a simple HTTP response."""
        response_body = "Welcome to Quiggle Server!"
        response_headers = {
            "Content-Type": "text/plain",
            "Content-Length": len(response_body),
            "Connection": "close",
        }
        response_header_string = "\r\n".join(f"{key}: {value}" for key, value in response_headers.items())
        response = f"HTTP/1.1 200 OK\r\n{response_header_string}\r\n\r\n{response_body}"
        return response.encode()