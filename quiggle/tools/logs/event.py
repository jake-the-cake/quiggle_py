## local imports
from quiggle.tools.reader import Reader

## global imports
from datetime import datetime
from pathlib import Path
import json

cwd = Path.cwd()
LOG_FOLDER = cwd / 'logs'


def timestamp_dict() -> dict:
    return { 'timestamp': datetime.now() }

class EventLog:
    
    def __init__(self, filename: str):
        self.file:      str = LOG_FOLDER / filename
        self.reader: Reader = Reader(self.file)
        self.entry:    dict = timestamp_dict()
    
    def add_property(self, key: str, value: str) -> None:
        self.entry[key] = value

    def use_log_message(self, key: str, prompt: str):
        message = input(prompt)
        self.add_property(key, message)

    def get_json_data(self):
        self.reader.get_json()
        return self

    def serialize_datetime(self):
        self.entry['timestamp'] = self.entry['timestamp'].strftime('%Y.%m.%d[%H:%M:%S]')
    
    def to_json(self):
        self.serialize_datetime()
        self.reader.updated_data = json.dumps(self.reader.updated_data)

    def add_entry(self):
        self.reader.updated_data['data'].append(self.entry)

    def write(self):
        self.to_json()
        self.reader.write('data')