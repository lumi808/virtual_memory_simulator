from collections import OrderedDict

from collections import OrderedDict

class PageTable:
    """
    Represents a page table for a virtual memory system.

    Attributes:
        num_pages (int): The total number of pages in the page table.
        table (OrderedDict): An ordered dictionary that maps page numbers to frame numbers.
    """

    def __init__(self, num_pages):
        """
        Initializes a new instance of the PageTable class.

        Args:
            num_pages (int): The total number of pages in the page table.
        """
        self.num_pages = num_pages
        self.table = OrderedDict()

    def access(self, page_num):
        """
        Retrieves the frame number associated with the given page number.

        Args:
            page_num (int): The page number to access.

        Returns:
            int: The frame number associated with the page number, or None if the page is not in the table.
        """
        if page_num not in self.table:
            return None

        frame_num = self.table[page_num]
        return frame_num
    
    def load_page(self, page_num, frame_num):
        """
        Loads a page into the page table.

        If the page table is full, the least recently used page will be evicted.

        Args:
            page_num (int): The page number to load.
            frame_num (int): The frame number to associate with the page.
        """
        if len(self.table) == self.num_pages:
            self.table.popitem(last=False)
        
        self.table[page_num] = frame_num
    
    def evict_page(self):
        """
        Evicts the least recently used page from the page table.

        If there are multiple pages with the same frame number, the frame numbers of the remaining pages will be decremented.
        """
        page_num_to_evict = None

        # Find the least recently used page and chagne the frame number of the remaining pages
        for page_num, frame_number in self.table.items():
            if frame_number == 0:
                page_num_to_evict = page_num
            else: 
                self.table[page_num] -= 1

        if page_num_to_evict is not None:
            del self.table[page_num_to_evict]