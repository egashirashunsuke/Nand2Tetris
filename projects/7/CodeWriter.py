C_ARITHMETIC = 1
C_PUSH = 2
C_POP = 3

SEG_BASE = {
    "local": "LCL",
    "argument": "ARG",
    "this": "THIS",
    "that": "THAT",
}

class CodeWriter:
   
    def __init__(self,outputPath):
        self.f = open(outputPath, "w", encoding="utf-8")
        self.id = 0

    def writeArithmetic(self, command):
        if command == "add":
            self._writeAdd()
        elif command == "sub":
            self._writeSub()
        elif command == "neg":
            self._writeNeg()
        elif command == "eq":
            self._writeEq()
        elif command == "gt":
            self._writeGt()
        elif command == "lt":
            self._writeLt()
        elif command == "and":
            self._writeAnd()
        elif command == "or":
            self._writeOr()
        elif command == "not":
            self._writeNot()
    
    def writePushPop(self, command, segment, index):
        if command == C_PUSH:
            if segment in ("local", "argument", "this", "that"):
                base = {"local":"LCL","argument":"ARG","this":"THIS","that":"THAT"}[segment]
                lines = [f"@{base}", "D=M", f"@{index}", "D=D+A", "A=D", "D=M"]
                self.f.write("\n".join(lines) + "\n")
                self._writePushAsm()
            elif segment == "pointer":
                base = {0:"THIS",1:"THAT"}[index]
                lines = [f"@{base}", "D=M"]
                self.f.write("\n".join(lines) + "\n")
                self._writePushAsm()
            elif segment == "temp":
                base = 5 + index
                lines = [f"@R{base}", "D=M"]
                self.f.write("\n".join(lines) + "\n")
                self._writePushAsm()
            elif segment == "constant":
                base = index
                lines = [f"@{base}", "D=A"]
                self.f.write("\n".join(lines) + "\n")
                self._writePushAsm()
            else:
                lines = [f"@FileName.{index}", "D=M"]
                self.f.write("\n".join(lines) + "\n")
                self._writePushAsm()
        elif command == C_POP:
            if segment in ("local", "argument", "this", "that"):
                base = {"local":"LCL","argument":"ARG","this":"THIS","that":"THAT"}[segment]
                lines = [f"@{base}", "D=M", f"@{index}", "D=D+A", "@R13", "M=D"]
                self.f.write("\n".join(lines) + "\n")
                self._writePopAsm()
                lines = ["@R13", "A=M", "M=D"]
                self.f.write("\n".join(lines) + "\n")

            elif segment == "pointer":
                base = {0:"THIS",1:"THAT"}[index]
                self._writePopAsm()
                lines = [f"@{base}", "M=D"]
                self.f.write("\n".join(lines) + "\n")

            elif segment == "temp":
                base = 5 + index
                self._writePopAsm()
                lines = [f"@R{base}", "M=D"]
                self.f.write("\n".join(lines) + "\n")
            else:
                self._writePopAsm()
                lines = [f"@FileName.{index}", "M=D"]
                self.f.write("\n".join(lines) + "\n")
                

    def close(self):
        self.f.close()

    def _writeAdd(self):
        self._writePopAsm()
        lines = ["@SP", "AM=M-1", "M=D+M", "@SP", "M=M+1"]
        self.f.write("\n".join(lines) + "\n")
    
    def _writeSub(self):
        self._writePopAsm()
        lines = ["@SP", "AM=M-1", "M=M-D", "@SP", "M=M+1"]
        self.f.write("\n".join(lines) + "\n")

    def _writeNeg(self):
        lines = ["@SP", "AM=M-1", "M=-M", "@SP", "M=M+1"]
        self.f.write("\n".join(lines) + "\n")

    def _writeEq(self):
        self._writePopAsm()
        lines = ["@SP", "AM=M-1", "D=M-D", f"@EQ_TRUE{self.id}", "D;JEQ", "@0", "D=A"]
        self.f.write("\n".join(lines) + "\n")
        self._writePushAsm()
        lines = [f"@EQ_END{self.id}", "0;JMP"]
        self.f.write("\n".join(lines) + "\n")
        lines = [f"(EQ_TRUE{self.id})", "@SP", "A=M", "M=-1", "@SP", "M=M+1", f"(EQ_END{self.id})"]
        self.f.write("\n".join(lines) + "\n")
        self.id += 1

    def _writeGt(self):
        self._writePopAsm()
        lines = ["@SP", "AM=M-1", "D=M-D", f"@GT_TRUE{self.id}", "D;JGT", "@0", "D=A"]
        self.f.write("\n".join(lines) + "\n")
        self._writePushAsm()
        lines = [f"@GT_END{self.id}", "0;JMP"]
        self.f.write("\n".join(lines) + "\n")
        lines = [f"(GT_TRUE{self.id})", "@SP", "A=M", "M=-1", "@SP", "M=M+1", f"(GT_END{self.id})"]
        self.f.write("\n".join(lines) + "\n")
        self.id += 1

    def _writeLt(self):
        self._writePopAsm()
        lines = ["@SP", "AM=M-1", "D=M-D", f"@LT_TRUE{self.id}", "D;JLT", "@0", "D=A"]
        self.f.write("\n".join(lines) + "\n")
        self._writePushAsm()
        lines = [f"@LT_END{self.id}", "0;JMP"]
        self.f.write("\n".join(lines) + "\n")
        lines = [f"(LT_TRUE{self.id})", "@SP", "A=M", "M=-1", "@SP", "M=M+1", f"(LT_END{self.id})"]
        self.f.write("\n".join(lines) + "\n")
        self.id += 1

    def _writeAnd(self):
        self._writePopAsm()
        lines = ["@SP", "AM=M-1", "D=D&M"]
        self.f.write("\n".join(lines) + "\n")
        self._writePushAsm()
       

    def _writeOr(self):
        self._writePopAsm()
        lines = ["@SP", "AM=M-1", "D=D|M"]
        self.f.write("\n".join(lines) + "\n")
        self._writePushAsm()

    def _writeNot(self):
        lines = ["@SP", "AM=M-1", "D=!M"]
        self.f.write("\n".join(lines) + "\n")
        self._writePushAsm()


    def _writePopAsm(self):
        pop = ["@SP", "AM=M-1", "D=M"]
        self.f.write("\n".join(pop) + "\n")
    
    def _writePushAsm(self):
        push = ["@SP", "A=M", "M=D", "@SP", "M=M+1"]
        self.f.write("\n".join(push) + "\n")
    
    def _writeLoop(self):
        loop = ["(END)", "@END", "0;JMP"]
        self.f.write("\n".join(loop) + "\n")


