"""Parse assembly language (.asm) file for Hack computer.

Parse assembly into commands. First step of assembler (parse->code->symbol)
"""
import re
import enum

class Command(enum.Enum):
    A_COMMAND = 1
    C_COMMAND = 2
    L_COMMAND = 3

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
                self._commands.append( (_nospace(command), i ) )

    def has_more(self):
        return self.cursor < len(self._commands)

    def advance(self):
        self._current_command = self._commands[self._cursor]
        self._cursor += 1

    def command_type(self):
        pass

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


def _isACommand(s):
    return _a_command_regex.fullmatch(s) is not None


def _nospace(s):
    """strip ALL whitespace from string"""
    return _whitespace_regex.sub("", s)
