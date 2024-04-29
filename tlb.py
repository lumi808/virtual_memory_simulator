class TLB:
    def __init__(self, size):
        self.size = size
        self.entries = {}

    def access(self, page_num):
        if page_num not in self.entries:
            return None
        
        frame_num = self.entries[page_num]
        return frame_num
