## local imports
from quiggle.config.globals import QUIGGLE_DIR

FOLDER_PATH = QUIGGLE_DIR + '/logs/'

class EventLog:
    
    def __init__(self, filename: str):
        self.file = FOLDER_PATH + filename
        print(self.file)