from .items import Item

class Inventory(object):
    def __init__(self, items=[]):
        self._items: list[Item] = items

    def items(self) -> list[Item]:
        return self._items

    def add_item(self, item: Item):
        if item in self._items:
            raise Exception("{} already exists".format(item))
        self._items.append(item)

    def remove_item(self, item: Item):
        if item not in self._items:
            raise IndexError("{} not found".format(item))
        self._items.remove(item)