import unittest
from computing.alu import half_adder, full_adder, adder


class TestAlu(unittest.TestCase):

    def test_halfadder(self):
        self.assertEqual((0, 0), half_adder(0, 0))
        self.assertEqual((0, 1), half_adder(0, 1))
        self.assertEqual((0, 1), half_adder(1, 0))
        self.assertEqual((1, 0), half_adder(1, 1))

    def test_fulladder(self):
        self.assertEqual((0, 0), full_adder(0, 0, 0))
        self.assertEqual((0, 1), full_adder(0, 0, 1))
        self.assertEqual((0, 1), full_adder(0, 1, 0))
        self.assertEqual((1, 0), full_adder(0, 1, 1))
        self.assertEqual((0, 1), full_adder(1, 0, 0))
        self.assertEqual((1, 0), full_adder(1, 0, 1))
        self.assertEqual((1, 0), full_adder(1, 1, 0))
        self.assertEqual((1, 1), full_adder(1, 1, 1))

    def test_adder(self):
        # test with a 4-bit adder for simplicity
        for a in range(0, 16):
            for b in range(0, 16):
                register_a = _int_as_register(a, 4)
                register_b = _int_as_register(b, 4)
                expected_output = _int_as_register(a + b, 4)
                actual_output = [None]*4
                adder(register_a, register_b, actual_output, 4)
                self.assertEqual(
                    expected_output,
                    actual_output,
                    f"{a} plus {b}"
                )

        register_a = _int_as_register(9, 4)
        self.assertEqual([1, 0, 0, 1], register_a)


def _int_as_register(integer, n):
    """ Convert an integer to a register of n-bits.
    _int_as_register(9, 4) returns [1,0,0,1]"""

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
