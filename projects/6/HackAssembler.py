from SymbolTable import SymbolTable
import sys
from Parser import Parser
from Code import Code

A_INSTRUCTION = 1
C_INSTRUCTION = 2
L_INSTRUCTION = 3

VARIABLE_COUNT = 16

def main():
    inputPath = sys.argv[1]
    parser = Parser(inputPath)
    parser2 = Parser(inputPath)

    symbol_table = SymbolTable()

    output_path = "Prog.hack"
    

    count = -1
    while (parser.hasMoreLines() is True):
            parser.advance()
            instruction_type = parser.instructionType()

            if instruction_type != L_INSTRUCTION:
                count += 1
            if instruction_type == L_INSTRUCTION:
                symbol = parser.symbol()
                symbol_table.addEntry(symbol, count+1)
    print(symbol_table.table)

    

    with open(output_path, "w") as f:
        # f.write("hello\n")
        lines = []
        variable_count = VARIABLE_COUNT
        while (parser2.hasMoreLines() is True):
            parser2.advance()
            instruction_type = parser2.instructionType()

            if instruction_type == A_INSTRUCTION:

                if parser2.symbol().isdigit():
                    bin = format(int(parser2.symbol()), '016b')
                    lines.append(str(bin))
                elif symbol_table.contains(parser2.symbol()):
                    combert_number = symbol_table.getAddress(parser2.symbol())
                    bin = format(int(combert_number), '016b')
                    lines.append(str(bin))
                else:
                    symbol_table.addEntry(parser2.symbol(), variable_count)
                    variable_count += 1
                    combert_number = symbol_table.getAddress(parser2.symbol())
                    bin = format(int(combert_number), '016b')
                    lines.append(str(bin))

            if instruction_type == C_INSTRUCTION:
                dest = parser2.dest()
                comp = parser2.comp()
                jump = parser2.jump()
                bin = "111" + Code.comp(comp) + Code.dest(dest)  + Code.jump(jump)
                lines.append(bin)
        f.write("\n".join(lines))
    



if __name__ == "__main__":
    main()

