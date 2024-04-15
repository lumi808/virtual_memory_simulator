from virtual_memory import VirtualMemory

def main():
    page_size = 4096
    num_pages = 16
    num_frames = 4  
    tlb_capacity = 4 

    virtual_memory = VirtualMemory(page_size, num_pages, num_frames, tlb_capacity)

    print("Hello World!")

if __name__ == "__main__":
    main()
