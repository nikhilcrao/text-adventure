class Item(object):
    def __init__(self, name: str, desc: str, price: int):
        self._name: str = name
        self._desc: str = desc
        self._price: int = price

    def __str__(self):
        return self.name()
    
    def name(self) -> str:
        return self._name
    
    def desc(self) -> str:
        return self._desc
    
    def price(self) -> int:
        return self._price
    

class Weapon(Item):
    def __init__(self, name: str, desc: str, price: int, damage: int):
        super().__init__(name, desc, price)
        self._damage: int = damage

    def damage(self) -> int:
        return self._damage
    
class Dagger(Weapon):
    def __init__(self):
        super().__init__(name="Dagger", desc="A dagger", price=5, damage=10)

class RustySword(Weapon):
    def __init__(self):
        super().__init__(name="Rusty Sword", desc="I would not touch this!", price=50, damage=20)

class Crossbow(Weapon):
    def __init__(self):
        super().__init__(name="Crossbow", desc="Pew Pew", price=95, damage=40)

class Consumable(Item):
    def __init__(self, name: str, desc: str, price: int, healing_value: int):
        super().__init__(name, desc, price)
        self._healing_value: int = healing_value

    def healing_value(self) -> int:
        return self._healing_value
    

class Bread(Consumable):
    def __init__(self):
        super().__init__(name="Bread", desc="Bread", price=10, healing_value=10)

class HealthPotion(Consumable):
    def __init__(self):
        super().__init__(name="Health Potion", desc="A potion to heal you.", price=40, healing_value=45)

class Poison(Consumable):
    def __init__(self):
        super().__init__(name="Worlds best potion.", desc="Nothing fishy here...", price=200, healing_value=-100)