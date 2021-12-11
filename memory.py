

class Memory():

    def __init__(self) -> None:
        self.__memory = [None for i in range(0x1000)]
        # add font
        self.__memory[0x50:0xA0] = [0xF0, 0x90, 0x90, 0x90, 0xF0,  # 0
                                    0x20, 0x60, 0x20, 0x20, 0x70,  # 1
                                    0xF0, 0x10, 0xF0, 0x80, 0xF0,  # 2
                                    0xF0, 0x10, 0xF0, 0x10, 0xF0,  # 3
                                    0x90, 0x90, 0xF0, 0x10, 0x10,  # 4
                                    0xF0, 0x80, 0xF0, 0x10, 0xF0,  # 5
                                    0xF0, 0x80, 0xF0, 0x90, 0xF0,  # 6
                                    0xF0, 0x10, 0x20, 0x40, 0x40,  # 7
                                    0xF0, 0x90, 0xF0, 0x90, 0xF0,  # 8
                                    0xF0, 0x90, 0xF0, 0x10, 0xF0,  # 9
                                    0xF0, 0x90, 0xF0, 0x90, 0x90,  # A
                                    0xE0, 0x90, 0xE0, 0x90, 0xE0,  # B
                                    0xF0, 0x80, 0x80, 0x80, 0xF0,  # C
                                    0xE0, 0x90, 0x90, 0x90, 0xE0,  # D
                                    0xF0, 0x80, 0xF0, 0x80, 0xF0,  # E
                                    0xF0, 0x80, 0xF0, 0x80, 0x80]  # F

    def get(memory_address):
        pass

    def set(memory_address):
        # TODO: limit memor to 4096 bytes, i.e index 0xFFF
        pass


if __name__ == '__main__':
    mem = Memory()
    print(mem._Memory__memory[0x50:0xA0])
