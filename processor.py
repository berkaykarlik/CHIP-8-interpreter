from gui import Gui
from memory import Memory
from stack import Stack
from register import Register
from timers import DelayTimer, SoundTimer

def _0nnn():
    """
    0x0NNN: SYS addr
    Jump to a machine code routine at nnn.
    """
    #raise NotImplementedError so that we will now if a program is trying to jump to a machine code routine
    raise NotImplementedError("Program tried to jump to a machine code routine")

def _00e0(gui:Gui):
    """
    0x00E0: CLS
    Clear the display.
    """
    gui.clear_screen()


def _00ee(mem:Memory,stack:Stack):
    """
    0x00EE: RET
    Return from a subroutine.
    """
    #pop the top value from the stack and jump to it
    return mem.jump(stack.pop())

def _1nnn(mem:Memory,nnn_nimble:int):
    """
    0x1NNN: JP addr
    Jump to location nnn.
    """
    return mem.jump(nnn_nimble)