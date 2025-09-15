class Buffer(object):
    def __init__(self):
        self._buf: list[str] = []
    
    def console(self) -> str:
        return "{}\n".format("\n".join(self._buf))

    def print(self, text: str):
        self._buf.append(text)

    def clear(self):
        self._buf = []