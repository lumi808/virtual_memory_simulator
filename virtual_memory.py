from tlb import TLB
from page_table import PageTable
import math

class VirtualMemory:
    def __init__(self, program_address_space, page_size, num_pages, num_frames, tlb_size):
        self.program_address_space = program_address_space
        self.page_size = page_size
        self.num_pages = num_pages
        self.num_frames = num_frames
        self.tlb_size = tlb_size

        self.page_table = PageTable(num_pages)
        self.tlb = TLB(tlb_size)

    def translate_address(self, virtual_address_decimal):
        virtual_address_binary = bin(virtual_address_decimal)[2:].zfill(self.program_address_space)
        print(f'virtual_address_binary: {virtual_address_binary}')

        page_num_bits = int(math.log(self.page_size, 2))
        page_num = virtual_address_binary[:page_num_bits+1]

        offset_bits = self.program_address_space - page_num_bits
        page_offset = virtual_address_binary[offset_bits+1:]

        frame_num = self.tlb.access(page_num)

        if frame_num is None:
            frame_num = self.page_table.access(page_num)
        
        if frame_num is None:
            frame_num = self.page_fault(page_num)
            #first commit

        return frame_num

    def page_fault(self, page_num):
        print('Page fault!')
        #TODO: Implement page fault handling