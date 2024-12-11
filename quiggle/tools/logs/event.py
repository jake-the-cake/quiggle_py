## local imports
from quiggle.config.globals import QUIGGLE_DIR
from quiggle.tools.reader import Reader

## global imports
from datetime import datetime

FOLDER_PATH = QUIGGLE_DIR + '/logs/'

class EventLog:
    
    def __init__(self, filename: str):
        self.file:   str    = FOLDER_PATH + filename
        self.reader: Reader = Reader(self.file)
        self.entry: dict    = {
            'timestamp': datetime.now()
        }
    
    def add_property(self, name: str, value: str) -> None:
        self.entry[name] = value