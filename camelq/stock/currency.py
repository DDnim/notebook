
class item():
    def __init__(self, code = '', name = ''):
        self._price = 0
        self._size = 1
        self.code = code
        self.name = name
        self.value = dict()

    def refresh(self, time = '1980-01-01', price = 0):
        self._price = price
        self.value[time] = price

    @property
    def price(self):
        return None

    @price.setter
    def price(self, v):
        self._price = v

    @price.getter
    def price(self):
        return self._price * self._size

    @property
    def size(self):
        return None

    @size.setter
    def size(self, v):
        self._size = v

    @size.getter
    def size(self):
        return self._size