from collections import OrderedDict

class PageTable:
    def __init__(self, num_pages):
        self.num_pages = num_pages
        self.table = OrderedDict()

    def access(self, page_num):
        if page_num not in self.table:
            return None

        frame_num = self.table[page_num]
        return frame_num
    
    def load_page(self, page_num, frame_num):
        if len(self.table) == self.num_pages:
            self.table.popitem(last=False)
        
        self.table[page_num] = frame_num
    
    def evict_page(self):
        page_num_to_evict = None

        for page_num, frame_number in self.table.items():
            if frame_number == 0:
                page_num_to_evict = page_num
            else: 
                self.table[page_num] -= 1

        if page_num_to_evict is not None:
            del self.table[page_num_to_evict]