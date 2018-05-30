import unittest
from itertools import product
from computing.gate import *


class TestGates(unittest.TestCase):

    def test_nand(self):
        self.assertEqual(1, Nand(0, 0))
        self.assertEqual(1, Nand(0, 1))
        self.assertEqual(1, Nand(1, 0))
        self.assertEqual(0, Nand(1, 1))

    def test_not(self):
        self.assertEqual(1, Not(0))
        self.assertEqual(0, Not(1))

    def test_and(self):
        self.assertEqual(0, And(0, 0))
        self.assertEqual(0, And(0, 1))
        self.assertEqual(0, And(1, 0))
        self.assertEqual(1, And(1, 1))

    def test_or(self):
        self.assertEqual(0, Or(0, 0))
        self.assertEqual(1, Or(0, 1))
        self.assertEqual(1, Or(1, 0))
        self.assertEqual(1, Or(1, 1))

    def test_xor(self):
        self.assertEqual(0, Xor(0, 0))
        self.assertEqual(1, Xor(0, 1))
        self.assertEqual(1, Xor(1, 0))
        self.assertEqual(0, Xor(1, 1))

    def test_mux(self):
        # sel = 0, a is returned
        self.assertEqual(0, Mux(0, 0, 0))
        self.assertEqual(0, Mux(0, 1, 0))
        self.assertEqual(1, Mux(1, 0, 0))
        self.assertEqual(1, Mux(1, 1, 0))

        # sel = 1, b is returned
        self.assertEqual(0, Mux(0, 0, 1))
        self.assertEqual(1, Mux(0, 1, 1))
        self.assertEqual(0, Mux(1, 0, 1))
        self.assertEqual(1, Mux(1, 1, 1))

    def test_dmux(self):
        # sel = 0, return (input, 0)
        self.assertEqual((0, 0), Dmux(0, 0))
        self.assertEqual((1, 0), Dmux(1, 0))

        # sel = 1, return (0, input)
        self.assertEqual((0, 0), Dmux(0, 1))
        self.assertEqual((0, 1), Dmux(1, 1))

    def test_not16(self):
        a = [0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0]
        e = [1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1]
        self.assertEqual(e, Not16(a))

    def test_or16(self):
        a = [0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0]
        b = [0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1]
        e = [0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1]
        self.assertEqual(e, Or16(a, b))

    def test_and16(self):
        a = [0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0]
        b = [0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1]
        e = [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
        self.assertEqual(e, And16(a, b))

    def test_mux16(self):
        a = [0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1]
        b = [0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1]
        self.assertEqual(a, Mux16(a, b, 0))
        self.assertEqual(b, Mux16(a, b, 1))

    def test_or8way(self):
        cases = product([0, 1], repeat=8)
        index = 0
        for c in cases:
            index += 1
            if 1 in c:
                expected = 1
            else:
                expected = 0

            self.assertEqual(expected, Or8Way(c), f"Case {index}")

    def test_and8way(self):
        cases = product([0, 1], repeat=8)
        index = 0
        for c in cases:
            index += 1
            if 0 in c:
                expected = 0
            else:
                expected = 1

            self.assertEqual(expected, And8Way(c), f"Case {index}")

    def test_mux4way(self):
        # all possible inputs of a, b, c, d
        cases = product([0, 1], repeat=4)
        for inputs in cases:

            # test each select bit combination
            self.assertEqual(inputs[0], Mux4Way(inputs, [0, 0]))
            self.assertEqual(inputs[1], Mux4Way(inputs, [1, 0]))
            self.assertEqual(inputs[2], Mux4Way(inputs, [0, 1]))
            self.assertEqual(inputs[3], Mux4Way(inputs, [1, 1]))

    def test_mux8way(self):
        # all possible inputs of a..h
        cases = product([0, 1], repeat=8)
        for inputs in cases:
            # test each select bit combination
            self.assertEqual(inputs[0], Mux8Way(inputs, [0, 0, 0]))
            self.assertEqual(inputs[1], Mux8Way(inputs, [1, 0, 0]))
            self.assertEqual(inputs[2], Mux8Way(inputs, [0, 1, 0]))
            self.assertEqual(inputs[3], Mux8Way(inputs, [1, 1, 0]))
            self.assertEqual(inputs[4], Mux8Way(inputs, [0, 0, 1]))
            self.assertEqual(inputs[5], Mux8Way(inputs, [1, 0, 1]))
            self.assertEqual(inputs[6], Mux8Way(inputs, [0, 1, 1]))
            self.assertEqual(inputs[7], Mux8Way(inputs, [1, 1, 1]))
