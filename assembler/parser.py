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
    def __init__(self, asm_string):
        self._cursor = 0
        self._current_command = None
        self._rawlines = asm_string.splitlines()

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
        return self._cursor < len(self._commands)

    def advance(self):
        self._current_command = self._commands[self._cursor]
        self._cursor += 1

    def get_symbol(self):
        command = self._current_command[0]
        if _isACommand(command):
            # strip leading @ from A-command
            return command[1:]
        elif _isLCommand(command):
            # strip leading/trailing parens from L-command
            return command[1:-1]
        else:
            raise Exception(
                "get_symbol() may only be called when command_type() is A_COMMAND or L_COMMAND"
            )

    def get_dest(self):
        """get the dest mnemonic in the current C-command.
        :returns dest mnemonic ("M", "D", "A", etc) or "null" if no destination present
        :raises Exception if current command is not a C-command
        """

        command = self._current_command[0]
        match = _c_command_regex.fullmatch(command)
        if match is None:
            raise Exception(
                "get_dest() may only be called when command_type() is C_COMMAND"
            )

        dest = match.group("dest")
        if dest is None:
            dest = "null"

        if dest in C_COMMAND_DEST:
            return dest
        else:
            line = self._current_command[1]
            raise Exception(
                f"Unrecognized destination on line {line}: {dest}"
            )

    def get_comp(self):
        """Get the comp mnemonic in the current C-Command.
        :raises Exception if current command is not a C-Command
        """
        command = self._current_command[0]
        match = _c_command_regex.fullmatch(command)
        if match is None:
            raise Exception(
                "get_comp() may only be called when command_type() is C_COMMAND"
            )

        comp = match.group("comp")
        if comp in C_COMMAND_COMP:
            return comp
        else:
            line = self._current_command[1]
            raise Exception(
                f"Unrecognized computation on line {line}: {comp}"
            )

    def get_jump(self):
        """get the jump mnemonic in the current C-command.
        :returns jump mnemonic ("JMP", "JEQ", "JLT", etc) or "null" if no jump
        :raises Exception if current command is not a C-command
        """

        command = self._current_command[0]
        match = _c_command_regex.fullmatch(command)
        if match is None:
            raise Exception(
                "get_jump() may only be called when command_type() is C_COMMAND"
            )

        jump = match.group("jump")
        if jump is None:
            jump = "null"

        if jump in C_COMMAND_JUMP:
            return jump
        else:
            line = self._current_command[1]
            raise Exception(
                f"Unrecognized jump mnemonic on line {line}: {jump}"
            )

    def command_type(self):
        command = self._current_command[0]
        if _isACommand(command):
            return Command.A_COMMAND
        elif _isCCommand(command):
            return Command.C_COMMAND
        elif _isLCommand(command):
            return Command.L_COMMAND
        else:
            line = self._current_command[1]
            raise SyntaxError(f"Unrecognized command on line {line}: {command}")




    def reset(self):
        self.cursor = 0

# A-command @CONSTANT, where constant must be nonnegative decimal integer
_constant_pattern = r"\d+"

# User-defined @SYMBOL where symbol can be letters, digits, underscore, dot,
# dollar sign, colon and may not begin with a digit.
_symbol_pattern = r"[A-z_\.\$:][A-z0-9_\.\$:]*"

# A Command is "@CONSTANT" or "@SYMBOL"
_a_command_regex= re.compile(f"(@{_constant_pattern})|(@{_symbol_pattern})")

_whitespace_regex = re.compile(r"\s+", flags=re.UNICODE)

_c_command_regex = re.compile(r"(?P<dest>(null|[AMD]{1,3})=)?(?P<comp>[AMD01\-+!&|]{1,3})(?P<jump>;(null|[JGTEQLNMP]{3}))?")

# L Command is "(SYMBOL)"
_l_command_regex = re.compile(f"\\({_symbol_pattern}\\)")

def _isACommand(s):
    return _a_command_regex.fullmatch(s) is not None


def _isCCommand(s):
    return _c_command_regex.fullmatch(s) is not None

def _isLCommand(s):
    return _l_command_regex.fullmatch(s) is not None

def _nospace(s):
    """strip ALL whitespace from string"""
    return _whitespace_regex.sub("", s)
