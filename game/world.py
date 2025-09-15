from .player import Player
from .enemies import Enemy, get_enemy
from .npc import Trader
from .actions import Action


class MapTile(object):
    def __init__(self, intro_text: str):
        self._intro_text: str = intro_text

    def __repr__(self):
        return "Room: intro_text={}".format(self._intro_text)

    def intro_text(self) -> str:
        return self._intro_text
    
    def modify_player(self, player: Player):
        pass

    def enemy(self) -> Enemy | None:
        return None

    def trader(self) -> Trader | None:
        return None


class EnemyTile(MapTile):
    def __init__(self):
        super().__init__(intro_text="This is an enemy tile!")
        self._enemy = get_enemy()

    def enemy(self) -> Enemy | None:
        return self._enemy
    
    def modify_player(self, player: Player):
        if self.enemy() and self.enemy().alive():
            player.handle_attack(self.enemy().damage())


class VictoryTile(MapTile):
    def __init__(self):
        super().__init__(intro_text="This is a victory tile!")


class TraderTile(MapTile):
    def __init__(self):
        super().__init__(intro_text="This is a trader tile!")
        self._trader: Trader = Trader()

    def trader(self) -> Trader | None:
        return self._trader


class StartTile(MapTile):
    def __init__(self):
        super().__init__(intro_text="This is the start tile!")


class BoringTile(MapTile):
    def __init__(self):
        super().__init__(intro_text="This is a boring tile!")


class RewardTile(MapTile):
    def __init__(self):
        super().__init__(intro_text="This is a reward tile!")

class Orangutan(MapTile):
    def __init__(self):
        super().__init__(intro_text="Look an Orangutan")


WORLD_DSL: str = """\
|ST|OT|EN|
|EN|  |BO|
|TR|VT|RW|
"""

WORLD_DSP_MAP: dict[str, MapTile] = {
    "ST": StartTile,
    "BO": BoringTile,
    "EN": EnemyTile,
    "RW": RewardTile,
    "TR": TraderTile,
    "VT": VictoryTile,
    "OT": Orangutan,
}


class World(object):
    def __init__(self, world_dsl: str = WORLD_DSL):
        self._map: list[list[MapTile]] = []
        self._start_x: int = -1
        self._start_y: int = -1
        self._init(world_dsl)

    def __repr__(self):
        return "World: len(map.rows)={} len(map.cols)={} start_row={} start_col={}".format(
            len(self._map),
            len(self._map[0]),
            self._start_x,
            self._start_y,
        )
    
    def _init(self, world_dsl: str):
        for row_idx, row_dsl in enumerate(world_dsl.splitlines()):
            row = []
            parts = row_dsl.split("|")
            for col_idx, col_dsl in enumerate(parts):
                # skip the first and last elements as they are empty values.
                if (col_idx == 0) or (col_idx == (len(parts) - 1)):
                    continue
                tile_type = WORLD_DSP_MAP.get(col_dsl)
                if tile_type:
                    row.append(tile_type())
                    if col_dsl == "ST":
                        self._start_x = row_idx
                        self._start_y = (col_idx - 1)
                else:
                    row.append(None)
            self._map.append(row)

    def start_pos(self) -> tuple[int, int]:
        return (self._start_x, self._start_y)

    def room(self, x: int, y: int) -> MapTile | None:
        if x < 0 or x >= len(self._map):
            return None
        if y < 0 or y >= len(self._map[0]):
            return None
        return self._map[x][y]

    def get_trade_actions(self, player: Player) -> list[Action]:
        return []
    
    def get_move_actions(self, player: Player) -> list[Action]:
        actions = []
        x_pos, y_pos = player.pos()

        if self.room(x_pos, y_pos - 1):
            actions.append(
                Action("n", "Go North", lambda: player.set_pos(x_pos, y_pos - 1))
            )
        if self.room(x_pos, y_pos + 1):
            actions.append(
                Action("s", "Go South", lambda: player.set_pos(x_pos, y_pos + 1))
            )
        if self.room(x_pos + 1, y_pos):
            actions.append(
                Action("e", "Go East", lambda: player.set_pos(x_pos + 1, y_pos))
            )
        if self.room(x_pos - 1, y_pos):
            actions.append(
                Action("w", "Go West", lambda: player.set_pos(x_pos - 1, y_pos))
            )
        
        return actions