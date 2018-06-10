// mult.asm
// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

@counter
M=0

@2
M=0

(LOOP)
    @counter
    D=M // D=counter
    @0
    D=D-M   // D=counter-r0
    @END
    D;JGE // If counter >= r0, exit loop

    @1
    D=M // D=R1

    @2
    M=D+M   // Add RAM[1] to total, RAM[0] times

    @counter
    M=M+1   // increment counter

    @LOOP
    0;JMP // Goto LOOP

(END)
    @END
    0;JMP // Stop