// fill.asm
//
// fill screen with black if key is pressed,
// otherwise fill with white.

@fillcolor
M=-1 // fill with black for now
// TODO: choose fill color based on keyboard input

(FILL)
    // fill each row based on @fillcolor

    @SCREEN
    D=A

    @rowaddress
    M=D

    @24575
    D=A

    @maxrowaddress
    M=D

    @FILLROW
    0;JMP


(FILLROW)
    @fillcolor  // load color into D
    D=M

    @rowaddress // load current row position into A, fill color at address A
    A=M
    M=D

    @rowaddress // increment row
    M=M+1
    D=M

    // TODO: exit case
    @maxrowaddress  // check if we filled all rows
    D=D-M

    @END
    D;JGT

    @FILLROW
    0;JMP


(END)
    @END
    0;JMP