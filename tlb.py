from collections import OrderedDict

from collections import OrderedDict

from collections import OrderedDict

class TLB:
    """
    Translation Lookaside Buffer (TLB) class.

    Attributes:
        size (int): The maximum number of entries in the TLB.
        entries (OrderedDict): The TLB entries, where the key is the page number and the value is the frame number.
        hits (int): The number of TLB hits.
        accesses (int): The total number of TLB accesses.

    Methods:
        access(page_num): Accesses the TLB for the given page number and returns the corresponding frame number.
        load_page(page_num, frame_num): Loads a page into the TLB with the given page number and frame number.
        evict_page(): Evicts a page from the TLB.
        hit_rate(): Calculates the hit rate of the TLB.
    """

    def __init__(self, size):
        """
        Initializes a TLB object with the specified size.

        Args:
            size (int): The maximum number of entries in the TLB.
        """
        self.size = size
        self.entries = OrderedDict()
        self.hits = 0
        self.accesses = 0

    def access(self, page_num):
        """
        Accesses the TLB for the given page number and returns the corresponding frame number.

        Args:
            page_num (int): The page number to access.

        Returns:
            int: The frame number corresponding to the given page number, or None if the page number is not in the TLB.
        """
        self.accesses += 1

        if page_num not in self.entries:
            return None
        
        self.hits += 1
        frame_num = self.entries[page_num]
        return frame_num
        
    def load_page(self, page_num, frame_num):
        """
        Loads a page into the TLB with the given page number and frame number.

        If the TLB is already full, the least recently used page is evicted.

        Args:
            page_num (int): The page number to load.
            frame_num (int): The frame number corresponding to the page number.
        """
        if len(self.entries) == self.size:
            self.entries.popitem(last=False)
        
        self.entries[page_num] = frame_num
    
    def evict_page(self):
        """
        Evicts a page from the TLB.

        The page with frame number 0 is evicted first. If no such page exists, the frame numbers of all pages in the TLB are decremented by 1.
        """
        page_num_to_evict = None

        for page_num, frame in self.entries.items():
            if frame == 0:
                page_num_to_evict = page_num
            else:
                self.entries[page_num] -= 1
        if page_num_to_evict is not None:
            del self.entries[page_num_to_evict]

    def hit_rate(self):
        """
        Calculates the hit rate of the TLB.

        Returns:
            float: The hit rate of the TLB as a percentage.
        """
        return self.hits / self.accesses * 100