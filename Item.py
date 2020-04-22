class Item:
    def __init__(self, x, y, t):
        self.type = t
        self.x = x
        self.y = y

    def delete(self, l):
        try:
            l.remove(self)
            return l
        except ValueError:
            return l
        finally:
            del self
