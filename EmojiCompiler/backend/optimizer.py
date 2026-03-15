class TACOptimizer:
    def optimize(self, tac_code):
        """
        Simple TAC optimizations:
        1. Constant Folding: t1 = 2 + 3  -> t1 = 5
        2. Simple Algebraic Simplification: x = a + 0 -> x = a
        """
        optimized = []
        constants = {} # type: dict

        for line in tac_code:
            if not line or ' = ' not in line:
                optimized.append(line)
                continue

            parts = line.split(' = ')
            if len(parts) < 2:
                optimized.append(line)
                continue
                
            target = parts[0].strip()
            expr = parts[1].strip()
            
            new_line = line
            
            # Check for arithmetic operations
            found_op = False
            for op in [' + ', ' - ', ' * ', ' / ']:
                if op in expr:
                    found_op = True
                    operands = expr.split(op)
                    left = operands[0].strip()
                    right = operands[1].strip()
                    
                    # Replace variables with constants if known
                    l_val = constants.get(left, left)
                    r_val = constants.get(right, right)
                    
                    try:
                        # Try constant folding if both are numeric
                        if self._is_numeric(l_val) and self._is_numeric(r_val):
                            lv = float(l_val)
                            rv = float(r_val)
                            
                            # Use float for division, int otherwise if possible
                            if op.strip() == '/':
                                res = lv / rv
                            else:
                                res = eval(f"{l_val} {op.strip()} {r_val}")
                            
                            new_line = f"{target} = {res}"
                            constants[target] = str(res)
                        else:
                            # Just substitute constants
                            new_line = f"{target} = {l_val} {op.strip()} {r_val}"
                            
                            # Simple algebraic identities
                            if op.strip() == '+' and r_val == '0':
                                new_line = f"{target} = {l_val}"
                            elif op.strip() == '*' and r_val == '1':
                                new_line = f"{target} = {l_val}"
                            elif op.strip() == '*' and r_val == '0':
                                new_line = f"{target} = 0"
                                constants[target] = "0"
                    except:
                        pass
                    break
            
            if not found_op:
                # Single value assignment x = y
                val = expr.strip()
                val = constants.get(val, val)
                if val:
                    new_line = f"{target} = {val}"
                    if self._is_numeric(val) or (isinstance(val, str) and val.startswith('"') and val.endswith('"')):
                        constants[target] = val
            
            optimized.append(new_line)
            
        return optimized

    def _is_numeric(self, s):
        if s is None or not isinstance(s, str): return False
        try:
            float(s)
            return True
        except (ValueError, TypeError):
            return False
