# computing

Implementation of the HACK computer, from NAND gates to high-level language. Written with python, and inspired by _The Elements of Computing Systems._

project structure:
<pre>
├── asm: HACK-assembly files
├── assembler: Assemble HACK-assembly files into machine code
├── cpu: HACK cpu architecture including ALU, memory, and logic gates
├── tests: unit tests
</pre>

To use the assembler:
`python hack-assemble.py input.asm output.hack`


For complete HACK computer specification, see [nand2tetris.org](https://www.nand2tetris.org/)


