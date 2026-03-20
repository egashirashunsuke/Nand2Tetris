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
        # 名前の衝突を避けるためのid
        self.id = 0
        self.file_name = ''
        self.current_function = ""
        lines = ["@256", "D=A", "@SP", "M=D"]
        self.f.write("\n".join(lines) + "\n")
        self.writeCall("Sys.init", 0)
    
    def setFileName(self, file_name):
        self.file_name = file_name

    # project 7
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
                lines = [f"@{self.file_name}.{index}", "D=M"]
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
                lines = [f"@{self.file_name}.{index}", "M=D"]
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

    def writeLabel(self, label):
        lines = [f"({self.current_function}${label})"]
        self.f.write("\n".join(lines) + "\n")

    def writeGoto(self, label):
        lines = [f"@{self.current_function}${label}", "0;JMP"]
        self.f.write("\n".join(lines) + "\n")
    
    def writeIf(self, label):
        lines = ["@SP", "AM=M-1", "D=M", f"@{self.current_function}${label}", "D;JNE"]
        self.f.write("\n".join(lines) + "\n")

    def writeFunction(self, function_name, n_vars):
        self.current_function = function_name
        lines = [f"({function_name})"]
        for i in range(n_vars):
            lines.extend(["@0", "D=A", "@SP", "A=M", "M=D", "@SP", "M=M+1"])
        self.f.write("\n".join(lines) + "\n")

    def writeReturn(self):
        lines = ["@LCL", "D=M", "@frame", "M=D"]
        lines.extend(["@5", "D=D-A", "A=D", "D=M", "@retAddr", "M=D"])
        lines.extend(["@SP", "AM=M-1", "D=M", "@ARG", "A=M", "M=D"])
        lines.extend(["@ARG", "D=M", "D=D+1", "@SP", "M=D"])
        lines.extend(["@frame", "D=M", "@1", "D=D-A", "A=D", "D=M", "@THAT", "M=D"])
        lines.extend(["@frame", "D=M", "@2", "D=D-A", "A=D", "D=M", "@THIS", "M=D"])
        lines.extend(["@frame", "D=M", "@3", "D=D-A", "A=D", "D=M", "@ARG", "M=D"])
        lines.extend(["@frame", "D=M", "@4", "D=D-A", "A=D", "D=M", "@LCL", "M=D"])
        lines.extend(["@retAddr", "A=M", "0;JMP"] )
        self.f.write("\n".join(lines) + "\n")

    def writeCall(self, function_name, n_args):
        lines = [f"@{self.current_function}$ret.{self.id}", "D=A"]
        self.f.write("\n".join(lines) + "\n")
        self._writePushAsm()
        lines = ["@LCL", "D=M"]
        self.f.write("\n".join(lines) + "\n")
        self._writePushAsm()
        lines = ["@ARG", "D=M"]
        self.f.write("\n".join(lines) + "\n")
        self._writePushAsm()
        lines = ["@THIS", "D=M"]
        self.f.write("\n".join(lines) + "\n")
        self._writePushAsm()
        lines = ["@THAT", "D=M"]
        self.f.write("\n".join(lines) + "\n")
        self._writePushAsm()
        lines = ["@SP", "D=M", "@5", "D=D-A", f"@{n_args}", "D=D-A", "@ARG", "M=D"]
        self.f.write("\n".join(lines) + "\n")
        lines = ["@SP", "D=M", "@LCL", "M=D"]
        self.f.write("\n".join(lines) + "\n")
        lines = [f"@{function_name}", "0;JMP"]
        self.f.write("\n".join(lines) + "\n")
        lines = [f"({self.current_function}$ret.{self.id})"]
        self.f.write("\n".join(lines) + "\n")
        self.id += 1

