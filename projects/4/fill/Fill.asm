// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.

//// Replace this comment with your code.
(LOOP)
@n
M=0
@512
D=A
@end
M=D
@KBD
D=M
@WHITELOOP
D;JEQ
(BLACKLOOP)
@end
D=M
@n
D=D-M
@LOOP
D;JEQ
@SCREEN
D=A
@n
A=D+M
M=-1
@n
M=M+1
@BLACKLOOP
0;JMP
(WHITELOOP)
@end
D=M
@n
D=D-M
@LOOP
D;JEQ
@SCREEN
D=A
@n
A=D+M
M=0
@n
M=M+1
@WHITELOOP
0;JMP
@SCREEN
M=0
@LOOP
0;JMP