import argparse
import random
from pathlib import Path
from time import sleep

from py import process

import modules.processor as processor
from modules.gui import Gui
from modules.memory import Memory
from modules.stack import Stack
from modules.register import Register
from modules.timers import DelayTimer, SoundTimer


INSTR_PER_SEC = 1400


def main(rom_path: Path) -> None:
    mem = Memory()
    stack = Stack()
    dtimer = DelayTimer()
    stimer = SoundTimer()
    gui = Gui()
    reg = Register()

    with open(rom_path, 'rb') as rom:
        instr = rom.read()

    for i in range(0, len(instr), 2):
        int_instr = int.from_bytes(instr[i:i + 2], byteorder='big')
        mem.load_instr(int_instr)

    while(True):
        # delay for simulating a more real CHIP-8 experience,  700 instr per second lets say
        sleep(1/INSTR_PER_SEC)

        gui.process_events()
        pressed_keys = gui.get_pool()
        print(f'pressed_keys {pressed_keys}')

        # fetch
        curr_instr = mem.fetch()
        # decode & execute

        # decode once to avoid repetation inside case statements, even if its unnecessary for some instructions
        st_nimble = (curr_instr & 0xF000) >> 12
        nd_nimble = (curr_instr & 0x0F00) >> 8
        rd_nimble = (curr_instr & 0x00F0) >> 4
        th_nimble = curr_instr & 0x000F
        #third and fourth
        nn_nimble = curr_instr & 0x00FF
        #second, third and fourth
        nnn_nimble = curr_instr & 0x0FFF

        match st_nimble:
            case 0x0:
                match nnn_nimble:
                    case 0x0E0:
                        processor._00e0(gui)
                    case 0x0EE:
                        processor._00ee(mem, stack)
                    case 0x000:  # run out of instructions, instr value is empty memory cell
                        print("empty memory")
            case 0x1:
                processor._1nnn(mem, nnn_nimble)
            case 0x2:
                processor._2nnn(stack, mem, nnn_nimble)
            case 0x3:
                processor._3xkk(reg, mem, nd_nimble, nn_nimble)
            case 0x4:
                processor._4xkk(reg, mem, nd_nimble, nn_nimble)
            case 0x5:
                processor._5xy0(reg, mem, nd_nimble, rd_nimble)
            case 0x6:
                processor._6xkk(reg, nd_nimble, nn_nimble)
            case 0x7:
                processor._7xkk(reg, nd_nimble, nn_nimble)
            case 0x8:
                match th_nimble:
                    case 0:
                        processor._8xy0(reg, nd_nimble, rd_nimble)
                    case 1:
                        processor._8xy1(reg, nd_nimble, rd_nimble)
                    case 2:
                        processor._8xy2(reg, nd_nimble, rd_nimble)
                    case 3:
                        processor._8xy3(reg, nd_nimble, rd_nimble)
                    case 4:
                        processor._8xy4(reg, nd_nimble, rd_nimble)
                    case 5:
                        processor._8xy5(reg, nd_nimble, rd_nimble)
                    case 6:
                        processor._8xy6(reg, nd_nimble)
                    case 7:
                        processor._8xy7(reg, nd_nimble, rd_nimble)
                    case 0xE:
                        processor._8xye(reg, nd_nimble)
            case 0x9:
                processor._9xy0(reg, mem, nd_nimble, rd_nimble)
            case 0xA:
                processor.annn(reg, nnn_nimble)
            case 0xB:
                processor.bnnn(reg, mem, nnn_nimble)
            case 0xC:
                processor.cxkk(reg, nd_nimble, nn_nimble)
            case 0xD:
                processor.dxyn(reg, mem, gui, nd_nimble, rd_nimble, th_nimble)
            case 0xE:
                match nn_nimble:
                    case 0x9E:
                        processor.ex9e(reg, mem, nd_nimble, pressed_keys)
                    case 0xA1:
                        processor.exa1(reg, mem, nd_nimble, pressed_keys)
            case 0xF:  # timers
                match nn_nimble:
                    case 0x07:
                        processor.fx07(reg, dtimer, nd_nimble)
                    case 0x0A:
                        processor.fx0a(reg, gui, nd_nimble)
                    case 0x15:
                        processor.fx15(reg, dtimer, nd_nimble)
                    case 0x18:
                        processor.fx18(reg, stimer, nd_nimble)
                    case 0x1E:  # add to index
                        print("add to index")
                        new_I = reg.get_I()+reg.get_Vx(nd_nimble)
                        # not part of original instruction set but it wont break stuff he said
                        reg.set_Vx(
                            0xF, 1) if new_I > 0x0FFF else reg.set_Vx(0xF, 0)
                        reg.set_I(new_I)
                    case 0x29:
                        processor.fx29(reg, nd_nimble)
                    case 0x33:  # binar coded decimal conversion
                        print("binary coded decimal conversion")
                        val = reg.get_Vx(nd_nimble)
                        dgt1 = val % 10
                        dgt2 = ((val % 100) - dgt1) // 10
                        dgt3 = (val - (val % 100)) // 100
                        mem.set_mem(reg.get_I(), dgt3)
                        mem.set_mem(reg.get_I()+0x1, dgt2)
                        mem.set_mem(reg.get_I()+0x2, dgt1)
                    case 0x55:  # store mem
                        print("store mem")
                        for i in range(nd_nimble+1):
                            mem.set_mem(reg.get_I()+i, reg.get_Vx(i))
                    case 0x65:  # load mem
                        print("load mem")
                        for i in range(nd_nimble+1):
                            reg.set_Vx(i, mem.get_mem(reg.get_I()+i))
            case _:
                print(f"not implemented: {curr_instr} type {st_nimble}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='chip-8 code interpreter')
    parser.add_argument('rom_path', type=Path,
                        nargs=1, help='.ch8 file path, i.e rom to interpret')
    args = parser.parse_args()
    main(args.rom_path[0])
