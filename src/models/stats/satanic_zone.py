from src.models.messages.satanic_zone import SzInfo


class SatanicZoneStats:
    satanic_zone_info: SzInfo


    def __init__(self, satanic_zone_info=None):
        self.satanic_zone_info = satanic_zone_info

    def update(self, satanic_zone_info: SzInfo | None = None):
        if satanic_zone_info is not None:
            self.satanic_zone_info = satanic_zone_info

