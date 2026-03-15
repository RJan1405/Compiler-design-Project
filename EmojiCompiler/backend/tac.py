from parser import ProgramNode, VarDeclNode, AssignNode, PrintNode, BinaryOpNode, IdNode, IfNode, WhileNode, LiteralNode

class TACGenerator:
    def __init__(self):
        self.temp_count = 0
        self.code = []

    def new_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"

    def generate(self, node):
        self.temp_count = 0
        self.code = []
        self._visit(node)
        return self.code

    def _visit(self, node):
        if isinstance(node, ProgramNode):
            for stmt in node.statements:
                self._visit(stmt)
        elif isinstance(node, (VarDeclNode, AssignNode)):
            res = self._visit(node.value_expr)
            self.code.append(f"{node.name} = {res}")
        elif isinstance(node, PrintNode):
            res = self._visit(node.expr)
            self.code.append(f"PRINT {res}")
        elif isinstance(node, BinaryOpNode):
            left = self._visit(node.left)
            right = self._visit(node.right)
            temp = self.new_temp()
            ops = {'PLUS': '+', 'MINUS': '-', 'MULT': '*', 'DIV': '/'}
            op_char = ops.get(node.op, node.op)
            self.code.append(f"{temp} = {left} {op_char} {right}")
            return temp
        elif isinstance(node, LiteralNode):
            return str(node.value)
        elif isinstance(node, IdNode):
            return node.name
        elif isinstance(node, IfNode):
            cond = self._visit(node.condition)
            label_else = f"L{len(self.code)+1}_else"
            label_end = f"L{len(self.code)+2}_end"
            self.code.append(f"IF NOT {cond} GOTO {label_else}")
            for s in node.then_branch: self._visit(s)
            self.code.append(f"GOTO {label_end}")
            self.code.append(f"LABEL {label_else}")
            if node.else_branch:
                for s in node.else_branch: self._visit(s)
            self.code.append(f"LABEL {label_end}")
        elif isinstance(node, WhileNode):
            label_start = f"L{len(self.code)+1}_start"
            label_end = f"L{len(self.code)+2}_end"
            self.code.append(f"LABEL {label_start}")
            cond = self._visit(node.condition)
            self.code.append(f"IF NOT {cond} GOTO {label_end}")
            for s in node.body: self._visit(s)
            self.code.append(f"GOTO {label_start}")
            self.code.append(f"LABEL {label_end}")
