import unittest
from itertools import product

from computing.alu import preset_register16
from computing.gate import *


class TestGates(unittest.TestCase):

    def test_nand(self):
        self.assertEqual(1, nand_gate(0, 0))
        self.assertEqual(1, nand_gate(0, 1))
        self.assertEqual(1, nand_gate(1, 0))
        self.assertEqual(0, nand_gate(1, 1))

    def test_not(self):
        self.assertEqual(1, not_gate(0))
        self.assertEqual(0, not_gate(1))

    def test_and(self):
        self.assertEqual(0, and_gate(0, 0))
        self.assertEqual(0, and_gate(0, 1))
        self.assertEqual(0, and_gate(1, 0))
        self.assertEqual(1, and_gate(1, 1))

    def test_or(self):
        self.assertEqual(0, or_gate(0, 0))
        self.assertEqual(1, or_gate(0, 1))
        self.assertEqual(1, or_gate(1, 0))
        self.assertEqual(1, or_gate(1, 1))

    def test_xor(self):
        self.assertEqual(0, xor_gate(0, 0))
        self.assertEqual(1, xor_gate(0, 1))
        self.assertEqual(1, xor_gate(1, 0))
        self.assertEqual(0, xor_gate(1, 1))

    def test_mux(self):
        # sel = 0, a is returned
        self.assertEqual(0, mux_gate(0, 0, 0))
        self.assertEqual(0, mux_gate(0, 1, 0))
        self.assertEqual(1, mux_gate(1, 0, 0))
        self.assertEqual(1, mux_gate(1, 1, 0))

        # sel = 1, b is returned
        self.assertEqual(0, mux_gate(0, 0, 1))
        self.assertEqual(1, mux_gate(0, 1, 1))
        self.assertEqual(0, mux_gate(1, 0, 1))
        self.assertEqual(1, mux_gate(1, 1, 1))

    def test_dmux(self):
        # sel = 0, return (input, 0)
        self.assertEqual((0, 0), dmux_gate(0, 0))
        self.assertEqual((1, 0), dmux_gate(1, 0))

        # sel = 1, return (0, input)
        self.assertEqual((0, 0), dmux_gate(0, 1))
        self.assertEqual((0, 1), dmux_gate(1, 1))

    def test_dmux4way(self):
        # sel = 00, return (input, 0, 0, 0)
        sel = [0, 0]
        self.assertEqual((0, 0, 0, 0), dmux4way_gate(0, sel))
        self.assertEqual((1, 0, 0, 0), dmux4way_gate(1, sel))

        # sel = 01, return (0, input, 0, 0)
        sel = [0, 1]
        self.assertEqual((0, 0, 0, 0), dmux4way_gate(0, sel))
        self.assertEqual((0, 1, 0, 0), dmux4way_gate(1, sel))

        # sel = 10, return (0, 0, input, 0)
        sel = [1, 0]
        self.assertEqual((0, 0, 0, 0), dmux4way_gate(0, sel))
        self.assertEqual((0, 0, 1, 0), dmux4way_gate(1, sel))

        # sel = 11, return (0, 0, 0, input)
        sel = [1, 1]
        self.assertEqual((0, 0, 0, 0), dmux4way_gate(0, sel))
        self.assertEqual((0, 0, 0, 1), dmux4way_gate(1, sel))

    def test_not16(self):
        a = [0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0]
        e = [1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1]
        self.assertEqual(e, not16_gate(a))

    def test_or16(self):
        a = [0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0]
        b = [0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1]
        e = [0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1]
        self.assertEqual(e, or16_gate(a, b))

    def test_and16(self):
        a = [0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0]
        b = [0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1]
        e = [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
        self.assertEqual(e, and16_gate(a, b))

    def test_mux16(self):
        a = [0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1]
        b = [0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1]
        output= [None]*16
        mux16_gate(a, b, output, 0)
        self.assertEqual(a, output)
        output = [None]*16
        mux16_gate(a, b, output, 1)
        self.assertEqual(b, output)

    def test_or8way(self):
        cases = product([0, 1], repeat=8)
        index = 0
        for c in cases:
            index += 1
            if 1 in c:
                expected = 1
            else:
                expected = 0

            self.assertEqual(expected, or8way_gate(c), f"Case {index}")

    def test_and8way(self):
        cases = product([0, 1], repeat=8)
        index = 0
        for c in cases:
            index += 1
            if 0 in c:
                expected = 0
            else:
                expected = 1

            self.assertEqual(expected, and8way_gate(c), f"Case {index}")

    def test_mux4way(self):
        # all possible inputs of a, b, c, d
        cases = product([0, 1], repeat=4)
        for inputs in cases:

            # test each select bit combination
            self.assertEqual(inputs[0], mux4way_gate(inputs, [0, 0]))
            self.assertEqual(inputs[1], mux4way_gate(inputs, [1, 0]))
            self.assertEqual(inputs[2], mux4way_gate(inputs, [0, 1]))
            self.assertEqual(inputs[3], mux4way_gate(inputs, [1, 1]))

    def test_mux8way(self):
        # all possible inputs of a..h
        cases = product([0, 1], repeat=8)
        for inputs in cases:
            # test each select bit combination
            self.assertEqual(inputs[0], mux8way_gate(inputs, [0, 0, 0]))
            self.assertEqual(inputs[1], mux8way_gate(inputs, [1, 0, 0]))
            self.assertEqual(inputs[2], mux8way_gate(inputs, [0, 1, 0]))
            self.assertEqual(inputs[3], mux8way_gate(inputs, [1, 1, 0]))
            self.assertEqual(inputs[4], mux8way_gate(inputs, [0, 0, 1]))
            self.assertEqual(inputs[5], mux8way_gate(inputs, [1, 0, 1]))
            self.assertEqual(inputs[6], mux8way_gate(inputs, [0, 1, 1]))
            self.assertEqual(inputs[7], mux8way_gate(inputs, [1, 1, 1]))

    def test_preset_register16(self):
        register_a = [0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1]
        negate_a = [1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0]
        output = [None]*16
        preset_register16(register_a, output, 0, 0)
        self.assertEqual(register_a, output, "Do not zero, do not negate")

        output = [None] * 16
        preset_register16(register_a, output, 1, 0)
        self.assertEqual([0]*16, output, "Zero, do not negate")

        output = [None] * 16
        preset_register16(register_a, output, 0, 1)
        self.assertEqual(negate_a, output, "Do not zero, negate")

        output = [None] * 16
        preset_register16(register_a, output, 1, 1)
        self.assertEqual([1]*16, output, "Zero, and negate")

