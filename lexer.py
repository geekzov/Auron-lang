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
            current_char = self.text[self.pos]
            
            # Skip whitespace
            if current_char.isspace():
                self.pos += 1
                continue
            
            # Handle comments
            elif current_char == '#':
                self.tokenize_comment()
            
            # Handle identifiers and keywords
            elif current_char.isalpha() or current_char == '_':
                tokens.append(self.tokenize_identifier())
            
            # Handle numbers
            elif current_char.isdigit():
                tokens.append(self.tokenize_number())
            
            # Handle strings
            elif current_char == '"':
                tokens.append(self.tokenize_string())
            
            # Handle multi-character operators
            elif self.text[self.pos:self.pos + 2] in ['==', '!=', '<=', '>=']:
                tokens.append(Token('OPERATOR', self.text[self.pos:self.pos + 2]))
                self.pos += 2
            
            # Handle single-character operators
            elif current_char in ['+', '-', '*', '/', '=', '<', '>', '(', ')', '{', '}', ';']:
                tokens.append(Token('OPERATOR', current_char))
                self.pos += 1
            
            # Handle unexpected characters
            else:
                raise ValueError(f"Unexpected character: {current_char}")
        
        return tokens

    def tokenize_identifier(self):
        start = self.pos
        while self.pos < len(self.text) and (self.text[self.pos].isalnum() or self.text[self.pos] == '_'):
            self.pos += 1
        value = self.text[start:self.pos]
        
        # Check for keywords
        keywords = ['if', 'else', 'while', 'for', 'fn', 'return', 'var', 'let', 'const', 'print']
        if value in keywords:
            return Token('KEYWORD', value)
        return Token('IDENTIFIER', value)

    def tokenize_number(self):
        start = self.pos
        while self.pos < len(self.text) and (self.text[self.pos].isdigit() or self.text[self.pos] == '.'):
            self.pos += 1
        value = self.text[start:self.pos]
        return Token('NUMBER', float(value) if '.' in value else int(value))

    def tokenize_string(self):
        self.pos += 1  # Skip opening quote
        start = self.pos
        while self.pos < len(self.text) and self.text[self.pos] != '"':
            if self.text[self.pos] == '\\':  # Handle escape sequences
                self.pos += 2  # Skip escape character and the next character
            else:
                self.pos += 1
        if self.pos == len(self.text):
            raise ValueError("Unterminated string")
        value = self.text[start:self.pos]
        self.pos += 1  # Skip closing quote
        return Token('STRING', value)

    def tokenize_comment(self):
        while self.pos < len(self.text) and self.text[self.pos] != '\n':
            self.pos += 1  # Skip comment until end of line

# Example usage
if __name__ == "__main__":
    sample_code = """
    fn main() {
        var x = 5;
        let y = "Hello, Auron!";
        # This is a comment
        if (x > 3) {
            print(y);
        }
    }
    """
    lexer = Lexer(sample_code)
    tokens = lexer.tokenize()
    for token in tokens:
        print(token)
