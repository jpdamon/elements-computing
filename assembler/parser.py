"""Parse assembly language (.asm) file for Hack computer.

Parse assembly into commands. First step of assembler (parse->code->symbol)
"""
import re
import enum


class Command(enum.Enum):
    A_COMMAND = 1
    C_COMMAND = 2
    L_COMMAND = 3

# C Command compute mnemoics mapped to a-c bits
C_COMMAND_COMP = {
    #        a  c1 c2 c3 c4 c5 c6
    "0":    [0, 1, 0, 1, 0, 1, 0],
    "1":    [0, 1, 1, 1, 1, 1, 1],
    "-1":   [0, 1, 1, 1, 0, 1, 0],
    "D":    [0, 0, 0, 1, 1, 0, 0],
    "A":    [0, 1, 1, 0, 0, 0, 0],
    "!D":   [0, 0, 0, 1, 1, 0, 1],
    "!A":   [0, 1, 1, 0, 0, 0, 1],
    "-D":   [0, 0, 0, 1, 1, 1, 1],
    "-A":   [0, 1, 1, 0, 0, 1, 1],
    "D+1":  [0, 0, 1, 1, 1, 1, 1],
    "A+1":  [0, 1, 1, 0, 1, 1, 1],
    "D-1":  [0, 0, 0, 1, 1, 1, 0],
    "A-1":  [0, 1, 1, 0, 0, 1, 0],
    "D+A":  [0, 0, 0, 0, 0, 1, 0],
    "D-A":  [0, 0, 1, 0, 0, 1, 1],
    "A-D":  [0, 0, 0, 0, 1, 1, 1],
    "D&A":  [0, 0, 0, 0, 0, 0, 0],
    "D|A":  [0, 0, 1, 0, 1, 0, 1],
    "M":    [1, 1, 1, 0, 0, 0, 0],
    "!M":   [1, 1, 1, 0, 0, 0, 1],
    "-M":   [1, 1, 1, 0, 0, 1, 1],
    "M+1":  [1, 1, 1, 0, 1, 1, 1],
    "M-1":  [1, 1, 1, 0, 0, 1, 0],
    "D+M":  [1, 0, 0, 0, 0, 1, 0],
    "D-M":  [1, 0, 1, 0, 0, 1, 1],
    "M-D":  [1, 0, 0, 0, 1, 1, 1],
    "D&M":  [1, 0, 0, 0, 0, 0, 0],
    "D|M":  [1, 0, 1, 0, 1, 0, 1]
}

# C Command destination mnemonics mapped to d bits
C_COMMAND_DEST = {
    #       d1  d2 d3
    "null": [0, 0, 0],
    "M":    [0, 0, 1],
    "D":    [0, 1, 0],
    "MD":   [0, 1, 1],
    "A":    [1, 0, 0],
    "AM":   [1, 0, 1],
    "AD":   [1, 1, 0],
    "AMD":  [1, 1, 1]
}

# C Command jump mnemonics mapped to d bits
C_COMMAND_JUMP = {
    #       j1  j2 j3
    "null": [0, 0, 0],
    "JGT":  [0, 0, 1],
    "JEQ":  [0, 1, 0],
    "JGE":  [0, 1, 1],
    "JLT":  [1, 0, 0],
    "JNE":  [1, 0, 1],
    "JLE":  [1, 1, 0],
    "JMP":  [1, 1, 1]
}

class Parser:
    def __init__(self, asmfilename):
        self._cursor = 0
        self._current_command = None
        with open(asmfilename, "r") as f:
            self._rawlines = f.readlines()

        # list of (command, linenumber) once comments/blanklines removed.
        self._commands = []
        self._get_commands()

    def _get_commands(self):
        """remove spaces & empty lines.
        retains actual line numbers for error reporting.
        """

        for i, line in enumerate(self._rawlines):
            command = line.strip()
            if command == "" or command.startswith("//"):
                pass
            else:
                self._commands.append( (command, i ) )

    def has_more(self):
        return self.cursor < len(self._commands)

    def advance(self):
        self._current_command = self._commands[self._cursor]
        self._cursor += 1

    def command_type(self):
        command = self._current_command[0]
        if _isACommand(self._current_command):
            return Command.A_COMMAND
        elif True:
            return Command.C_COMMAND
        elif True:
            return Command.L_COMMAND
        else:
            line = self._current_command[1]
            raise SyntaxError(f"Unrecognized command on line {line}: {command}")




    def reset(self):
        self.cursor = 0

# A-command @CONSTANT, where constant must be nonnegative decimal integer
_constant_pattern = r"@\d+"

# User-defined @SYMBOL where symbol can be letters, digits, underscore, dot,
# dollar sign, colon and may not begin with a digit.
_symbol_pattern = r"@[A-z_\.\$:][A-z0-9_\.\$:]*"

# A Command is "@CONSTANT" or "@SYMBOL"
_a_command_regex= re.compile(f"({_constant_pattern})|({_symbol_pattern})")

_whitespace_regex = re.compile(r"\s+", flags=re.UNICODE)

_c_command_regex = re.compile(r"(?P<dest>(null|[AMD]{1,3})=)?(?P<comp>[AMD01\-+!&|]{1,3})(?P<jump>;(null|[JGTEQLNMP]{3}))?")


def _isACommand(s):
    return _a_command_regex.fullmatch(s) is not None


def _isCCommand(s):
    return _c_command_regex.fullmatch(s) is not None


def _nospace(s):
    """strip ALL whitespace from string"""
    return _whitespace_regex.sub("", s)
