"""Parse assembly language (.asm) file for Hack computer.

Parse assembly into commands. First step of assembler (parse->code->symbol)
"""
import re
import enum
import string


class Command(enum.Enum):
    A_COMMAND = 1
    C_COMMAND = 2
    L_COMMAND = 3


def comp_bits(s):
    """Get 7 bits for comp part of C-Command s
        :raises KeyError if s is an invalid comp"""
    return C_COMMAND_COMP[s]


def dest_bits(s):
    """Get 3 bits for dest part of C-Command s
        :raises KeyError if s is an invalid dest"""
    return C_COMMAND_DEST[s]


def jump_bits(s):
    """Get 3 bits for jump part of C-Command s
        :raises KeyError if s is an invalid jump"""
    return C_COMMAND_JUMP[s]


# C Command compute mnemonics mapped to a-c bits
C_COMMAND_COMP = {
    #        a  c1 c2 c3 c4 c5 c6
    "0":    "0101010",
    "1":    "0111111",
    "-1":   "0111010",
    "D":    "0001100",
    "A":    "0110000",
    "!D":   "0001101",
    "!A":   "0110001",
    "-D":   "0001111",
    "-A":   "0110011",
    "D+1":  "0011111",
    "A+1":  "0110111",
    "D-1":  "0001110",
    "A-1":  "0110010",
    "D+A":  "0000010",
    "D-A":  "0010011",
    "A-D":  "0000111",
    "D&A":  "0000000",
    "D|A":  "0010101",
    "M":    "1110000",
    "!M":   "1110001",
    "-M":   "1110011",
    "M+1":  "1110111",
    "M-1":  "1110010",
    "D+M":  "1000010",
    "D-M":  "1010011",
    "M-D":  "1000111",
    "D&M":  "1000000",
    "D|M":  "1010101"
}

# C Command destination mnemonics mapped to d bits
C_COMMAND_DEST = {
    #       d1  d2 d3
    "null": "000",
    "M":    "001",
    "D":    "010",
    "MD":   "011",
    "A":    "100",
    "AM":   "101",
    "AD":   "110",
    "AMD":  "111"
}

# C Command jump mnemonics mapped to d bits
C_COMMAND_JUMP = {
    #       j1  j2 j3
    "null": "000",
    "JGT":  "001",
    "JEQ":  "010",
    "JGE":  "011",
    "JLT":  "100",
    "JNE":  "101",
    "JLE":  "110",
    "JMP":  "111"
}


