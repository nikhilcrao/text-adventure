import random
import pickle
from enum import Enum

from utils.buffer import Buffer

from .player import Player
from .world import World
from .actions import Action


class MenuState:
    ROOT = 0
    TRADER = 1
    HEAL = 2


class Engine(object):
    def __init__(self):
        self._id: str = random.randbytes(16)
        self._world: World = World()
        self._player: Player = Player(self.world().start_pos())
        self._buffer: Buffer = Buffer()
        self._menu: MenuState = MenuState.ROOT

    def id(self) -> str:
        return self._id

    def save(self) -> bytearray:
        return pickle.dumps(self)

    def buffer(self) -> Buffer:
        return self._buffer
    
    def world(self) -> World:
        return self._world

    def player(self) -> Player:
        return self._player
    
    def menu(self) -> MenuState:
        return self._menu
    
    def set_menu(self, state: MenuState):
        self._menu = state

    def get_actions(self) -> list[Action]:
        if self.menu() == MenuState.HEAL:
            actions = self.player().get_heal_actions()
            actions.append(
                Action("q", "Quit", lambda: self.set_menu(MenuState.ROOT))
            )
            return actions
        
        if self.menu() == MenuState.TRADER:
            actions = self.world().get_trade_actions(self.player())
            actions.append(
                Action("q", "Quit", lambda: self.set_menu(MenuState.ROOT))
            )
            return actions
        
        x_pos, y_pos = self.player().pos()
        room = self.world().room(x_pos, y_pos)
        assert(room)

        actions = []

        if room.enemy() and room.enemy().alive():
            def handle_attack():
                room.enemy().handle_attack(self.player().damage())
                room.modify_player(self.player())
            actions.append(Action("a", "Attack", handle_attack))
        else:
            move_actions = self.world().get_move_actions(self.player())
            actions.extend(move_actions)

        if room.trader():
            actions.append(
                Action("t", "Trade", lambda: self.set_menu(MenuState.TRADER))
            )

        if self.player().hp() < Player.MAX_HP:
            actions.append(
                Action("h", "Heal", lambda: self.set_menu(MenuState.HEAL))
            )

        return actions
    
    def handle_input(self, input: str) -> bool:
        actions = self.get_actions()
        for action in actions:
            if action.key() == input:
                handler = action.handler()
                handler()
                return True
        return False


def init_engine(save_bytes: bytearray) -> Engine:
    return pickle.loads(save_bytes)