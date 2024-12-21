''' /quiggle/server/router '''

## local imports
from .router import Router
from .folder import FolderRouter

RouterType = FolderRouter | Router

def not_set(key: str, filename: str):
    return Exception(f'Please set { key } in "{ filename }"')