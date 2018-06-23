import unittest
from assembler.parser import _isACommand


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
