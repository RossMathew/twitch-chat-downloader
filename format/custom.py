from .format import Format


class Custom(Format):
    def __init__(self, name: str):
        super().__init__()
        self.name: str = name

    def use(self):
        pass
