from computing.alu import inc16
from computing.gate import not16_gate


def int_as_register(integer, n):
    """ Convert a (nonnegative) integer to a register of n-bits.
    int_as_register(9, 4) returns [1,0,0,1]
    """

    register = [1 if digit == '1' else 0 for digit in bin(integer)[2:]]

    if len(register) == n:
        return register
    elif len(register) > n:
        # return least significant n bits, discarding overflow
        return register[-n:]
    else:
        # pad with zeros
        while len(register) < n:
            register = [0] + register

        return register


def int16_as_register(integer):
    mag = abs(integer)

    output = int_as_register(mag, 16)

    if integer < 0:
        # do 2's complement for negative
        complement = not16_gate(output)
        inc16(complement, output)

    return output
