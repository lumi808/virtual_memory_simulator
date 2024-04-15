from tlb import TLB
from page_table import PageTable

class VirtualMemory:
    def __init__(self, page_size, num_pages, num_frames, tlb_size):
        self.page_size = page_size
        self.num_pages = num_pages
        self.num_frames = num_frames
        self.tlb_size = tlb_size

        self.page_table = PageTable(num_pages)
        self.tlb = TLB(tlb_size)