
A_INSTRUCTION = 1
C_INSTRUCTION = 2
L_INSTRUCTION = 3

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

    def instructionType(self):
        striped_line = self.lines[self.current_line_index].strip()
        instruction_type = C_INSTRUCTION
        if  striped_line.startswith("@"):
            instruction_type = A_INSTRUCTION
        if striped_line.startswith("("):
            instruction_type = L_INSTRUCTION
        return instruction_type

    def symbol(self):
        instruction_type = self.instructionType()
        if instruction_type == A_INSTRUCTION:
            command_without_a = self.lines[self.current_line_index].strip()[1:]
            return command_without_a
        if instruction_type == L_INSTRUCTION:
            return self.lines[self.current_line_index].strip()[1:-1]

    def dest(self):
        command = self.lines[self.current_line_index].strip()
        if "=" not in command:
            return None
        command = command.split("=", 1)[0]
        return command
    
    def comp(self):
        command = self.lines[self.current_line_index].strip()

        if "=" in command:
            command = command.split("=", 1)[1]
        if ";" in command:
            command = command.split(";", 1)[0]
        return command

    def jump(self):
        command = self.lines[self.current_line_index].strip()

        if ";" not in command:
            return None
        if "=" in command:
            command = command.split("=", 1)[1]
        if ";" in command:
            command = command.split(";", 1)[1]
        return command
