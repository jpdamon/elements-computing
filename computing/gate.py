""" Logic Gates

    All gates implemented using NAND gates.
"""

_NAND_PRIMITIVE = [[1, 1], [1, 0]]


def nand_gate(a, b):
    """ a primitive gate, used to build all other gates"""

    return _NAND_PRIMITIVE[a][b]


def not_gate(a):
    return nand_gate(a, a)


def and_gate(a, b):
    return not_gate(nand_gate(a, b))


def or_gate(a, b):
    return nand_gate(not_gate(a), not_gate(b))


def xor_gate(a, b):
    return and_gate(or_gate(a, b), nand_gate(a, b))


def mux_gate(a, b, sel):
    """ if sel=0, return a. if sel=1, return b"""

    # (!sel and a) or (sel and b)
    return or_gate(and_gate(not_gate(sel), a), and_gate(sel, b))


def dmux_gate(input, sel):
    """ if sel=0, return (input, 0). if sel=1, return (0, input)"""
    return (and_gate(not_gate(sel), input), and_gate(sel, input))


def dmux4way_gate(input, sel2):
    sel_a = and_gate(not_gate(sel2[0]), not_gate(sel2[1]))
    sel_b = and_gate(not_gate(sel2[0]), sel2[1])
    sel_c = and_gate(sel2[0], not_gate(sel2[1]))
    sel_d = and_gate(sel2[0], sel2[1])

    return (
        and_gate(sel_a, input),
        and_gate(sel_b, input),
        and_gate(sel_c, input),
        and_gate(sel_d, input)
    )


def not16_gate(arr):
    """ apply Not to each bit in array """

    return [not_gate(arr[i]) for i in range(16)]


def and16_gate(a, b):
    """ AND each bit of 16 bit array a with each bit of array b"""
    return [and_gate(a[i], b[i]) for i in range(16)]


def or16_gate(a, b):
    """ OR each bit of 16 bit array a with each bit of array b"""
    return [or_gate(a[i], b[i]) for i in range(16)]


def mux16_gate(a, b, out, sel):
    """ MUX each bit of 16 bit array a and array b using sel """
    for i in range(16):
        out[i] = mux_gate(a[i], b[i], sel)


def or8way_gate(arr):
    """ OR every bit of array. return 1 if any bit is 1 """
    return or_gate(
        or_gate(
            or_gate(arr[0], arr[1]),
            or_gate(arr[2], arr[3])
        ),
        or_gate(
            or_gate(arr[4], arr[5]),
            or_gate(arr[6], arr[7])
        )
    )


def and8way_gate(arr):
    """ AND every bit of array. return 1 if all bits are 1 """
    return and_gate(
        and_gate(
            and_gate(arr[0], arr[1]),
            and_gate(arr[2], arr[3])
        ),
        and_gate(
            and_gate(arr[4], arr[5]),
            and_gate(arr[6], arr[7])
        )
    )


def mux4way_gate(input4, sel2):
    """
    MUX with 4 inputs, 2-bit selector.

    sel[1]| sel[0]  | out
    ----|-------|-----
    0   |   0   | a
    0   |   1   | b
    1   |   0   | c
    1   |   1   | d
    """
    top = mux_gate(input4[0], input4[1], sel2[0])
    bottom = mux_gate(input4[2], input4[3], sel2[0])
    return mux_gate(top, bottom, sel2[1])


def mux8way_gate(input8, sel3):
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
    top = mux4way_gate(input8[0:4], sel3[0:2])
    bottom = mux4way_gate(input8[4:], sel3[0:2])
    return mux_gate(top, bottom, sel3[2])


