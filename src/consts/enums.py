from enum import Enum


class ConnectionError(Enum):
    NoInternet = 1
    ServerNotResponding = 2
    InterfaceNotFound = 3


class Sizes(Enum):
    Small = 'sm'
    Medium = 'md'
    Large = 'lg'
    XLarge = 'xl'


class Regions(str, Enum):
    ASIA = "Asia-Karponia"
    AMERICAS = "America-Mevius"
    EUROPE_1 = "Europe-Inoya"
    EUROPE_2 = "Europe-Damien"
