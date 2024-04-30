from virtual_memory import VirtualMemory

def main():
    program_address_space = 16 # Number of bits in the address space
    page_size = 256 # Size of a page in bytes
    num_pages = 16 # Number of pages in virtual memory
    num_frames = 256 # Number of frames in physical memory
    tlb_capacity = 16 # Number of entries in the TLB

    virtual_memory = VirtualMemory(program_address_space, page_size, num_pages, num_frames, tlb_capacity)

    virtual_memory.translate_address_from_file('addresses.txt')

if __name__ == "__main__":
    main()
