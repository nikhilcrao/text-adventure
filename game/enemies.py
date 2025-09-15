import random

from .items import Item

class AttackerBase(object):
    def __init__(self, hp: int, damage: int):
        self._hp: int = hp
        self._damage: int = damage

    def alive(self) -> bool:
        return self._hp > 0
    
    def handle_attack(self, attack_damage: int):
        self._hp -= min(self._hp, attack_damage)

    def damage(self):
        return self._damage
    
    def hp(self):
        return self._hp


class Enemy(AttackerBase):
    def __init__(self, name: str, hp: int, damage: int, alive_text: str, dead_text: str):
        super().__init__(hp, damage)
        self._name: str = name
        self._alive_text: str = alive_text
        self._dead_text: str = dead_text

    def __repr__(self):
        return "Enemy: name={} hp={} damage={} alive_text={} dead_text={}".format(
            self._name, self._hp, self._damage, self._alive_text, self._dead_text)

    def alive_text(self) -> str:
        return self._alive_text

    def dead_text(self) -> str:
        return self._dead_text

    def drop(self) -> Item | None:
        return None


class Fullion(Enemy):
    def __init__(self):
        super().__init__(name="Fullion", hp=20, damage=5, alive_text="A Fullion Stands in front of you, it's tusks are ready to bite!", dead_text="The Fullion rots on the ground")


class Troll(Enemy):
    def __init__(self):
        super().__init__(name="Troll", hp=30, damage=10, alive_text="A Troll stands in front of you and blocks you're path", dead_text="The Troll lies on the !")


class Anaconda(Enemy):
    def __init__(self):
        super().__init__(name="Anaconda", hp=40, damage=5, alive_text="Snakey! Awww...", dead_text="Snakey! Nooo...")


class Giant(Enemy):
    def __init__(self):
        super().__init__(name="Giant", hp=60, damage=15, alive_text="So big?", dead_text="Small when dead...")


def get_enemy() -> Enemy:
    enemy_class = random.choices(
        [
            Fullion,
            Troll,
            Anaconda,
            Giant,
        ],
        weights=[
            0.6,
            0.25,
            0.1,
            0.05,
        ],
        k = 1
    )
    return enemy_class[0]()