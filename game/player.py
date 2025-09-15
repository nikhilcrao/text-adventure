from .inventory import Inventory
from .items import Weapon, Consumable, Dagger, HealthPotion
from .actions import Action
from .enemies import AttackerBase


class Player(AttackerBase):
    MAX_HP: int = 105

    def __init__(self, start_pos: tuple[int, int]):
        super().__init__(Player.MAX_HP, 0)
        self._x: int = start_pos[0]
        self._y: int = start_pos[1]
        self._bananas: int = 0
        self._inventory: Inventory = Inventory(items=[Dagger(), HealthPotion()])

    def __repr__(self):
        return "Player: pos=({}, {}) hp={} bananas={} damage={} inventory={}".format(
            self._x,
            self._y,
            self._bananas,
            self.hp(),
            self.damage(),
            self._inventory,
        )

    def x(self) -> int:
        return self._x
    
    def y(self) -> int:
        return self._y
    
    def inventory(self) -> Inventory:
        return self._inventory
    
    def set_pos(self, x_pos: int, y_pos: int):
        self._x = x_pos
        self._y = y_pos
    
    def pos(self) -> tuple[int, int]:
        return (self._x, self._y)
    
    def damage(self) -> int:
        max_damage = 0
        for item in self.inventory().items():
            if isinstance(item, Weapon):
                max_damage = max(max_damage, item.damage())
        return max_damage
    
    def consume(self, item: Consumable):
        self._hp += item.healing_value()

    def get_heal_actions(self) -> list[Action]:
        actions = []
        counter = 0
        for item in self.inventory().items():
            if isinstance(item, Consumable):
                counter += 1
                actions.append(
                    Action(str(counter), item.name(), lambda: self.consume(item))
                )
        return actions