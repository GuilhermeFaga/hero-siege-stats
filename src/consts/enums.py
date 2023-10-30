from enum import Enum


class ConnectionError(Enum):
    NoInternet = 1
    ServerNotResponding = 2
    InterfaceNotFound = 3


class Sizes(Enum):
    Small = 'sm'
    Medium = 'md'
    Large = 'lg'


class Regions(str, Enum):
    ASIA = "Asia-Karponia"
    AMERICAS = "America-Mevius"
    EUROPE_1 = "Europe-Inoya"
    EUROPE_2 = "Europe-Damien"


class ItemSources(str, Enum):
    TO_STASH = "Item Added To Stash"
    TO_GROUND = "Item removed"
    FROM_STASH = "Item taken from Stash"
    FROM_GROUND = "Item Added!"
    NEW_ITEM = "Populated item drop table!"
