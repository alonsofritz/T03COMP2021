import sys
import os.path
import string
import terminals
import tokens

""" Classe que representa o analisador léxico """
class Lex():
    
    tokens_list = []

    def __init__(self):
        self.input_file = "test.qsl"
        self.output_file = "lex.txt"

    def isDelimiter(self, char):
        delimiters = "(){}\',;"
        if char in delimiters:
            return True
        return False

    def whatsTypeDelimiter(self, entry):
        d = "(){}\',;"
        pos = d.find(entry)
        return "t10" + str(pos)

    def isLetter (self, char):
        letter = string.ascii_letters
        if char in letter:
            return True
        return False

    def isDigit (self, char):
        digit = '0123456789'
        if char in digit:
            return True
        return False

    def isSymbol(self, char):
        symbols = ''' !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHJKLMNOPQRSTUVXWYZ[\]^_`abcdefghijklmnopqrstuvxwyz{|}~'''
        if(char in symbols):
            return True
        return False

    def isOperator(self, entry):
        operators = '+ - * / % ++ -- == != = > >= < <= ar hela la helaer'.split()
        if entry in operators:
            return True
        return False

    def whatsTypeOperator(self, entry):
        operators = '+ - * / % ++ -- == != = > >= < <= ar hela la helaer'.split()
        pos = 0
        for x in operators:
            if x == entry:
                break
            pos += 1
        
        if(pos > 9):
            return "t4"+str(pos)
        else:
            return "t40"+str(pos)

    def isKeyword(self, entry):
        keywords = "an car cela entulesse ista qui sarme celace hyaline note liltengwa yulmavene true false".split()
        if entry in keywords:
            return True
        return False

    def whatsTypeKeyword(self, entry):
        keywords = "an car cela entulesse ista qui sarme celace hyaline note liltengwa yulmavene true false".split()
        pos = 0
        for x in keywords:
            if x == entry:
                break
            pos += 1

        if(pos > 9):
            return "t2"+str(pos)
        else:
            return "t20"+str(pos)

    def start(self):
        input_file = open(self.input_file, 'r')
        output_file = open(self.output_file, 'w')

        line_number = 1
        current_line = input_file.readline()

        while current_line:
            column = 0
            line_size = len(current_line)

            while column < line_size:
                current_char = current_line[column]
                next_char = None

                if (column + 1) < line_size:
                    next_char = current_line[column+1]
                
                if self.isDelimiter(current_char):
                    output_file.write(
                        terminals.delimiters[self.whatsTypeDelimiter(current_char)] + ", " + 
                        current_char + ", " + 
                        str(line_number) + '\n'
                    )
                
                elif current_char == '-' and next_char == '-':
                    column = line_size

                elif next_char != None and self.isOperator(current_char + next_char):
                    output_file.write(
                        terminals.operators[self.whatsTypeOperator(current_char + next_char)] + ", " +
                        current_char +
                        next_char + ", " +
                        str(line_number) + '\n'
                    )
                    column += 1
                
                elif self.isOperator(current_char):
                    output_file.write(
                        terminals.operators[self.whatsTypeOperator(current_char)] + ", " +
                        current_char + ", " +
                        str(line_number) + '\n'
                    )
        
                elif current_char == string.punctuation[6]:
                    print("Erros...")
                
                # Cadeia de caracteres (string = "abc") ???
                elif current_char == string.punctuation[1]:
                    print("Cadeia de caracteres...")
                
                elif self.isDigit(current_char):
                    tmp = current_char
                    column += 1
                    
                    current_char = current_line[column]
                    while (self.isDigit(current_char) and (column+1 < line_size)):
                        tmp += current_char
                        column += 1
                        current_char = current_line[column]

                    output_file.write(
                        terminals.constants['t301'] + ", " +
                        tmp + ", " +
                        str(line_number) + '\n'
                    )

                    if(not self.isDigit(current_char)):
                        column -= 1

                elif self.isLetter(current_char):
                    tmp = current_char
                    column += 1
                    error = False

                    while column < line_size:
                        next_char = None
                        current_char = current_line[column]

                        if (column + 1) < line_size:
                            next_line = current_line[column + 1]

                        if self.isLetter(current_char) or self.isDigit(current_char) or current_char == '_':
                            tmp += current_char
                        
                        elif self.isDelimiter(current_char) or current_char == ' ' or current_char == '\t' or current_char == '\r':
                            column -= 1
                            break
                        
                        elif next_char != None and self.isOperator(current_char + next_char) or self.isOperator(current_char):
                            column -= 1
                            break

                        elif current_char != '\n':
                            error = True
                            break
                        
                        column += 1
                    
                    if not error:
                        if self.isKeyword(tmp):
                            output_file.write(
                                terminals.keywords[self.whatsTypeKeyword(tmp)] + ", " +
                                tmp + ", " +
                                str(line_number) + '\n'
                            )
                        else:
                            output_file.write(
                                terminals.constants['t300'] + ", " +
                                tmp + ", " +
                                str(line_number) + '\n'
                            )
                    else:
                        print("Error...")

                elif current_char != '\n' and current_char != ' ' and current_char != '\t' and current_char != '\r':
                    print("Erro caractér inválido...")

                column += 1
            
            current_line = input_file.readline()
            line_number += 1
        
        input_file.close()
        output_file.write("$")
        output_file.close()
        self.pushTokens()

    def pushTokens(self):
        f = open(self.output_file, 'r')
        tmp = f.readline()

        while tmp:
            l = tmp.split(", ")
            l[-1] = l[-1].strip()

            if tmp == "$":
                self.tokens_list.append(tmp)
            else:
                self.tokens_list.append(tokens.Token(l[0], l[1], l[2], 0))

            tmp = f.readline()
            
        f.close()
        os.remove(self.output_file)

    def printTokenList(self):
        for x in self.tokens_list:
            print(x)
