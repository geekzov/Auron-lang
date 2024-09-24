import re

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f'Token({self.type}, {self.value})'


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0

    def tokenize(self):
        tokens = []
        while self.pos < len(self.text):
            if self.text[self.pos].isspace():
                self.pos += 1
                continue
            elif self.text[self.pos] == '/':
                if self.pos + 1 < len(self.text) and self.text[self.pos + 1] == '/':
                    self.tokenize_comment()  # Handle single-line comments
                    continue
                elif self.pos + 1 < len(self.text) and self.text[self.pos + 1] == '*':
                    self.tokenize_multiline_comment()  # Handle multi-line comments
                    continue
            elif self.text[self.pos].isalpha():
                tokens.append(self.tokenize_identifier())
            elif self.text[self.pos].isdigit():
                tokens.append(self.tokenize_number())
            elif self.text[self.pos] == '"':
                tokens.append(self.tokenize_string())
            elif self.text[self.pos:self.pos + 2] in ['==', '!=', '<=', '>=', '+=', '-=', '*=', '/=']:
                tokens.append(Token('OPERATOR', self.text[self.pos:self.pos + 2]))
                self.pos += 2
            elif self.text[self.pos] in ['+', '-', '*', '/', '=', '<', '>', '(', ')', '{', '}', ';']:
                tokens.append(Token('OPERATOR', self.text[self.pos]))
                self.pos += 1
            else:
                raise ValueError(f"Unexpected character: {self.text[self.pos]} at position {self.pos}")
        return tokens

    def tokenize_identifier(self):
        start = self.pos
        while self.pos < len(self.text) and (self.text[self.pos].isalnum() or self.text[self.pos] == '_'):
            self.pos += 1
        value = self.text[start:self.pos]
        if value in ['if', 'else', 'while', 'for', 'fn', 'return', 'var', 'let', 'const']:
            return Token('KEYWORD', value)
        return Token('IDENTIFIER', value)

    def tokenize_number(self):
        start = self.pos
        while self.pos < len(self.text) and (self.text[self.pos].isdigit() or self.text[self.pos] == '.'):
            self.pos += 1
        return Token('NUMBER', float(self.text[start:self.pos]))

    def tokenize_string(self):
        self.pos += 1  # Skip opening quote
        start = self.pos
        while self.pos < len(self.text) and self.text[self.pos] != '"':
            self.pos += 1
        if self.pos == len(self.text):
            raise ValueError("Unterminated string")
        value = self.text[start:self.pos]
        self.pos += 1  # Skip closing quote
        return Token('STRING', value)

    def tokenize_comment(self):
        self.pos += 2  # Skip '//'
        while self.pos < len(self.text) and self.text[self.pos] != '\n':
            self.pos += 1

    def tokenize_multiline_comment(self):
        self.pos += 2  # Skip '/*'
        while self.pos < len(self.text):
            if self.text[self.pos] == '*' and self.pos + 1 < len(self.text) and self.text[self.pos + 1] == '/':
                self.pos += 2  # Skip '*/'
                return
            self.pos += 1
        raise ValueError("Unterminated multi-line comment")


# Example usage
if __name__ == "__main__":
    sample_code = """
    fn main() {
        var x = 5; // Initialize x
        let y = "Hello, Auron!";
        if (x > 3) {
            print(y);
        }
        /* This is a 
           multi-line comment */
        y += " Welcome!";
    }
    """
    lexer = Lexer(sample_code)
    try:
        tokens = lexer.tokenize()
        for token in tokens:
            print(token)
    except ValueError as e:
        print(f"Error: {e}")
