from lexer import Lexer, Token


class Node:
    pass


class VarAssignNode(Node):
    def __init__(self, var_name, value):
        self.var_name = var_name
        self.value = value

    def __repr__(self):
        return f'VarAssignNode({self.var_name}, {self.value})'


class PrintNode(Node):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'PrintNode({self.value})'


class IfNode(Node):
    def __init__(self, condition, then_branch, else_branch=None):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def __repr__(self):
        return f'IfNode({self.condition}, {self.then_branch}, {self.else_branch})'


class FunctionDeclNode(Node):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

    def __repr__(self):
        return f'FunctionDeclNode({self.name}, {self.params}, {self.body})'


class FunctionCallNode(Node):
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments

    def __repr__(self):
        return f'FunctionCallNode({self.name}, {self.arguments})'


class Interpreter:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.variables = {}
        self.functions = {}

    def parse(self):
        nodes = []
        while self.pos < len(self.tokens):
            token = self.tokens[self.pos]
            if token.type == 'KEYWORD' and token.value == 'var':
                self.pos += 1  # Skip 'var'
                var_name = self.tokens[self.pos].value
                self.pos += 1  # Skip variable name
                self.pos += 1  # Skip '='
                value = self.evaluate_expression()
                nodes.append(VarAssignNode(var_name, value))
            elif token.type == 'KEYWORD' and token.value == 'print':
                self.pos += 1  # Skip 'print'
                self.pos += 1  # Skip '('
                value = self.evaluate_expression()
                nodes.append(PrintNode(value))
                self.pos += 1  # Skip ')'
            elif token.type == 'KEYWORD' and token.value == 'if':
                self.pos += 1  # Skip 'if'
                self.pos += 1  # Skip '('
                condition = self.evaluate_expression()
                self.pos += 1  # Skip ')'
                self.pos += 1  # Skip '{'
                then_branch = self.parse()
                else_branch = None
                if self.tokens[self.pos].type == 'KEYWORD' and self.tokens[self.pos].value == 'else':
                    self.pos += 1  # Skip 'else'
                    self.pos += 1  # Skip '{'
                    else_branch = self.parse()
                nodes.append(IfNode(condition, then_branch, else_branch))
                self.pos += 1  # Skip '}'
            elif token.type == 'KEYWORD' and token.value == 'fn':
                self.pos += 1  # Skip 'fn'
                func_name = self.tokens[self.pos].value
                self.pos += 1  # Skip function name
                self.pos += 1  # Skip '('
                params = []
                while self.tokens[self.pos].type == 'IDENTIFIER':
                    params.append(self.tokens[self.pos].value)
                    self.pos += 1
                    if self.tokens[self.pos].value == ',':
                        self.pos += 1  # Skip ','
                self.pos += 1  # Skip ')'
                self.pos += 1  # Skip '{'
                body = self.parse()
                nodes.append(FunctionDeclNode(func_name, params, body))
                self.pos += 1  # Skip '}'
            elif token.type == 'IDENTIFIER':
                func_name = token.value
                self.pos += 1  # Move to next token
                if self.tokens[self.pos].value == '(':
                    self.pos += 1  # Skip '('
                    arguments = []
                    while self.tokens[self.pos].type != 'OPERATOR' or self.tokens[self.pos].value != ')':
                        arguments.append(self.evaluate_expression())
                        if self.tokens[self.pos].value == ',':
                            self.pos += 1  # Skip ','
                    self.pos += 1  # Skip ')'
                    nodes.append(FunctionCallNode(func_name, arguments))
            elif token.type == 'EOF':
                break
            else:
                raise ValueError(f"Unexpected token: {token}")
        return nodes

    def evaluate_expression(self):
        token = self.tokens[self.pos]
        if token.type == 'NUMBER':
            self.pos += 1
            return token.value
        elif token.type == 'STRING':
            self.pos += 1
            return token.value
        elif token.type == 'IDENTIFIER':
            var_name = token.value
            self.pos += 1
            return self.variables.get(var_name, 0)  # Default to 0 if variable not found
        elif token.type == 'OPERATOR' and token.value in ['+', '-', '*', '/']:
            op = token.value
            self.pos += 1  # Move to the next token
            left = self.evaluate_expression()
            right = self.evaluate_expression()
            return self.apply_operator(op, left, right)

        raise ValueError(f"Invalid expression token: {token}")

    def apply_operator(self, op, left, right):
        if op == '+':
            return left + right
        elif op == '-':
            return left - right
        elif op == '*':
            return left * right
        elif op == '/':
            if right == 0:
                raise ValueError("Division by zero error")
            return left / right
        raise ValueError(f"Unknown operator: {op}")

    def run(self, nodes):
        for node in nodes:
            if isinstance(node, VarAssignNode):
                self.variables[node.var_name] = node.value
            elif isinstance(node, PrintNode):
                print(node.value)
            elif isinstance(node, IfNode):
                condition = node.condition
                if condition:
                    self.run(node.then_branch)
                elif node.else_branch:
                    self.run(node.else_branch)
            elif isinstance(node, FunctionDeclNode):
                self.functions[node.name] = node
            elif isinstance(node, FunctionCallNode):
                self.call_function(node)

    def call_function(self, node):
        if node.name not in self.functions:
            raise ValueError(f"Function {node.name} is not defined")
        function = self.functions[node.name]
        if len(node.arguments) != len(function.params):
            raise ValueError(f"Function {node.name} expects {len(function.params)} arguments but got {len(node.arguments)}")
        # Save current variables to restore later
        saved_vars = self.variables.copy()
        # Assign parameters
        for param, arg in zip(function.params, node.arguments):
            self.variables[param] = arg
        self.run(function.body)
        # Restore variables
        self.variables = saved_vars


if __name__ == "__main__":
    sample_code = """
    fn main() {
        var x = 5;
        var y = "Hello, Auron!";
        print(y);
        
        if (x > 3) {
            print("x is greater than 3");
        } else {
            print("x is less than or equal to 3");
        }
        
        fn greet(name) {
            print("Hello, " + name + "!");
        }
        
        greet("World");
    }
    """

    lexer = Lexer(sample_code)
    tokens = lexer.tokenize()
    
    interpreter = Interpreter(tokens)
    nodes = interpreter.parse()
    interpreter.run(nodes)