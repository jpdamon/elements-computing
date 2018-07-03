""" Translate VM commands into Hack assembly code"""

class VmTranslator:
    def __init__(self, outstream):
        self.out = outstream
        
    def start_vmfilename(self, name):
        """ Inform that translation of a new VM file is started"""
        pass
    
    def write_arithmetic(self, command):
        """ Write assembly code equivalent of given arithmetic command"""
        pass
    
    def write_pushpop(self, command_type, segment, index):
        """ Write assembly code equivalent of given C_PUSH or C_POP command"""
        pass
    
    def close(self):
        """ Close output stream"""
        self.out.close()
    
    