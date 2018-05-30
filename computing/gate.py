""" Logic Gates

    All gates implemented using NAND gates.
"""

# usage: _NAND[a][b]
_NAND = [[1, 1], [1, 0]]


def Nand(a, b):
    """ a primitive gate, used to build all other gates"""

    return _NAND[a][b]


def Not(a):
    return Nand(a, a)


def And(a, b):
    return Not(Nand(a, b))


def Or(a, b):
    return Nand(Not(a), Not(b))


def Xor(a, b):
    # todo: this seems like it can be simplified
    return And(Or(a, b), Nand(a, b))


def Mux(a, b, sel):
    ''' if sel=0, return a. if sel=1, return b'''

    # (!sel and a) or (sel and b)
    return Or(And(Not(sel), a), And(sel, b))


def Dmux(input, sel):
    """ if sel=0, return (input, 0). if sel=1, return (0, input)"""
    return (And(Not(sel), input), And(sel, input))

def Not16(arr):
    """ apply Not to each bit in array """

    return [Not(arr[i]) for i in range(16)]


def And16(arrA, arrB):
    """ AND each bit of arrA with each bit of arrB"""
    return [And(arrA[i], arrB[i]) for i in range(16)]


def Or16(arrA, arrB):
    """ OR each bit of arrA with each bit of arrB"""
    return [Or(arrA[i], arrB[i]) for i in range(16)]


def Mux16(arrA, arrB, sel):
    """ MUX each bit of arrA and arrB using sel """
    return [Mux(arrA[i], arrB[i], sel) for i in range(16)]

def Or8Way(arr):
    """ OR every bit of array. return 1 if any bit is 1 """
    return Or(
        Or(
            Or(arr[0], arr[1]),
            Or(arr[2], arr[3])
        ),
        Or(
            Or(arr[4], arr[5]),
            Or(arr[6], arr[7])
        )
    )

def And8Way(arr):
    """ AND every bit of array. return 1 if all bits are 1 """
    return And(
        And(
            And(arr[0], arr[1]),
            And(arr[2], arr[3])
        ),
        And(
            And(arr[4], arr[5]),
            And(arr[6], arr[7])
        )
    )

def Mux4Way(input4, sel2):
    """
    MUX with 4 inputs, 2-bit selector.

    sel[1]| sel[0]  | out
    ----|-------|-----
    0   |   0   | a
    0   |   1   | b
    1   |   0   | c
    1   |   1   | d
    """
    top = Mux(input4[0], input4[1], sel2[0])
    bottom = Mux(input4[2], input4[3], sel2[0])
    return Mux(top , bottom, sel2[1])

def Mux8Way(input8, sel3):
    """
    MUX with 8 inputs, 3-bit selector

    sel[2] |sel[1]| sel[0]  | out
    ----|-------|-----
    0   |   0   |   0   | a
    0   |   0   |   1   | b
    0   |   1   |   0   | c
    0   |   1   |   1   | d
    1   |   0   |   0   | e
    1   |   0   |   1   | f
    1   |   1   |   0   | g
    1   |   1   |   1   | h
    """
    top = Mux4Way(input8[0:4], sel3[0:2])
    bottom = Mux4Way(input8[4:], sel3[0:2])
    return Mux(top, bottom, sel3[2])


