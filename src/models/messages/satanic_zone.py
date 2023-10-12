
class SatanicZoneMessage:
    status: str
    message: str
    satanic_zone_name: str

    def __init__(self, msg_dict: dict):
        self.status = msg_dict['status']
        self.message = msg_dict['message']
        self.satanic_zone_name = msg_dict['satanicZoneName']
