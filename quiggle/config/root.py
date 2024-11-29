## local imports
import quiggle

## global imports
import os

def get_root_dir():
    return os.path.dirname(quiggle.__file__)

root_dir = get_root_dir()