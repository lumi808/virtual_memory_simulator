class PageTable:
    def __init__(self, num_pages):
        self.num_pages = num_pages
        self.table = {}

    def access(self, page_num):
        if page_num not in self.table:
            return None

        frame_num = self.table[page_num]
        return frame_num