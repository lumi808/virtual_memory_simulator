class PageTable:
    def __init__(self, num_pages):
        self.num_pages = num_pages
        self.table = [None] * num_pages