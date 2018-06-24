import unittest
from assembler.parser import _isACommand, _isCCommand


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