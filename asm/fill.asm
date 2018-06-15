// fill.asm
//
// fill screen with black if key is pressed,
// otherwise fill with white.


(GETFILLCOLOR)
    @KBD
    D=M

    // if KBD=0, fillcolor=0(white), else fillcolor=-1(black)
    @FILLWHITE
    D;JEQ

    @FILLBLACK
    0;JMP

(FILLBLACK)
    @fillcolor
    M=-1

    @FILL
    0;JMP

(FILLWHITE)
    @fillcolor
    M=0

    @FILL
    0;JMP

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

    @maxrowaddress  // check if we filled all rows
    D=D-M

    @GETFILLCOLOR    // re-sample keyboard input if done
    D;JGT

    @FILLROW
    0;JMP


(END)
    @END
    0;JMP