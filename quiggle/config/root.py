## local imports
from quiggle import __file__ as file
from quiggle.tools.logs.presets import infolog

## global imports
from pathlib import Path

def get_quiggle_dir() -> str:
    return '/' + str(Path(file)).strip('/__init__.py')

def read_local_file_variables(filename: str):
	with open(filename) as file:
		data = {}
		exec(file.read(), data)
		return data

def config_root(filename: str = 'config') -> str:
    paths: list = [
        f'/config/{ filename }.py',
        f'/{ filename }/config.py',
        f'/quiggle/config/{ filename }.py',
        '/config.py'
    ]

    for path in paths:
        path = Path.cwd() / path[1:]
        if path.exists():
            return path

    raise FileNotFoundError(infolog('Could not find a valid config file.'))

def get_config(root: str = 'config') -> dict:
     config_file = config_root(root)
     dictionary = read_local_file_variables(config_file)
     dictionary['filename'] = config_file
     return dictionary