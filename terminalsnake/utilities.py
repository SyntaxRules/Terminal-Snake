
class Location(object):
    """
    A standard Data Object for holding things
    """

    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
