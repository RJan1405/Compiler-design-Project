import re

class Token:
    def __init__(self, type, value, line, column):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def to_dict(self):
        return {
            "type": self.type, 
            "value": str(self.value), 
            "line": self.line, 
            "column": self.column
        }

    def __repr__(self):
        return f"Token({self.type}, {self.value}, {self.line}:{self.column})"

class Lexer:
    EMOJI_MAP = {
        '🙂': 'START',
        '🔚': 'END',
        '🆕': 'VAR_DECL',
        '📢': 'PRINT',
        '➕': 'PLUS',
        '➖': 'MINUS',
        '✖': 'MULT',
        '➗': 'DIV',
        '❓': 'IF',
        '🔁': 'ELSE',
        '🔄': 'WHILE',
        '➡': 'THEN',
    }

    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.line = 1
        self.column = 1
        self.pos = 0

    def tokenize(self):
        while self.pos < len(self.code):
            char = self.code[self.pos]

            if char.isspace():
                if char == '\n':
                    self.line += 1
                    self.column = 1
                else:
                    self.column += 1
                self.pos += 1
                continue

            # Check for emojis
            found_emoji = False
            for emoji, token_type in self.EMOJI_MAP.items():
                if self.code.startswith(emoji, self.pos):
                    self.tokens.append(Token(token_type, emoji, self.line, self.column))
                    self.pos += len(emoji)
                    self.column += 1
                    found_emoji = True
                    break
            
            if found_emoji:
                continue

            # Check for numbers
            if char.isdigit():
                num_str = ""
                start_col = self.column
                while self.pos < len(self.code) and self.code[self.pos].isdigit():
                    num_str += self.code[self.pos]
                    self.pos += 1
                    self.column += 1
                self.tokens.append(Token('NUMBER', int(num_str), self.line, start_col))
                continue

            # Check for identifiers (variables)
            if char.isalpha():
                id_str = ""
                start_col = self.column
                while self.pos < len(self.code) and (self.code[self.pos].isalnum() or self.code[self.pos] == '_'):
                    id_str += self.code[self.pos]
                    self.pos += 1
                    self.column += 1
                self.tokens.append(Token('ID', id_str, self.line, start_col))
                continue
            
            if char == '=':
                if self.pos + 1 < len(self.code) and self.code[self.pos + 1] == '=':
                    self.tokens.append(Token('COMPARE', '==', self.line, self.column))
                    self.pos += 2
                    self.column += 2
                else:
                    self.tokens.append(Token('ASSIGN', '=', self.line, self.column))
                    self.pos += 1
                    self.column += 1
                continue

            # Comparison
            if char in ('>', '<', '!'):
                op = char
                self.pos += 1
                self.column += 1
                if self.pos < len(self.code) and self.code[self.pos] == '=':
                    op += '='
                    self.pos += 1
                    self.column += 1
                self.tokens.append(Token('COMPARE', op, self.line, self.column - len(op)))
                continue

            # Check for strings
            if char == '"':
                string_val = ""
                start_col = self.column
                self.pos += 1 # Skip starting quote
                self.column += 1
                while self.pos < len(self.code) and self.code[self.pos] != '"':
                    string_val += self.code[self.pos]
                    self.pos += 1
                    self.column += 1
                if self.pos >= len(self.code):
                    raise Exception(f"Lexer Error: Unterminated string at {self.line}:{start_col}")
                self.pos += 1 # Skip closing quote
                self.column += 1
                self.tokens.append(Token('STRING', string_val, self.line, start_col))
                continue

            raise Exception(f"Lexer Error: Unknown character '{char}' at {self.line}:{self.column}")

        return self.tokens
