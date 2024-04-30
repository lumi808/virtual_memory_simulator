from collections import OrderedDict

class TLB:
    def __init__(self, size):
        self.size = size
        self.entries = OrderedDict()
        self.hits = 0
        self.accesses = 0

    def access(self, page_num):
        self.accesses += 1

        if page_num not in self.entries:
            return None
        
        self.hits += 1
        frame_num = self.entries[page_num]
        return frame_num
        
    def load_page(self, page_num, frame_num):
        if len(self.entries) == self.size:
            self.entries.popitem(last=False)
        
        self.entries[page_num] = frame_num
    
    def evict_page(self):
        page_num_to_evict = None

        for page_num, frame in self.entries.items():
            if frame == 0:
                page_num_to_evict = page_num
            else:
                self.entries[page_num] -= 1
        if page_num_to_evict is not None:
            del self.entries[page_num_to_evict]

    def hit_rate(self):
        return self.hits / self.accesses * 100