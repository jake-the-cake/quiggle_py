## global imports
from typing import (
	Callable,
	List,
	Tuple
)
import socket

ClientAddressType = Tuple[str, int]
ClientSocketType = socket.socket

SocketAddressType = Tuple[ClientSocketType, ClientAddressType]

MiddlewareType = Callable[[ClientSocketType, ClientAddressType], None]
MiddlewareListType = List[MiddlewareType]