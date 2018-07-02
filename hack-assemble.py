import sys
from assembler.assembler import assemble_file

if len(sys.argv) != 3:
    print("usage: python hack-assemble.py input.asm output.hack")
    sys.exit(1)

assemble_file(sys.argv[1], sys.argv[2])
