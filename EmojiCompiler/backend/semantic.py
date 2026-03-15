from parser import ProgramNode, VarDeclNode, AssignNode, PrintNode, BinaryOpNode, IdNode, IfNode, WhileNode, LiteralNode, StringNode

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}

    def analyze(self, node):
        self.symbol_table = {}
        self.errors = []
        self._visit(node)
        return self.errors, self.symbol_table

    def _visit(self, node):
        if isinstance(node, ProgramNode):
            for stmt in node.statements:
                self._visit(stmt)
        elif isinstance(node, VarDeclNode):
            if node.name in self.symbol_table:
                self.errors.append(f"Semantic Error: Duplicate variable declaration '{node.name}'")
            self.symbol_table[node.name] = "variable"
            self._visit(node.value_expr)
        elif isinstance(node, AssignNode):
            if node.name not in self.symbol_table:
                self.errors.append(f"Semantic Error: Variable '{node.name}' assigned before declaration")
            self._visit(node.value_expr)
        elif isinstance(node, PrintNode):
            self._visit(node.expr)
        elif isinstance(node, BinaryOpNode):
            self._visit(node.left)
            self._visit(node.right)
        elif isinstance(node, IdNode):
            if node.name not in self.symbol_table:
                self.errors.append(f"Semantic Error: Variable '{node.name}' used before declaration")
        elif isinstance(node, IfNode):
            self._visit(node.condition)
            for stmt in node.then_branch: self._visit(stmt)
            if node.else_branch:
                for stmt in node.else_branch: self._visit(stmt)
        elif isinstance(node, WhileNode):
            self._visit(node.condition)
            for stmt in node.body: self._visit(stmt)
        elif isinstance(node, (LiteralNode, StringNode)):
            pass
