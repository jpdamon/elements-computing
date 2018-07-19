import unittest
from assembler.assembler import assemble


class TestAssembler(unittest.TestCase):
    def test_assembler_a_commands_constants(self):
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

    def test_assembler_a_commands(self):
        asm = """
        @x
        M=1
        @y
        M=0
        @x
        M=0
        """

        expected_output = str(
            "0000000000010000\n"    # create new variable at 16
            "1110111111001000\n"    # M=1
            "0000000000010001\n"    # create new variable at 17
            "1110101010001000\n"    # M=0
            "0000000000010000\n"    # re-use x variable at 16
            "1110101010001000\n"  # M=0

        )

        actual_output = assemble(asm)
        self.assertEqual(expected_output, actual_output)

    def test_assembler_l_commands(self):
        asm = """D=M+1;JGE
        (LOOP)
        MD=1
        @LOOP
        0;JMP
        """
        expected_output = str(
            "1111110111010011\n"    # D=M+1;JGE
            "1110111111011000\n"    # MD=1
            "0000000000000001\n"    # @LOOP points to line 1 (MD=1)
            "1110101010000111\n"    # 0;JMP
        )
        actual_output = assemble(asm)

        self.assertEqual(expected_output, actual_output)

    def test_assembler_c_commands(self):
        self.assertEqual("1111110111010011\n", assemble("D=M+1;JGE"))
        self.assertEqual("1110101010000111\n", assemble("0;JMP"))
        self.assertEqual("1110111111011000\n", assemble("MD=1"))

    def test_assemble_pong(self):
        with open("data/Expected_Pong.hack", "r") as f:
            expected = f.read()

        with open("data/Pong.asm", "r") as f:
            asm_string = f.read()

        actual = assemble(asm_string)
        self.assertEqual(expected, actual, "Compare assembler output to a verified file")


if __name__ == '__main__':
    unittest.main()