
C_ARITHMETIC = 1
C_PUSH = 2
C_POP = 3
C_LABEL = 4
C_GOTO = 5
C_IF = 6
C_FUNCTION = 7
C_RETURN = 8
C_CALL = 9

class Parser:
    def __init__(self, inputPath):
        with open(inputPath, "r", encoding="utf-8",) as f:
            self.lines = f.readlines()
        
        self.lines_length = len(self.lines)
        self.current_line_index = -1
    
    def hasMoreLines(self):
        if self.current_line_index >= self.lines_length -1:
            return False
        return True
    
    def advance(self):
        self.current_line_index += 1
        is_not_valid_row = 0
        striped_line = self.lines[self.current_line_index].strip()
        if  striped_line == "":
            is_not_valid_row = 1
        if striped_line.startswith("//"):
            is_not_valid_row = 1
        
        while (is_not_valid_row):
            is_not_valid_row = 0
            self.current_line_index += 1
            striped_line = self.lines[self.current_line_index].strip()
            if  striped_line == "":
                is_not_valid_row = 1
            if striped_line.startswith("//"):
                is_not_valid_row = 1

    def commandType(self):
        current_command = self.lines[self.current_line_index].strip()
        command = current_command.split(" ")[0]
        print(repr(command))

        c_arithmetic_command_set = {'add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not'}
        if command in c_arithmetic_command_set:
            return C_ARITHMETIC
        elif command == 'push':
            return C_PUSH
        elif command == 'pop':
            return  C_POP
        elif command == 'label':
            return C_LABEL
        elif command == 'goto':
            return C_GOTO
        elif command == 'if-goto':
            return C_IF
        elif command == 'function':
            return C_FUNCTION
        elif command == 'call':
            return C_CALL
        elif command == 'return':
            return C_RETURN
        return 

    def arg1(self):
        current_command = self.lines[self.current_line_index].strip()
        command = current_command.split(" ")
        if self.commandType() == C_ARITHMETIC:
            return command[0]
        return command[1]

    def arg2(self):
        current_command = self.lines[self.current_line_index]
        command = current_command.split(" ")[2]
        return int(command)
