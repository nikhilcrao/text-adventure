import random

from .inventory import Inventory
from .items import RustySword
from .actions import Action

class NonPlayableCharacter(object):
    def __init__(self, name: str):
        self._name: str = name

    def name(self) -> str:
        return self._name

    def get_actions(self) -> dict[str, str]:
        return {}

class TraderBase(object):
    def __init__(self, bananas: int, inventory: Inventory):
        self._bananas: bananas
        self._inventory: inventory


TRADER_ITEM_PROB = {
    RustySword: 0.5,
}

class Trader(NonPlayableCharacter, TraderBase):
    def __init__(self):
        super().__init__(name="Trader")
        self._bananas = random.randint(80, 100)
        self._inventory = Inventory()
        self.generate_inventory()

    def inventory(self):
        return self._inventory

    def generate_inventory(self):
        for item in TRADER_ITEM_PROB:
            if random.random() < TRADER_ITEM_PROB[item]:
                self._inventory.add_item(item())

    def greet_text(self) -> str:
        return "Hello, I'm a trader!"
    
    def get_actions(self, player_inventory: Inventory) -> list[Action]:
        actions = {"q": "Quit"}
        counter = 1
        for item in self.inventory().items():
            actions.update({"{}. Buy {} for {} bananas"}.format(counter, item.name(), item.price()))
        for item in player_inventory.items():
            actions.update({"{}. Sell {} for {} bananas"}.format(counter, item.name(), item.price()))
        return actions