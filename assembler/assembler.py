"""Assemble Hack-assembly files (.asm) into Hack-machine code (.hack).
"""

from assembler.parser import AsmParser, Command, comp_bits, dest_bits, jump_bits
import io


def assemble_file(input_file, output_file):
    """Assemble a Hack-assembly file (.asm) into Hack-machine code (.hack)"""

    with open(input_file, "r") as f:
        asm_string = f.read()

    out_string = assemble(asm_string)
    with open(output_file, "w") as f:
        f.write(out_string)

def assemble(asm_string):
    """Assemble a Hack-assembly string, return Hack-machine code.

    Machine-code format is 16 0s and 1s representing a 16-bit word on
    each line of a file. The line number of a file is the  address of that
    command once loaded into ROM"""

    p = AsmParser(asm_string)

    machine_code = io.StringIO()
    # TODO: this currently does not handle symbols at all (no L-commands, and no A-commands except constants)

    while p.has_more():
        p.advance()
        command_type = p.command_type()
        if command_type is Command.A_COMMAND:
            symbol = p.get_symbol()

            # convert constant to 16-bit address
            try:
                c = int(symbol)
                machine_code.write(_constant_to_binary_string(c))
                machine_code.write("\n")
            except ValueError:
                raise Exception("A-command non-constant symbols not yet supported")

        elif command_type is Command.L_COMMAND:
            raise Exception("L-Command (labels) not yet supported")
        elif command_type is Command.C_COMMAND:
            machine_code.write("111")
            machine_code.write(comp_bits(p.get_comp()))
            machine_code.write(dest_bits(p.get_dest()))
            machine_code.write(jump_bits(p.get_jump()))
            machine_code.write("\n")

    output_string = machine_code.getvalue()
    machine_code.close()
    return output_string


def _write_bits(bits, f):
    for b in bits:
        f.write(str(b))


def _constant_to_binary_string(n):
    """Convert integer constant to 16-bit binary string"""
    if n < 0 or n >= 2**15:
        raise Exception("A-command Constant must be positive integer less than 2**15")

    bs = bin(n)[2:]
    return bs.zfill(16)
