import sys
import os
from Parser import Parser
from CodeWriter import CodeWriter


C_ARITHMETIC = 1
C_PUSH = 2
C_POP = 3
C_LABEL = 4
C_GOTO = 5
C_IF = 6
C_FUNCTION = 7
C_RETURN = 8
C_CALL = 9


VARIABLE_COUNT = 16

def main():
    inputPath = sys.argv[1]

    if os.path.isfile(inputPath):
        output_path = "source.asm"
        code_writer = CodeWriter(output_path)
        code_writer.setFileName(os.path.splitext(os.path.basename(inputPath))[0])
        translate_file(inputPath, code_writer)
        code_writer.close()
    elif os.path.isdir(inputPath):
        translate_dir(inputPath)
    else:
        print("Error")


def translate_file(inputPath, code_writer):
    parser = Parser(inputPath)

    while (parser.hasMoreLines() is True):
        parser.advance()
        commandType = parser.commandType()
        if commandType == C_ARITHMETIC:
            code_writer.writeArithmetic(parser.arg1())
        elif commandType == C_PUSH or commandType == C_POP:
            code_writer.writePushPop(commandType, parser.arg1(), parser.arg2())
        elif commandType == C_LABEL:
            code_writer.writeLabel(parser.arg1())
        elif commandType == C_GOTO:
            code_writer.writeGoto(parser.arg1())
        elif commandType == C_IF:
            code_writer.writeIf(parser.arg1())
        elif commandType == C_FUNCTION:
            code_writer.writeFunction(parser.arg1(), parser.arg2())
        elif commandType == C_RETURN:
            code_writer.writeReturn()
        elif commandType == C_CALL:
            code_writer.writeCall(parser.arg1(), parser.arg2())


def translate_dir(dir_path):
    output_path = "source.asm"

    code_writer = CodeWriter(output_path)

    vm_files = []
    for file_name in os.listdir(dir_path):
        if file_name.endswith(".vm"):
            vm_files.append(os.path.join(dir_path, file_name))

    vm_files.sort()

    for vm_file in vm_files:
        code_writer.setFileName(os.path.splitext(os.path.basename(vm_file))[0])
        translate_file(vm_file, code_writer)

    code_writer.close()
  
       
    



if __name__ == "__main__":
    main()

