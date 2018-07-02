"""Memory chips, including registers & RAM"""
from cpu.gate import *
import math

class ChipClock:
    """Clock for synchronizing chip logic"""

    def __init__(self):
        self.cycle = 0
        self.callbacks = []

    def connect(self, tick_function):
        """Add a no-arg callback that will be invoked on every clock tick"""
        self.callbacks.append(tick_function)

    def tick(self):
        """Advance the clock one-cycle and notify all connected chips """
        for f in self.callbacks:
            f()

        self.cycle += 1


class DataFlipFlop:
    """ Elementary sequential device.
    Output is only changed at each clock cycle
    """

    def __init__(self, clock):
        self.input = 0
        self.output = 0
        clock.connect(self.tick)

    def tick(self):
        self.output = self.input


class BitRegister:
    """Single-bit memory register"""

    def __init__(self, clock):
        self._input = 0
        self._load = 0
        self._dff = DataFlipFlop(clock)

    def set_in(self, value):
        """ Set memory input signal.
        Input is loaded into memory on next clock cycle if the load signal = true
        """
        self._input = value
        self._update()

    def set_load(self, value):
        """ Set load signal.
            Input is loaded into memory on next clock cycle if the load signal = true
            """
        self._load = value
        self._update()

    def _update(self):
        self._dff.input = mux_gate(
            self._dff.output,
            self._input,
            self._load
        )

    def get_out(self):
        return self._dff.output


class Register16:
    """16-bit memory register"""

    def __init__(self, clock):
        self._bitreg = [None]*16
        for i in range(16):
            self._bitreg[i] = BitRegister(clock)

    def set_input(self, input16):
        """set 16-bit input bus"""
        for i in range(16):
            self._bitreg[i].set_in(input16[i])

    def set_load(self, value):
        for i in range(16):
            self._bitreg[i].set_load(value)

    def get_out(self):
        """get 16-bit output bus"""
        output = [None]*16
        for i in range(16):
            output[i] = self._bitreg[i].get_out()

        return output

class NRAM:
    """n 16-bit registers, with access by log(n) bit address

    Unlike RAM8, which is written to be composed of more primitive
    gates to emulate actual hardware, NRAM is backed by traditional python
    data structures to speed things up & is useful for testing.
    Both expose the same interfaces.
    """

    def __init__(self, size, clock):
        if not _is_power_2(size):
            raise ValueError("NRAM size must be power of 2")

        self._size = size
        self._address_bits = int(math.log(size, 2))
        self._registers = []
        for _ in range(size):
            self._registers.append([0]*16)
        self._input_bus = [0]*16
        self._address_bus = [0]*self._address_bits
        self._load_bit = 0
        clock.connect(self._on_tick)

    def set_load(self, v):
        self._load_bit = v

    def set_input_bus(self, bus):
        for i in range(16):
            self._input_bus[i] = bus[i]

    def set_address_bus(self, bus):
        for i in range(self._address_bits):
            self._address_bus[i] = bus[i]

    def set_inputs(self, input_bus, address_bus, load_bit):
        self.set_input_bus(input_bus)
        self.set_address_bus(address_bus)
        self.set_load(load_bit)

    def _on_tick(self):
        # load new input into memory
        if self._load_bit == 1:
            address = self._address_to_index()
            for i in range(16):
                self._registers[address][i] = self._input_bus[i]

    def get_output_bus(self):
        """get output register based on address input"""
        address = self._address_to_index()
        output_bus = [0]*16
        for i in range(16):
            output_bus[i] = self._registers[address][i]

        return output_bus

    def _address_to_index(self):
        multiplier = 1
        index = 0
        for address_bit in range(self._address_bits - 1, -1, -1):
            index += multiplier*self._address_bus[address_bit]
            multiplier *= 2

        return index


def _is_power_2(n):
    return n > 0 and (n & (n-1) == 0)
