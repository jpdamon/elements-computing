import unittest
from assembler.parser import _isACommand, _isCCommand, _isLCommand, Parser, Command


class TestParser(unittest.TestCase):

    def test_is_a_command(self):
        self.assertTrue(_isACommand("@1"), "Constant A-Command")
        self.assertTrue(_isACommand("@1234"), "Constant A-Command")
        self.assertTrue(_isACommand("@i"), "Symbol A-Command")
        self.assertTrue(_isACommand("@$The_co:m12mand"), "Symbol A-Command")

    def test_not_a_command(self):
        self.assertFalse(_isACommand("@-1"), "Negative Constant A-Command")
        self.assertFalse(_isACommand("@12.0"), "Non-decimal A-Command")
        self.assertFalse(_isACommand("@1symbol"), "Symbol starts with digit")
        self.assertFalse(_isACommand("symbol"), "missing @ prefix")
        self.assertFalse(_isACommand("@symb-ol"), "invalid symbol char '-'")

    def test_is_c_command(self):
        # Comp part only
        self.assertTrue(_isCCommand("1"))
        self.assertTrue(_isCCommand("-1"))
        self.assertTrue(_isCCommand("D+1"))
        self.assertTrue(_isCCommand("D&A"))
        self.assertTrue(_isCCommand("-M"))
        self.assertTrue(_isCCommand("M-D"))

        # Comp+jump
        self.assertTrue(_isCCommand("0;JMP"))
        self.assertTrue(_isCCommand("D;JLT"))
        self.assertTrue(_isCCommand("M+1;JLE"))

        # dest+comp
        self.assertTrue(_isCCommand("M=M+1"))
        self.assertTrue(_isCCommand("D=A&M"))
        self.assertTrue(_isCCommand("A=-1"))

        # dest+comp+jump
        self.assertTrue(_isCCommand("D=D|M;JEQ"))

    def test_is_l_command(self):
        self.assertTrue(_isLCommand("(LOOP)"))
        self.assertTrue(_isLCommand("(Symbol)"))
        self.assertTrue(_isLCommand("(Func:A_1)"))

    def test_not_l_command(self):
        self.assertFalse(_isLCommand("@1234"))
        self.assertFalse(_isLCommand("@symbol"))
        self.assertFalse(_isLCommand("(symbol"))
        self.assertFalse(_isLCommand("symbol)"))
        self.assertFalse(_isLCommand("symbol"))

    def test_get_command_type(self):
        asm = """// this is a comment
        
        (LOOP)
            @SCREEN
            M=1
            
            @KBD
            D=M
            
            @LOOP
            D;JLT
            
        (END)
            @END
            0;JMP"""

        p = Parser(asm)

        expected_types = [
            Command.L_COMMAND,  # (LOOP)
            Command.A_COMMAND,  # @SCREEN
            Command.C_COMMAND,  # M=1
            Command.A_COMMAND,  # @KBD
            Command.C_COMMAND,  # D=M
            Command.A_COMMAND,  # @LOOP
            Command.C_COMMAND,  # D;JLT
            Command.L_COMMAND,  # (END)
            Command.A_COMMAND,  # @END
            Command.C_COMMAND   # 0;JMP
        ]

        for command_type in expected_types:
            self.assertTrue(p.has_more())

            p.advance()
            self.assertEqual(command_type, p.command_type())

        self.assertFalse(p.has_more())
