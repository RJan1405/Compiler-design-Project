from parser import ProgramNode, VarDeclNode, AssignNode, PrintNode, BinaryOpNode, IdNode, IfNode, WhileNode, LiteralNode, StringNode

class CodeGenerator:
    def __init__(self):
        self.indent_level = 0

    def generate(self, node):
        self.indent_level = 0
        return self._visit(node)

    def _visit(self, node):
        indent = "    " * self.indent_level
        if isinstance(node, ProgramNode):
            return "\n".join(self._visit(stmt) for stmt in node.statements)
        elif isinstance(node, (VarDeclNode, AssignNode)):
            return f"{indent}{node.name} = {self._visit(node.value_expr)}"
        elif isinstance(node, PrintNode):
            return f"{indent}print({self._visit(node.expr)})"
        elif isinstance(node, BinaryOpNode):
            ops = {'PLUS': '+', 'MINUS': '-', 'MULT': '*', 'DIV': '/'}
            op_char = ops.get(node.op, node.op)
            return f"({self._visit(node.left)} {op_char} {self._visit(node.right)})"
        elif isinstance(node, LiteralNode):
            return str(node.value)
        elif isinstance(node, StringNode):
            return f'"{node.value}"'
        elif isinstance(node, IdNode):
            return node.name
        elif isinstance(node, IfNode):
            code = f"{indent}if {self._visit(node.condition)}:\n"
            self.indent_level += 1
            code += "\n".join(self._visit(s) for s in node.then_branch)
            self.indent_level -= 1
            if node.else_branch:
                code += f"\n{indent}else:\n"
                self.indent_level += 1
                code += "\n".join(self._visit(s) for s in node.else_branch)
                self.indent_level -= 1
            return code
        elif isinstance(node, WhileNode):
            code = f"{indent}while {self._visit(node.condition)}:\n"
            self.indent_level += 1
            code += "\n".join(self._visit(s) for s in node.body)
            self.indent_level -= 1
            return code
        return ""
