from tlb import TLB
from page_table import PageTable
import math
from collections import deque, OrderedDict

class VirtualMemory:
    def __init__(self, program_address_space, page_size, num_pages, num_frames, tlb_size):
        """
        Initializes a VirtualMemory object.

        Args:
            program_address_space (int): The size of the program's address space.
            page_size (int): The size of each page in the virtual memory.
            num_pages (int): The total number of pages in the virtual memory.
            num_frames (int): The total number of frames in the physical memory.
            tlb_size (int): The size of the Translation Lookaside Buffer (TLB).

        Attributes:
            program_address_space (int): The size of the program's address space.
            page_size (int): The size of each page in the virtual memory.
            num_pages (int): The total number of pages in the virtual memory.
            num_frames (int): The total number of frames in the physical memory.
            tlb_size (int): The size of the Translation Lookaside Buffer (TLB).
            disk_file (file): The file object representing the disk simulation.
            page_table (PageTable): The page table for mapping virtual addresses to physical addresses.
            tlb (TLB): The Translation Lookaside Buffer for caching page translations.
            physical_memory (deque): The physical memory frames.
            accesses (int): The total number of memory accesses.
            page_faults (int): The total number of page faults.
            logs (list): The list of log entries.

        Returns:
            None
        """
        self.program_address_space = program_address_space
        self.page_size = page_size
        self.num_pages = num_pages
        self.num_frames = num_frames
        self.tlb_size = tlb_size
        self.disk_file = open('disk_sim', 'rb')

        self.page_table = PageTable(num_pages)
        self.tlb = TLB(tlb_size)
        self.physical_memory = deque(maxlen=num_frames)
        
        self.accesses = 0
        self.page_faults = 0
        self.logs = []
    def translate_address_from_file(self, file_name):
            """
            Translates virtual addresses from a file and logs system information.

            Args:
                file_name (str): The name of the file containing virtual addresses.

            Returns:
                None
            """
            with open(file_name, 'r') as file:
                for line in file:
                    virtual_address_decimal = int(line)
                    self.translate_address(virtual_address_decimal)
            self.log_system_info()

    def get_page_num_offset(self, virtual_address_binary):
        """
        Extracts the page number and offset from a given virtual address.

        Args:
            virtual_address_binary (str): The binary representation of the virtual address.

        Returns:
            tuple: A tuple containing the page number and page offset.

        """
        page_num_bits = int(math.log(self.page_size, 2))
        page_num = virtual_address_binary[:page_num_bits+1]

        offset_bits = self.program_address_space - page_num_bits
        page_offset = virtual_address_binary[offset_bits:]

        return page_num, page_offset

    def translate_address(self, virtual_address_decimal):
        """
        Translates a virtual address to a physical address and retrieves the corresponding data.

        Args:
            virtual_address_decimal (int): The virtual address to be translated.

        Returns:
            tuple: A tuple containing the physical address and the corresponding data.

        Raises:
            None

        """
        self.accesses += 1

        virtual_address_binary = bin(virtual_address_decimal)[2:].zfill(self.program_address_space)

        page_num, page_offset = self.get_page_num_offset(virtual_address_binary)

        # try to find the frame number in the TLB
        frame_num = self.tlb.access(page_num)

        # if the frame number is not in the TLB, try to find it in the page table
        if frame_num is None:
            frame_num = self.page_table.access(page_num)
        
        # if the frame number is not in the page table, trigger a page fault
        if frame_num is None:
            self.page_faults += 1
            frame_num = self.page_fault(page_num)
        
        physical_address = frame_num * self.page_size + int(page_offset, 2)
        data = self.physical_memory[frame_num]

        # log the virtual address, physical address, and data
        self.logs.append(f"Virtual address: {bin(virtual_address_decimal)[2:]}, Physical address: { bin(physical_address)[2:]}, Value: {int.from_bytes(data, byteorder='big')}")

        return physical_address, data

    def page_fault(self, page_num):
        """
        Handles a page fault by loading the page data from disk and returning the frame number.

        Args:
            page_num (str): The page number in binary format.

        Returns:
            int: The frame number where the page data is loaded.
        """
        self.disk_file.seek(int(page_num, 2) * self.page_size)
        page_data_binary = self.disk_file.read(self.page_size)

        frame_num = self.load_page_data(page_num, page_data_binary)
        
        return frame_num
    
    def load_page_data(self, page_num, page_data_binary):
        """
        Loads the given page data into the physical memory.

        Args:
            page_num (int): The page number of the page data.
            page_data_binary (str): The binary representation of the page data.

        Returns:
            int: The frame number where the page data is loaded.
        """

        # if the physical memory is full, evict a page
        if len(self.physical_memory) == self.num_frames:
            self.evict_page()
        
        # load the page data into the physical memory
        self.physical_memory.append(page_data_binary)

        # the frame number is the index of the page data in the physical memory
        frame_num = len(self.physical_memory) - 1

        # update the page table and TLB with the new page data
        self.page_table.load_page(page_num, frame_num)
        self.tlb.load_page(page_num, frame_num)
        
        return frame_num
        
    def evict_page(self):
        """
        Evicts a page from the page table and TLB, and removes the corresponding page from physical memory.

        This method is responsible for evicting a page from the page table and TLB, as well as removing the corresponding
        page from physical memory. It follows a FIFO (First-In-First-Out) eviction policy, where the oldest page in the
        physical memory is evicted.

        Note:
        - The page table and TLB must be initialized before calling this method.
        - The physical memory must contain at least one page before calling this method.

        Returns:
        None
        """
        self.page_table.evict_page()
        self.tlb.evict_page()

        # remove the oldest page from the physical memory in a FIFO manner with O(1) time complexity
        self.physical_memory.popleft()
    
    def page_fault_rate(self):
        """
        Calculates the page fault rate as a percentage.

        Returns:
            float: The page fault rate.
        """
        return self.page_faults / self.accesses * 100

    def tlb_hit_rate(self):
            """
            Calculates and returns the hit rate of the Translation Lookaside Buffer (TLB).

            Returns:
                float: The hit rate of the TLB.
            """
            return self.tlb.hit_rate()
    
    def log_system_info(self):
        """
        Logs the system information including program address space, page size, number of pages,
        number of frames, TLB size, page fault rate, and TLB hit rate. It also writes the logs to
        a file named 'log.txt'.

        Returns:
            None
        """
        self.logs.append(f"Program address space: {self.program_address_space}")
        self.logs.append(f"Page size: {self.page_size}")
        self.logs.append(f"Number of pages: {self.num_pages}")
        self.logs.append(f"Number of frames: {self.num_frames}")
        self.logs.append(f"TLB size: {self.tlb_size}")
        self.logs.append(f"Page fault rate: {self.page_fault_rate()}%")
        self.logs.append(f"TLB hit rate: {self.tlb_hit_rate()}%")

        with open('log.txt', 'w') as log_file:
            for line in self.logs:
                log_file.write(line + '\n')
    
    def __str__(self):
        """
        Returns a string representation of the VirtualMemory object.

        The string includes the page table, TLB entries, and physical memory.

        Returns:
            str: A string representation of the VirtualMemory object.
        """
        return f"Page Table: {self.page_table.table}\nTLB: {self.tlb.entries}\nPhysical Memory: {self.physical_memory}"