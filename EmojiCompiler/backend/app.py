from flask import Flask, request, jsonify
from flask_cors import CORS
from lexer import Lexer
from parser import Parser
from semantic import SemanticAnalyzer
from tac import TACGenerator
from codegen import CodeGenerator

app = Flask(__name__)
CORS(app)

@app.route('/compile', methods=['POST'])
def compile_code():
    data = request.json
    emoji_code = data.get('code', '')
    
    try:
        # 1. Lexical Analysis
        lexer = Lexer(emoji_code)
        tokens = lexer.tokenize()
        token_list = [t.to_dict() for t in tokens]
        
        # 2. Syntax Analysis
        parser = Parser(tokens)
        ast = parser.parse()
        ast_dict = ast.to_dict()
        
        # 3. Semantic Analysis
        semantic = SemanticAnalyzer()
        errors, symbol_table = semantic.analyze(ast)
        
        if errors:
            return jsonify({
                "success": False,
                "errors": errors,
                "tokens": token_list,
                "ast": ast_dict
            }), 400
            
        # 4. Intermediate Code Generation (TAC)
        tac_gen = TACGenerator()
        tac_code = tac_gen.generate(ast)
        
        # 5. Final Code Generation (Python)
        codegen = CodeGenerator()
        python_code = codegen.generate(ast)
        
        # 6. Execution (Run the generated code)
        import io
        from contextlib import redirect_stdout
        output_buffer = io.StringIO()
        try:
            with redirect_stdout(output_buffer):
                exec(python_code, {"__builtins__": __builtins__}, {})
            execution_result = output_buffer.getvalue()
        except Exception as e:
            execution_result = f"Runtime Error: {str(e)}"
        
        return jsonify({
            "success": True,
            "python_code": python_code,
            "tac_code": tac_code,
            "tokens": token_list,
            "ast": ast_dict,
            "symbol_table": symbol_table,
            "execution_output": execution_result
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
