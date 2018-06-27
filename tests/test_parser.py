import unittest
from assembler.parser import _is_a_type, _is_c_type, _is_l_type, AsmParser, Command


class TestParser(unittest.TestCase):

    def test_is_a_command(self):
        self.assertTrue(_is_a_type("@1"), "Constant A-Command")
        self.assertTrue(_is_a_type("@1234"), "Constant A-Command")
        self.assertTrue(_is_a_type("@i"), "Symbol A-Command")
        self.assertTrue(_is_a_type("@$The_co:m12mand"), "Symbol A-Command")

    def test_not_a_command(self):
        self.assertFalse(_is_a_type("@-1"), "Negative Constant A-Command")
        self.assertFalse(_is_a_type("@12.0"), "Non-decimal A-Command")
        self.assertFalse(_is_a_type("@1symbol"), "Symbol starts with digit")
        self.assertFalse(_is_a_type("symbol"), "missing @ prefix")
        self.assertFalse(_is_a_type("@symb-ol"), "invalid symbol char '-'")

    def test_is_c_command(self):
        # Comp part only
        self.assertTrue(_is_c_type("1"))
        self.assertTrue(_is_c_type("-1"))
        self.assertTrue(_is_c_type("D+1"))
        self.assertTrue(_is_c_type("D&A"))
        self.assertTrue(_is_c_type("-M"))
        self.assertTrue(_is_c_type("M-D"))

        # Comp+jump
        self.assertTrue(_is_c_type("0;JMP"))
        self.assertTrue(_is_c_type("D;JLT"))
        self.assertTrue(_is_c_type("M+1;JLE"))

        # dest+comp
        self.assertTrue(_is_c_type("M=M+1"))
        self.assertTrue(_is_c_type("A=D&M"))
        self.assertTrue(_is_c_type("A=-1"))

        # dest+comp+jump
        self.assertTrue(_is_c_type("D=D|M;JEQ"))

    def test_is_l_command(self):
        self.assertTrue(_is_l_type("(LOOP)"))
        self.assertTrue(_is_l_type("(Symbol)"))
        self.assertTrue(_is_l_type("(Func:A_1)"))

    def test_not_l_command(self):
        self.assertFalse(_is_l_type("@1234"))
        self.assertFalse(_is_l_type("@symbol"))
        self.assertFalse(_is_l_type("(symbol"))
        self.assertFalse(_is_l_type("symbol)"))
        self.assertFalse(_is_l_type("symbol"))

    def test_get_command_type(self):
        asm = """// this is a comment
        
        (LOOP)
            @SCREEN
            M=1
            
            // another comment
            @KBD
            D=M
            
            @LOOP   // an inline comment
            D;JLT// another inline comment
            
        (END)
            @END
            0;JMP"""

        p = AsmParser(asm)

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

        p = AsmParser(asm)
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

        p = AsmParser(asm)
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

        p = AsmParser(asm)
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

        p = AsmParser(asm)
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