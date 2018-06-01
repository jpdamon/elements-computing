"""Arithmetic Logical Unit

Modules for performing simple 2s-complement arithmetic, using
logic gates from gates.py
"""
from computing.gate import xor_gate, and_gate, or_gate


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


def adder(register_a, register_b, register_out, n):
    """ n-bit adder.
    2s complement addition of register a and b, storing in output register.
    Overflow is not handled or detected.
    """

    carry = 0
    # start at LSB and move to MSB
    for i in range(n-1, -1, -1):
        carry, register_out[i] = full_adder(register_a[i], register_b[i], carry)
