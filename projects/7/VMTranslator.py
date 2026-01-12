import sys
from Parser import Parser
from CodeWriter import CodeWriter


C_ARITHMETIC = 1
C_PUSH = 2
C_POP = 3


VARIABLE_COUNT = 16

def main():
    inputPath = sys.argv[1]
    parser = Parser(inputPath)

    output_path = "Prog.asm"

    codeWriter = CodeWriter(output_path)

    while (parser.hasMoreLines() is True):
        parser.advance()
        commandType = parser.commandType()
        if commandType == C_ARITHMETIC:
            codeWriter.writeArithmetic(parser.arg1())
        elif commandType == C_PUSH or commandType == C_POP:
            codeWriter.writePushPop(commandType, parser.arg1(), parser.arg2())
    
    codeWriter.close()


  
       
    



if __name__ == "__main__":
    main()

