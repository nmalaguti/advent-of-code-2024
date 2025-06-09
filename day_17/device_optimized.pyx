# device_optimized.pyx

# Reinstate deprecated-API macro before NumPy includes
cdef extern from *:
    """
    #define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
    """

# Cython speed directives
# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True
# cython: infer_types=True

import numpy as np
cimport numpy as np


# 64-bit unsigned alias
ctypedef np.uint64_t UINT64

# Operand kinds
cdef enum OperandKind:
    IGNORE = 0
    LITERAL = 1
    COMBO = 2

# Fast inline operand resolver
cdef inline UINT64 resolve_operand(UINT64 o, int kind,
                                   UINT64 A, UINT64 B, UINT64 C):
    if kind == OperandKind.LITERAL:
        return o
    if o <= 3:
        return o
    elif o == 4:
        return A
    elif o == 5:
        return B
    elif o == 6:
        return C
    return <UINT64>0

# Main entry point
def device(unsigned long long a, unsigned long long b, unsigned long long c,
           np.ndarray[np.uint64_t, ndim=1] program):
    """
    a, b, c: initial register values (uint64)
    program: numpy array of uint64 instructions [op, operand, ...]
    """
    # 1) Ensure C-contiguous uint64 array
    cdef np.ndarray[UINT64, ndim=1] arr = \
        np.ascontiguousarray(program, dtype=np.uint64)
    # 2) Obtain memoryview
    cdef UINT64[:] p = arr
    cdef Py_ssize_t n = arr.shape[0]

    # Registers & instruction pointer
    cdef UINT64 A = <UINT64>a
    cdef UINT64 B = <UINT64>b
    cdef UINT64 C = <UINT64>c
    cdef Py_ssize_t IP = 0

    # Collect outputs in a list
    cdef list out_list = []
    cdef UINT64 op, opd, val
    cdef int kind

    # Interpreter loop
    while IP + 1 < n:
        op  = p[IP]
        opd = p[IP + 1]
        if op == 0:
            kind = OperandKind.COMBO
            A >>= resolve_operand(opd, kind, A, B, C)
            IP += 2
        elif op == 1:
            kind = OperandKind.LITERAL
            B ^= resolve_operand(opd, kind, A, B, C)
            IP += 2
        elif op == 2:
            kind = OperandKind.COMBO
            B = resolve_operand(opd, kind, A, B, C) & 7
            IP += 2
        elif op == 3:
            kind = OperandKind.LITERAL
            if A != 0:
                IP = resolve_operand(opd, kind, A, B, C)
            else:
                IP += 2
        elif op == 4:
            B ^= C
            IP += 2
        elif op == 5:
            kind = OperandKind.COMBO
            val = resolve_operand(opd, kind, A, B, C) & 7
            out_list.append(val)
            IP += 2
        elif op == 6:
            kind = OperandKind.COMBO
            B = A >> resolve_operand(opd, kind, A, B, C)
            IP += 2
        elif op == 7:
            kind = OperandKind.COMBO
            C = A >> resolve_operand(opd, kind, A, B, C)
            IP += 2
        else:
            break

    # Convert outputs to a uint64 NumPy array and return
    return np.array(out_list, dtype=np.uint64)
