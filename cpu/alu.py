"""Arithmetic Logic Unit

Modules for performing simple 2s-complement arithmetic, using
logic gates from gates.py
"""
from cpu.gate import *


def half_adder(a, b):
    """Add a and b, returning sum and carry bit
    :return (carry, sum)

    a   |   b   | carry |   sum
    ----|-------|-------|---------
    0   |   0   |   0   |   0
    0   |   1   |   0   |   1
    1   |   0   |   0   |   1
    1   |   1   |   1   |   0
    """

    return and_gate(a, b), xor_gate(a, b)


def full_adder(a, b, c):
    """Add a, b, and c, returning sum and carry bit.
    :return (carry, sum)

    a   |   b   |   c   | carry |   sum
    ----|-------|-------|-------|-------
    0   |   0   |   0   |   0   |   0
    0   |   0   |   1   |   0   |   1
    0   |   1   |   0   |   0   |   1
    0   |   1   |   1   |   1   |   0
    1   |   0   |   0   |   0   |   1
    1   |   0   |   1   |   1   |   0
    1   |   1   |   0   |   1   |   0
    1   |   1   |   1   |   1   |   1
    """

    carry1, partial_sum = half_adder(a, b)
    carry2, final_sum = half_adder(c, partial_sum)
    return or_gate(carry1, carry2), final_sum


def add(register_a, register_b, register_out, n):
    """ n-bit adder.
    2s complement addition of register a and b, storing in output register.
    Overflow is not handled or detected.
    """

    carry = 0
    # start at LSB and move to MSB
    for i in range(n-1, -1, -1):
        carry, register_out[i] = full_adder(register_a[i], register_b[i], carry)


def add16(register_a, register_b, register_out):
    """ 16-bit adder.
    2s complement addition of register a and b, storing in output register.
    Overflow is not handled or detected.
    """
    add(register_a, register_b, register_out, 16)

_FALSE16 = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
_TRUE16 = (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
_INCREMENT16 = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1)


def inc16(register_in, register_out):
    """ increment register_in by 1, store result in register_out"""
    add16(register_in, _INCREMENT16, register_out)


def preset_register16(register_in, register_out, zero, negate):
    """ setup register input for ALU, based on zero and negate flags"""
    intermediate = [None]*16
    mux16_gate(register_in, _FALSE16, intermediate, zero)
    notregister = not16_gate(intermediate)
    mux16_gate(intermediate, notregister, register_out, negate )

def alu16(register_x, register_y, zero_x, not_x, zero_y, not_y, f, not_out, register_out):
    """16-bit Arithemtic Logic Unit.

    :param register_x: first register in equation
    :param register_y: second register in equation
    :param zero_x: if 1, treat register_x as zero in calculation
    :param not_x: if 1, use !register_x in calculation
    :param zero_y: if 1, treat register_y as zero in calculation
    :param not_y: if 1, use !register_y in calculation
    :param f: if f=1, then out=x+y. if f=0, out=x&y
    :param not_out: if 1, negate (!out) equation result before returning
    :param register_out: register where equation result will be stored
    :returns (zero_flag, negative_flag): zero_flag=1 if output is 0, negative_flag=1 if output is negative
    """

    # intermediate pins
    x = [None]*16
    y = [None]*16
    add_out= [None]*16
    mux_out = [None]*16

    preset_register16(register_x, x, zero_x, not_x)
    preset_register16(register_y, y, zero_y, not_y)

    # Do x+y, and x&y, select which result based on f flag
    add16(x, y, add_out)
    and_out = and16_gate(x, y)
    mux16_gate(and_out, add_out, mux_out, f)

    # Negate output based on not_out flag
    negate_out = not16_gate(mux_out)
    mux16_gate(mux_out, negate_out, register_out, not_out)


# Common ALU function commands
ALU_ZERO = [1, 0, 1, 0, 1, 0]
ALU_ONE = [1, 1, 1, 1, 1, 1]
ALU_NEGATIVE_ONE = [1, 1, 1, 0, 1, 0]
ALU_X = [0, 0, 1, 1, 0, 0]
ALU_Y = [1, 1, 0, 0, 0, 0]
ALU_NOT_X = [0, 0, 1, 1, 0, 1]
ALU_NOT_Y = [1, 1, 0, 0, 0, 1]
ALU_NEGATIVE_X = [0, 0, 1, 1, 1, 1]
ALU_NEGATIVE_Y = [1, 1, 0, 0, 1, 1]
ALU_INCREMENT_X = [0, 1, 1, 1, 1, 1]
ALU_INCREMENT_Y = [1, 1, 0, 1, 1, 1]
ALU_DECREMENT_X = [0, 0, 1, 1, 1, 0]
ALU_DECREMENT_Y = [1, 1, 0, 0, 1, 0]
ALU_X_PLUS_Y = [0, 0, 0, 0, 1, 0]
ALU_X_MINUS_Y = [0, 1, 0, 0, 1, 1]
ALU_Y_MINUS_X = [0, 0, 0, 1, 1, 1]
ALU_X_AND_Y = [0, 0, 0, 0, 0, 0]
ALU_X_OR_Y = [0, 1, 0, 1, 0, 1]

# Command bit index for passing to alu16 command(ALU_X_PLUS_Y[ZX_BIT] yields the zx flag bit for x+y command)
ZX_BIT = 0
NX_BIT = 1
ZY_BIT = 2
NY_BIT = 3
F_BIT = 4
NO_BIT = 5