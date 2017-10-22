class AspectRatio(object):
    x: int
    y: int

    def __init__(self, x=0, y=0, input=None):
        if input != None and type(input) == str:
            (self.x, self.y) = input.split(':')
        else:
            self.x = x
            self.y = y