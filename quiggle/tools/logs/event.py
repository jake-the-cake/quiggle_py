## local imports
from quiggle.config.globals import QUIGGLE_DIR
from quiggle.tools.reader import Reader

## global imports
from datetime import datetime
import json

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

    def get_original_data(self):
        self.reader.get_json()

    def to_dict(self):
        self.reader.updated_data = json.dumps(self.reader.original_data)
        if self.reader.updated_data == '""':
            self.reader.updated_data = json.dumps([])
        json.load(self.reader.updated_data)
        print(self.reader.original_data)
        print(self.reader.updated_data)

    def to_json(self):
        self.reader.updated_data = json.dumps(self.reader.updated_data)

    def add_entry(self):
        self.reader.updated_data.append(self.entry)

    def write(self):
        self.to_json()
        self.reader.write('data')