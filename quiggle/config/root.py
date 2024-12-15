## local imports
from quiggle import __file__ as file
from quiggle.tools.logs.presets import infolog

## global imports
from pathlib import Path

def get_quiggle_dir() -> str:
    return Path(file)

def config_root(filename: str = 'config') -> str:
    paths: list = [
        f'/config.py',
        f'/{ filename }.py',
        f'/config/{ filename }.py',
        f'/quiggle/config/{ filename }.py'
    ]

    for path in paths:
        path = Path((str(Path.cwd())) + path)
        if path.exists():
            return path

    raise FileNotFoundError(infolog('Could not find a valid config file.'))