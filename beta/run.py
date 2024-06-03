from config import settings
from data.json import to_json
from server.start import Server


# app = start_server()
app = Server()
print(to_json(app))






# if settings.DEV_MODE == True:	app.use_dev_mode()