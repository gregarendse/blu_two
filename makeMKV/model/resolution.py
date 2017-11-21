class Resolution(object):
    x: int
    y: int

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def compare(self, other):
        if (type(self) != type(other)):
            raise Exception('Type mismatch')

        if self.y > other.y:
            return 1
        elif self.y == other.y:
            return 0
        elif self.y < other.y:
            return -1

