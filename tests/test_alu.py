import unittest
from computing.alu import *
from tests.util import int_as_register


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

    def test_add(self):
        # test with a 4-bit adder for simplicity
        for a in range(0, 16):
            for b in range(0, 16):
                register_a = int_as_register(a, 4)
                register_b = int_as_register(b, 4)
                expected_output = int_as_register(a + b, 4)
                actual_output = [None]*4
                add(register_a, register_b, actual_output, 4)
                self.assertEqual(
                    expected_output,
                    actual_output,
                    f"{a} plus {b}"
                )

    def test_inc16(self):
        for a in range(2**(16-1)):
            register_a = int_as_register(a, 16)
            expected_output = int_as_register(a + 1, 16)
            actual_output = [None]*16
            inc16(register_a, actual_output)
            self.assertEqual(expected_output, actual_output, f"{a} plus 1")

    def test_alu_zero(self):
        x = int_as_register(1234, 16)
        y = int_as_register(567, 16)
        output = [None]*16
        alu16(
            x,
            y,
            ALU_ZERO[ZX_BIT],
            ALU_ZERO[NX_BIT],
            ALU_ZERO[ZY_BIT],
            ALU_ZERO[NY_BIT],
            ALU_ZERO[F_BIT],
            ALU_ZERO[NO_BIT],
            output)
        self.assertEqual([0]*16, output)

    def test_alu_one(self):
        x = int_as_register(1234, 16)
        y = int_as_register(567, 16)
        output = [None]*16
        alu16(
            x,
            y,
            ALU_ONE[ZX_BIT],
            ALU_ONE[NX_BIT],
            ALU_ONE[ZY_BIT],
            ALU_ONE[NY_BIT],
            ALU_ONE[F_BIT],
            ALU_ONE[NO_BIT],
            output)
        self.assertEqual(int_as_register(1, 16), output)

    def test_alu_negative_one(self):
        x = int_as_register(1234, 16)
        y = int_as_register(567, 16)
        output = [None]*16
        alu16(
            x,
            y,
            ALU_NEGATIVE_ONE[ZX_BIT],
            ALU_NEGATIVE_ONE[NX_BIT],
            ALU_NEGATIVE_ONE[ZY_BIT],
            ALU_NEGATIVE_ONE[NY_BIT],
            ALU_NEGATIVE_ONE[F_BIT],
            ALU_NEGATIVE_ONE[NO_BIT],
            output)
        self.assertEqual([1]*16, output)

    def test_alu_x(self):
        x = int_as_register(1234, 16)
        y = int_as_register(567, 16)
        output = [None]*16
        alu16(
            x,
            y,
            ALU_X[ZX_BIT],
            ALU_X[NX_BIT],
            ALU_X[ZY_BIT],
            ALU_X[NY_BIT],
            ALU_X[F_BIT],
            ALU_X[NO_BIT],
            output)
        self.assertEqual(x, output)

    def test_alu_y(self):
        x = int_as_register(1234, 16)
        y = int_as_register(567, 16)
        output = [None]*16
        alu16(
            x,
            y,
            ALU_Y[ZX_BIT],
            ALU_Y[NX_BIT],
            ALU_Y[ZY_BIT],
            ALU_Y[NY_BIT],
            ALU_Y[F_BIT],
            ALU_Y[NO_BIT],
            output)
        self.assertEqual(y, output)

    def test_alu_not_x(self):
        x = [0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0]
        y = int_as_register(567, 16)
        not_x = [1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1]
        output = [None]*16
        alu16(
            x,
            y,
            ALU_NOT_X[ZX_BIT],
            ALU_NOT_X[NX_BIT],
            ALU_NOT_X[ZY_BIT],
            ALU_NOT_X[NY_BIT],
            ALU_NOT_X[F_BIT],
            ALU_NOT_X[NO_BIT],
            output)
        self.assertEqual(not_x, output)

    def test_alu_not_y(self):
        x = int_as_register(1234, 16)
        y = [0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0]
        not_y = [1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1]
        output = [None]*16
        alu16(
            x,
            y,
            ALU_NOT_Y[ZX_BIT],
            ALU_NOT_Y[NX_BIT],
            ALU_NOT_Y[ZY_BIT],
            ALU_NOT_Y[NY_BIT],
            ALU_NOT_Y[F_BIT],
            ALU_NOT_Y[NO_BIT],
            output)
        self.assertEqual(not_y, output)
