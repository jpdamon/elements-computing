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
            
            // another comment
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

    def test_get_symbol(self):
        asm = """@i
        D=0
        
        @my_var1:1
        M=D
        
        (the_end)
            0;JMP
        """

        p = Parser(asm)
        p.advance()
        self.assertEqual("i", p.get_symbol())
        p.advance()
        with self.assertRaises(Exception):
            # Exception when get_symbol() called on C-Command D=0
            p.get_symbol()
        p.advance()
        self.assertEqual("my_var1:1", p.get_symbol())
        p.advance()
        with self.assertRaises(Exception):
            # Exception when get_symbol() called on C-Command M=D
            p.get_symbol()
        p.advance()
        self.assertEqual("the_end", p.get_symbol())
        p.advance()
        with self.assertRaises(Exception):
            # Exception when get_symbol() called on C-Command 0;JMP
            p.get_symbol()

    def test_get_comp(self):
        asm = """@i
        D=0
        
        @my_var1:1
        M=D+1
        A=D&M
        D=D+A;JLE
        
        (the_end)
            0;JMP
        """

        p = Parser(asm)
        p.advance()
        p.advance()
        self.assertEqual("0", p.get_comp())
        p.advance()
        p.advance()
        self.assertEqual("D+1", p.get_comp())
        p.advance()
        self.assertEqual("D&M", p.get_comp())
        p.advance()
        self.assertEqual("D+A", p.get_comp())
        p.advance()
        p.advance()
        self.assertEqual("0", p.get_comp())

    def test_get_jump(self):
        asm = """@function_a
        D=M;JGE
        A=1
        (function_a)
            D=A+1;JEQ
            D&M;JLT
            
        (END)
            0;JMP"""

        p = Parser(asm)
        p.advance()
        p.advance()
        self.assertEqual("JGE", p.get_jump())
        p.advance()
        self.assertEqual("null", p.get_jump())
        p.advance()
        p.advance()
        self.assertEqual("JEQ", p.get_jump())
        p.advance()
        self.assertEqual("JLT", p.get_jump())
        p.advance()
        p.advance()
        self.assertEqual("JMP", p.get_jump())

    def test_get_dest(self):
        asm = """D+1
        D=1
        M=D+A
        A=1;JLE
        AM=D
        AMD=D&M
        """

        p = Parser(asm)
        p.advance()
        self.assertEqual("null", p.get_dest())
        p.advance()
        self.assertEqual("D", p.get_dest())
        p.advance()
        self.assertEqual("M", p.get_dest())
        p.advance()
        self.assertEqual("A", p.get_dest())
        p.advance()
        self.assertEqual("AM", p.get_dest())
        p.advance()
        self.assertEqual("AMD", p.get_dest())