from server.server import Web_Server
import logging

logging.basicConfig(level=logging.ERROR)

app = Web_Server('web')
app.receive_request()