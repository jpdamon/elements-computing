""" Parse .vm files for use by vm translator
"""
from enum import Enum
import re


# Stack:
#       | ... |
#       | x   |
#       | y   |
# SP->  |     |
_Arithmetic_Commands = Enum( 
    'add',  # x + y
    'sub',  # x - y
    'neg',  # -y
    'eq',   # x = y
    'gt',   # x > y
    'lt',   # x < y
    'and',  # x & y
    'or',   # x | y
    'not'   # !y
    )
    
class VmParser:
    
    def __init__(self, instream):
        self.in = instream
        
    def has_more(self):
        """ Returns True if there are more commands in input"""
        pass
    
    def advance(self):
        """ Read next command from input and makes it the current command."""
        pass
    
    def command_type(self):
        """ Returns the type of the current VM command."""
        pass
    
    def arg1(self):
        """ Get first argument of current command
        
        In the case of C_ARITHMETIC, the command itself (add, sub, etc) is 
        returned. Should not be called if the current command is C_RETURN
        """
        pass
    
    def arg2(self):
        """ Get second argument of current command.
        
        Should only be called if the current command is C_PUSH, C_POP, 
        C_FUNCTION, or C_CALL
        """
        
        
        
def _is_command(s):
    for c in VmCommand:
        match = re.fullmatch(r"\s*" + c + "\s*(?P<arg1>")
    