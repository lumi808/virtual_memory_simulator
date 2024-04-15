class TLB:
    def __init__(self, size):
        self.size = size
        self.entries = [None] * size