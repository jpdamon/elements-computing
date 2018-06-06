import unittest

from computing.memory import *
from tests.util import *


class MockGate:
    def __init__(self, clock):
        self.tick_called = False
        clock.connect(self.tick)

    def tick(self):
        self.tick_called = True


class TestMemory(unittest.TestCase):
    def test_clock_no_callbacks(self):
        clock = ChipClock()
        self.assertEqual(0, clock.cycle)
        clock.tick()
        self.assertEqual(1, clock.cycle)

    def test_clock_callback(self):
        clock = ChipClock()
        a = MockGate(clock)
        b = MockGate(clock)
        c = MockGate(clock)

        self.assertFalse(a.tick_called)
        self.assertFalse(b.tick_called)
        self.assertFalse(c.tick_called)

        clock.tick()

        self.assertTrue(a.tick_called)
        self.assertTrue(b.tick_called)
        self.assertTrue(c.tick_called)

    def test_dataflipflop(self):
        clock = ChipClock()
        dff = DataFlipFlop(clock)
        dff.input = 1
        clock.tick()
        self.assertEqual(1, dff.output)

        # output does not change immediately
        dff.input = 0
        self.assertEqual(1, dff.output)

        # does change after clock tick
        clock.tick()
        self.assertEqual(0, dff.output)

    def test_bit_register(self):
        clock = ChipClock()
        reg = BitRegister(clock)

        # Load 1 into register
        reg.set_in(1)
        reg.set_load(1)
        clock.tick()
        self.assertEqual(1, reg.get_out())

        # Don't store input if load=0
        reg.set_load(0)
        reg.set_in(0)
        clock.tick()
        self.assertEqual(1, reg.get_out())

        # Load input into register by setting load=1
        reg.set_load(1)
        clock.tick()
        self.assertEqual(0, reg.get_out())

        # Keep load=1 and change input
        reg.set_in(1)
        clock.tick()
        self.assertEqual(1, reg.get_out())

    def test_16bit_register(self):
        clock = ChipClock()
        reg = Register16(clock)

        # load register
        value1 = int_as_register(12345, 16)
        reg.set_input(value1)
        reg.set_load(1)
        clock.tick()
        self.assertEqual(value1, reg.get_out())

        # Don't store input if load=0
        value2 = int_as_register(678, 16)
        reg.set_load(0)
        reg.set_input(value2)
        clock.tick()
        self.assertEqual(value1, reg.get_out())

        # Load input into register by setting load=1
        reg.set_load(1)
        clock.tick()
        self.assertEqual(value2, reg.get_out())

        # Keep load=1 and change input
        value3 = int_as_register(91011, 16)
        reg.set_input(value3)
        clock.tick()
        self.assertEqual(value3, reg.get_out())

    def test_nram(self):
        clock = ChipClock()
        ram = NRAM(4, clock)

        # load into memory
        expected = [
            int16_as_register(1),
            int16_as_register(2),
            int16_as_register(3),
            int16_as_register(4),
        ]

        ram.set_load(1)

        ram.set_address_bus([0, 0])
        ram.set_input_bus(expected[0])
        clock.tick()

        ram.set_address_bus([0, 1])
        ram.set_input_bus(expected[1])
        clock.tick()

        ram.set_address_bus([1, 0])
        ram.set_input_bus(expected[2])
        clock.tick()

        ram.set_address_bus([1, 1])
        ram.set_input_bus(expected[3])
        clock.tick()

        # Read from each address
        ram.set_address_bus([0, 0])
        self.assertEqual(expected[0], ram.get_output_bus())
        ram.set_address_bus([0, 1])
        self.assertEqual(expected[1], ram.get_output_bus())
        ram.set_address_bus([1, 0])
        self.assertEqual(expected[2], ram.get_output_bus())
        ram.set_address_bus([1, 1])
        self.assertEqual(expected[3], ram.get_output_bus())
