from config import settings
from data.json import to_json
from server.server import Web_Server

# from routing.router import WebRouter

# app = Server_Connection('web')
app = Web_Server('web')
app.receive_request()