from typing import Callable

class Action(object):
    def __init__(self, key: str, desc: str, handler: Callable[[], None]):
        self._key: str = key
        self._desc: str = desc
        self._handler: Callable[[], None] = handler

    def key(self) -> str:
        return self._key

    def desc(self) -> str:
        return self._desc
    
    def handler(self) -> Callable[[], None]:
        return self._handler
    
    def run(self):
        handler = self.handler()
        handler()