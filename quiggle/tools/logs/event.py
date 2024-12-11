## local imports
from quiggle.config.globals import QUIGGLE_DIR
from quiggle.tools.reader import Reader

## global imports
from datetime import datetime

FOLDER_PATH = QUIGGLE_DIR + '/logs/'
def timestamp_dict() -> dict:
    return { 'timestamp': datetime.now() }

class EventLog:
    
    def __init__(self, filename: str):
        self.file:      str = FOLDER_PATH + filename
        self.reader: Reader = Reader(self.file)
        self.entry:    dict = timestamp_dict()
    
    def add_property(self, key: str, value: str) -> None:
        self.entry[key] = value

    def use_log_message(self, key: str, prompt: str):
        message = input(prompt)
        self.add_property(key, message)