class Node:
    def to_dict(self):
        raise NotImplementedError()

class ProgramNode(Node):
    def __init__(self, statements):
        self.statements = statements
    def to_dict(self):
        return {"type": "Program", "statements": [s.to_dict() for s in self.statements]}

class VarDeclNode(Node):
    def __init__(self, name, value_expr):
        self.name = name
        self.value_expr = value_expr
    def to_dict(self):
        return {"type": "VarDecl", "name": self.name, "value": self.value_expr.to_dict()}

class AssignNode(Node):
    def __init__(self, name, value_expr):
        self.name = name
        self.value_expr = value_expr
    def to_dict(self):
        return {"type": "Assign", "name": self.name, "value": self.value_expr.to_dict()}

class PrintNode(Node):
    def __init__(self, expr):
        self.expr = expr
    def to_dict(self):
        return {"type": "Print", "expr": self.expr.to_dict()}

class IfNode(Node):
    def __init__(self, condition, then_branch, else_branch=None):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch
    def to_dict(self):
        return {
            "type": "If", 
            "condition": self.condition.to_dict(), 
            "then": [s.to_dict() for s in self.then_branch],
            "else": [s.to_dict() for s in self.else_branch] if self.else_branch else None
        }

class WhileNode(Node):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
    def to_dict(self):
        return {
            "type": "While", 
            "condition": self.condition.to_dict(), 
            "body": [s.to_dict() for s in self.body]
        }

class BinaryOpNode(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
    def to_dict(self):
        return {"type": "BinaryOp", "left": self.left.to_dict(), "op": self.op, "right": self.right.to_dict()}

class LiteralNode(Node):
    def __init__(self, value):
        self.value = value
    def to_dict(self):
        return {"type": "Literal", "value": self.value}

class StringNode(Node):
    def __init__(self, value):
        self.value = value
    def to_dict(self):
        return {"type": "String", "value": self.value}

class IdNode(Node):
    def __init__(self, name):
        self.name = name
    def to_dict(self):
        return {"type": "Identifier", "name": self.name}

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self, offset=0):
        if self.pos + offset < len(self.tokens):
            return self.tokens[self.pos + offset]
        return None

    def consume(self, expected_type=None):
        token = self.peek()
        if not token:
            raise Exception("Parser Error: Unexpected end of input")
        if expected_type and token.type != expected_type:
            raise Exception(f"Parser Error: Expected {expected_type}, got {token.type} at {token.line}:{token.column}")
        self.pos += 1
        return token

    def parse(self):
        self.consume('START')
        statements = []
        while self.peek() and self.peek().type != 'END':
            statements.append(self.parse_statement())
        self.consume('END')
        return ProgramNode(statements)

    def parse_statement(self):
        token = self.peek()
        if token.type == 'VAR_DECL':
            self.consume('VAR_DECL')
            id_token = self.consume('ID')
            self.consume('ASSIGN')
            expr = self.parse_expression()
            return VarDeclNode(id_token.value, expr)
        elif token.type == 'ID' and self.peek(1) and self.peek(1).type == 'ASSIGN':
            id_token = self.consume('ID')
            self.consume('ASSIGN')
            expr = self.parse_expression()
            return AssignNode(id_token.value, expr)
        elif token.type == 'PRINT':
            self.consume('PRINT')
            expr = self.parse_expression()
            return PrintNode(expr)
        elif token.type == 'IF':
            self.consume('IF')
            condition = self.parse_expression()
            self.consume('THEN')
            then_branch = []
            while self.peek() and self.peek().type not in ('ELSE', 'END'):
                then_branch.append(self.parse_statement())
            
            else_branch = None
            if self.peek() and self.peek().type == 'ELSE':
                self.consume('ELSE')
                while self.peek() and self.peek().type != 'END':
                    else_branch = else_branch or []
                    else_branch.append(self.parse_statement())
            return IfNode(condition, then_branch, else_branch)
        elif token.type == 'WHILE':
            self.consume('WHILE')
            condition = self.parse_expression()
            self.consume('THEN')
            body = []
            while self.peek() and self.peek().type != 'END':
                # Peek ahead to avoid eating the global END
                if self.peek().type in ('IF', 'WHILE', 'VAR_DECL', 'PRINT', 'ID'):
                     body.append(self.parse_statement())
                else:
                    break
            return WhileNode(condition, body)
        else:
            return self.parse_expression()

    def parse_expression(self):
        node = self.parse_term()
        while self.peek() and (self.peek().type in ('PLUS', 'MINUS') or self.peek().type == 'COMPARE'):
            op_token = self.consume()
            right = self.parse_term()
            node = BinaryOpNode(node, op_token.type if op_token.type != 'COMPARE' else op_token.value, right)
        return node

    def parse_term(self):
        node = self.parse_factor()
        while self.peek() and self.peek().type in ('MULT', 'DIV'):
            op_token = self.consume()
            right = self.parse_factor()
            node = BinaryOpNode(node, op_token.type, right)
        return node

    def parse_factor(self):
        token = self.peek()
        if token.type == 'NUMBER':
            self.consume('NUMBER')
            return LiteralNode(token.value)
        if token.type == 'STRING':
            self.consume('STRING')
            return StringNode(token.value)
        if token.type == 'ID':
            self.consume('ID')
            return IdNode(token.value)
        raise Exception(f"Parser Error: Unexpected token {token.type} at {token.line}:{token.column}")
