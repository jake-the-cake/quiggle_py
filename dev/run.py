from config import settings
from data.json import to_json
# from server.start import Server
from server.server import Server_Connection

# app = start_server()
# app = Server()
app = Server_Connection('web')
# print(to_json(app))






# if settings.DEV_MODE == True:	app.use_dev_mode()