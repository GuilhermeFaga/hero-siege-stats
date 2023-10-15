from enum import Enum


class ConnectionError(Enum):
    NoInternet = 1
    ServerNotResponding = 2
    InterfaceNotFound = 3
