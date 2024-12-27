import ast
import inspect
from functools import wraps

def autoreturn(func):
    """
    Decorator that automatically returns the last expression in a function.
    """
    # Get function source and dedent it
    source_lines = inspect.getsourcelines(func)[0]
    source = ''.join(source_lines)
    
    # Parse the source into an AST
    parsed = ast.parse(source)
    
    # Find the function definition node
    function_def = parsed.body[0]
    
    # Check if the last statement is an expression that could be returned
    if function_def.body and isinstance(function_def.body[-1], ast.Expr):
        # Create a modified copy of the function's body
        new_body = function_def.body[:-1]
        
        # Convert the last expression into a return statement
        last_expr = function_def.body[-1].value
        return_stmt = ast.Return(value=last_expr)
        ast.copy_location(return_stmt, function_def.body[-1])
        new_body.append(return_stmt)
        
        # Create a new function definition with the modified body
        new_function_def = ast.FunctionDef(
            name=function_def.name,
            args=function_def.args,
            body=new_body,
            decorator_list=[],
            returns=function_def.returns if hasattr(function_def, 'returns') else None
        )
        ast.copy_location(new_function_def, function_def)
        
        # Create a new module with the modified function
        new_module = ast.Module(body=[new_function_def], type_ignores=[])
        ast.fix_missing_locations(new_module)
        
        # Compile and execute the new function
        code = compile(new_module, filename="<ast>", mode="exec")
        namespace = {}
        exec(code, func.__globals__, namespace)
        
        # Return the new function with the original metadata
        new_func = namespace[func.__name__]
        return wraps(func)(new_func)
    
    # If the last statement isn't an expression, return the original function
    return func

