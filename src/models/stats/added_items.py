from src.models.messages.added_item import AddedItemObject

from src.consts.sets import ItemsRarity


class AddedItemsStats:
    added_items = {}
    items_per_hour = {}

    def __init__(self):
        for rarity_id in ItemsRarity:
            self.added_items[ItemsRarity[rarity_id]] = {
                'mf': 0,
                'total': 0
            }
            self.items_per_hour[ItemsRarity[rarity_id]] = 0

    def update(self, added_item_object: AddedItemObject | None = None, items_per_hour: dict | None = None):
        if added_item_object is not None:
            self.added_items[ItemsRarity[str(added_item_object.rarity)]
                             ]['total'] += 1
            if added_item_object.mf_drop == 1:
                self.added_items[ItemsRarity[str(
                    added_item_object.rarity)]]['mf'] += 1

        if items_per_hour is not None:
            self.items_per_hour = items_per_hour
