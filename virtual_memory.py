from tlb import TLB
from page_table import PageTable
import math
from collections import deque, OrderedDict

class VirtualMemory:
    def __init__(self, program_address_space, page_size, num_pages, num_frames, tlb_size):
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
        with open(file_name, 'r') as file:
            for line in file:
                virtual_address_decimal = int(line)
                self.translate_address(virtual_address_decimal)
        self.log_system_info()

    def get_page_num_offset(self, virtual_address_binary):
        page_num_bits = int(math.log(self.page_size, 2))
        page_num = virtual_address_binary[:page_num_bits+1]

        offset_bits = self.program_address_space - page_num_bits
        page_offset = virtual_address_binary[offset_bits:]

        return page_num, page_offset

    def translate_address(self, virtual_address_decimal):
        self.accesses += 1

        virtual_address_binary = bin(virtual_address_decimal)[2:].zfill(self.program_address_space)

        page_num, page_offset = self.get_page_num_offset(virtual_address_binary)

        frame_num = self.tlb.access(page_num)

        if frame_num is None:
            frame_num = self.page_table.access(page_num)
        
        if frame_num is None:
            self.page_faults += 1
            frame_num = self.page_fault(page_num)
        
        physical_address = frame_num * self.page_size + int(page_offset, 2)
        data = self.physical_memory[frame_num]
        self.logs.append(f"Virtual address: {bin(virtual_address_decimal)[2:]}, Physical address: { bin(physical_address)[2:]}, Value: {int.from_bytes(data, byteorder='big')}")

        return physical_address, data

    def page_fault(self, page_num):
        self.disk_file.seek(int(page_num, 2) * self.page_size)
        page_data_binary = self.disk_file.read(self.page_size)

        frame_num = self.load_page_data(page_num, page_data_binary)
        
        return frame_num
    
    def load_page_data(self, page_num, page_data_binary):
        if len(self.physical_memory) == self.num_frames:
            self.evict_page()
        
        self.physical_memory.append(page_data_binary)

        frame_num = len(self.physical_memory) - 1

        self.page_table.load_page(page_num, frame_num)
        self.tlb.load_page(page_num, frame_num)
        
        return frame_num
        
    def evict_page(self):
        self.page_table.evict_page()
        self.tlb.evict_page()

        self.physical_memory.popleft()
    
    def page_fault_rate(self):
        return self.page_faults / self.accesses * 100

    def tlb_hit_rate(self):
        return self.tlb.hit_rate()
    
    def log_system_info(self):
        self.logs.append(f"Page fault rate: {self.page_fault_rate()}%")
        self.logs.append(f"TLB hit rate: {self.tlb_hit_rate()}%")

        with open('log.txt', 'w') as log_file:
            for line in self.logs:
                log_file.write(line + '\n')
    
    def __str__(self):
        return f"Page Table: {self.page_table.table}\nTLB: {self.tlb.entries}\nPhysical Memory: {self.physical_memory}"