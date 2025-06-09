import cython
import numpy as np


cdef enum OperandKind:
    IGNORE = 0
    LITERAL = 1
    COMBO = 2


class Device:
    A: cython.ulonglong
    B: cython.ulonglong
    C: cython.ulonglong
    IP: cython.uint
    opcode: cython.uint
    operand: cython.uint
    operand_kind: cython.uint
    program: np.ndarray
    output: np.ndarray

    def __init__(self, a: cython.ulonglong, b: cython.ulonglong, c: cython.ulonglong, program: np.ndarray):
        self.A = a
        self.B = b
        self.C = c
        self.IP = 0

        self.opcode = 0
        self.operand = 0
        self.operand_kind = 0

        self.program = program
        self.output = np.array([], np.uint64)


    def run(self):
        while True:
            if self.IP + 1 > len(self.program):
                break

            self.opcode, self.operand = self.program[self.IP:self.IP + 2]

            if self.opcode == 0:
                inc_ip = self._adv()
            elif self.opcode == 1:
                inc_ip = self._bxl()
            elif self.opcode == 2:
                inc_ip = self._bst()
            elif self.opcode == 3:
                inc_ip = self._jnz()
            elif self.opcode == 4:
                inc_ip = self._bxc()
            elif self.opcode == 5:
                inc_ip = self._out()
            elif self.opcode == 6:
                inc_ip = self._bdv()
            elif self.opcode == 7:
                inc_ip = self._cdv()

            if inc_ip:
                self.IP += 2

    def _operand(self):
        if self.operand_kind == OperandKind.IGNORE:
            raise RuntimeError("tried to read an ignored operand")
        elif self.operand_kind == OperandKind.LITERAL:
            # literal
            return self.operand
        elif self.operand_kind == OperandKind.COMBO:
            # combo
            if  0 <= self.operand <= 3:
                return self.operand
            elif self.operand == 4:
                return self.A
            elif self.operand == 5:
                return self.B
            elif self.operand == 6:
                return self.C
            else:
                raise RuntimeError("combo 7 is undefined")
        else:
            raise RuntimeError("unknown operand_kind")

    def _adv(self):
        self.operand_kind = COMBO
        self.A = (self.A // 2 ** self._operand())
        return True

    def _bxl(self):
        self.operand_kind = LITERAL
        self.B = self.B ^ self._operand()
        return True

    def _bst(self):
        self.operand_kind = COMBO
        self.B = self._operand() % 8
        return True

    def _jnz(self):
        self.operand_kind = LITERAL
        if self.A == 0:
            return True

        self.IP = self._operand()
        return False

    def _bxc(self):
        self.operand_kind = IGNORE
        self.B = self.B ^ self.C
        return True

    def _out(self):
        self.operand_kind = COMBO
        self.output = np.append(self.output, self._operand() % 8)
        return True

    def _bdv(self):
        self.operand_kind = COMBO
        self.B = (self.A // 2 ** self._operand())
        return True

    def _cdv(self):
        self.operand_kind = COMBO
        self.C = (self.A // 2 ** self._operand())
        return True


def device(a, b, c, program):
    d = Device(a, b, c, program)
    d.run()
    return d.output