class AsmParser:
    def __init__(self, asm_string):
        self._cursor = 0
        self._current_command = None
        self._rawlines = asm_string.splitlines()

        # list of (command, linenumber) once comments/blanklines removed.
        self._commands = []
        self._get_commands()

    def _get_commands(self):
        """remove spaces, empty lines, and comments, leaving only commands.
        retains actual line numbers for error reporting.
        """

        for i, line in enumerate(self._rawlines):
            command = line

            # if comment is found, remove everything from '//' until end of line.
            comment = command.find("//")
            if comment != -1:
                command = command[:comment]

            # removal of whitespace must come after comment removal to support inline comments
            command = command.strip()
            if command == "":
                # Blank line or comment, ignore
                pass
            else:
                self._commands.append({"command": command, "line": i})

    def has_more(self):
        return self._cursor < len(self._commands)

    def advance(self):
        self._current_command = self._commands[self._cursor]
        self._cursor += 1

    def get_line_number(self):
        return self._current_command["line"]

    def command_type(self):
        # fast return if we already found type of this line
        if "type" in self._current_command:
            return self._current_command["type"]

        command = self._current_command["command"]
        if _is_a_type(command):
            self._current_command["type"] = Command.A_COMMAND
            return Command.A_COMMAND
        elif _is_c_type(command):
            self._current_command["type"] = Command.C_COMMAND
            return Command.C_COMMAND
        elif _is_l_type(command):
            self._current_command["type"] = Command.L_COMMAND
            return Command.L_COMMAND
        else:
            line = self._current_command["line"]
            raise SyntaxError(f"Unrecognized command on line {line}: {command}")

    def get_symbol(self):
        t = self.command_type()
        command = self._current_command["command"]
        if t == Command.A_COMMAND:
            # strip leading @ from A-command
            return command[1:]
        elif t == Command.L_COMMAND:
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

        command = self._current_command["command"]
        t = self.command_type()
        if t is not Command.C_COMMAND:
            raise Exception(
                "get_dest() may only be called when command_type() is C_COMMAND"
            )

        eq = command.find("=")
        if eq == -1:
            dest = "null"
        else:
            dest = command[:eq]

        if dest in C_COMMAND_DEST:
            return dest
        else:
            line = self._current_command["line"]
            raise Exception(
                f"Unrecognized destination on line {line}: {dest}"
            )

    def get_comp(self):
        """Get the comp mnemonic in the current C-Command.
        :raises Exception if current command is not a C-Command
        """
        command = self._current_command["command"]
        t = self.command_type()
        if t is not Command.C_COMMAND:
            raise Exception(
                "get_comp() may only be called when command_type() is C_COMMAND"
            )

        # remove dest part if present
        dest = command.find("=")
        if dest != -1:
            command = command[dest+1:]

        # remove jump part if present
        jmp = command.find(";")
        if jmp != -1:
            command = command[:jmp]

        if command in C_COMMAND_COMP:
            return command
        else:
            line = self._current_command["line"]
            raise Exception(
                f"Unrecognized computation on line {line}: {command}"
            )

    def get_jump(self):
        """get the jump mnemonic in the current C-command.
        :returns jump mnemonic ("JMP", "JEQ", "JLT", etc) or "null" if no jump
        :raises Exception if current command is not a C-command
        """

        command = self._current_command["command"]
        if self.command_type() is not Command.C_COMMAND:
            raise Exception(
                "get_jump() may only be called when command_type() is C_COMMAND"
            )

        jmp = command.find(";")
        if jmp == -1:
            jump = "null"
        else:
            # everything after ';' is jump command
            jump = command[jmp+1:]

        if jump in C_COMMAND_JUMP:
            return jump
        else:
            line = self._current_command["line"]
            raise Exception(
                f"Unrecognized jump mnemonic on line {line}: {jump}"
            )

    def reset(self):
        self._cursor = 0


_whitespace_regex = re.compile(r"\s+", flags=re.UNICODE)

# Generate list of all possible c-commands (8d*28c*8j = 1762) plus their bit string
_VALID_C_COMMANDS = {}
for d in C_COMMAND_DEST.keys():
    for c in C_COMMAND_COMP.keys():
        for j in C_COMMAND_JUMP.keys():
            key = ""
            if d != "null":
                key += d + "="

            key += c
            if j != "null":
                key += ";" + j

            bits = "111" + C_COMMAND_COMP[c] + C_COMMAND_DEST[d] + C_COMMAND_JUMP[j]
            _VALID_C_COMMANDS[key] = bits

_VALID_SYMBOL_CHARS = string.ascii_letters + string.digits + "_.$:"
_VALID_SYMBOL_FIRST_CHAR = string.ascii_letters + "_.$:"


def _is_a_type(s):
    """Check if this is an A-Command, e.g. @Xxx or @123"""
    if len(s) <= 1 or s[0] != "@":
        return False

    if s[1:].isdigit():
        return True
    elif s[1] in _VALID_SYMBOL_FIRST_CHAR:
        for item in s[2:]:
            if item not in _VALID_SYMBOL_CHARS:
                return False

        return True
    else:
        return False


def _is_c_type(s):
    """Check if this is a C-Command, e.g. D=M+1;JMP"""
    return s in _VALID_C_COMMANDS


def _is_l_type(s):
    """Check if this is a L-Command, e.g. (LOOP)"""
    if len(s) < 3 or s[0] != "(" or s[-1] != ")" or s[1] not in _VALID_SYMBOL_FIRST_CHAR:
        return False

    for item in s[2:-2]:
        if item not in _VALID_SYMBOL_CHARS:
            return False

    return True
