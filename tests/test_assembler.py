import unittest
import time
from assembler.assembler import assemble


class TestAssembler(unittest.TestCase):
    def test_assembler_a_commands(self):
        asm = """
        @0
        @12345
        @32767
        """

        expected_output = str(
            "0000000000000000\n" 
            "0011000000111001\n" 
            "0111111111111111\n"
        )

        actual_output = assemble(asm)
        self.assertEqual(expected_output, actual_output, "A-Commands with constant symbols only")

    def test_assembler_l_commands_not_supported(self):
        with self.assertRaises(Exception):
            assemble("(LOOP)")

    def test_assembler_c_commands(self):
        self.assertEqual("1111110111010011\n", assemble("D=M+1;JGE"))
        self.assertEqual("1110101010000111\n", assemble("0;JMP"))
        self.assertEqual("1110111111011000\n", assemble("MD=1"))

    def test_assemble_pong(self):
        with open("data/PongL.asm", "r") as f:
            asm_string = f.read()

        # check that we can assemble a real program successfully
        start = time.perf_counter()
        output = assemble(asm_string)
        elapsed = time.perf_counter() - start
        print(f"Completed in {elapsed} seconds. Output file size {len(output)}")
