class Rectangle:
    def __init__(self, l, b):

        if not isinstance(l, int) or not isinstance(b, int):
            raise ValueError("Length and Breadth must be numbers")

        self.l = l
        self.b = b

    def __iter__(self):
        yield {"length": self.l}

        yield {"width": self.b}
