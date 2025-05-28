# analyze.py - Combined semantic analyzer
# Based on bebo's and omar's implementations with fixes

from globalTypes import *
from symtab import *

Error = False
current_function = None
function_return_type = None

def error(lineno, message):
    """Report a semantic error"""
    global Error
    Error = True
    print(f">>> Semantic error on line {lineno}: {message}")

def warning(lineno, message):
    """Report a semantic warning"""
    print(f">>> Warning on line {lineno}: {message}")

def traverse(t, preProc, postProc):
    """
    Generic traversal of the syntax tree:
    - preProc is applied in preorder
    - postProc is applied in postorder
    """
    if t is not None:
        preProc(t)
        for i in range(MAXCHILDREN):
            traverse(t.child[i], preProc, postProc)
        postProc(t)
        traverse(t.sibling, preProc, postProc)

def nullProc(t):
    """Procedure that does nothing"""
    pass

def markFunctionBodies(tree):
    """
    Mark compound nodes that are function bodies
    to correctly handle scopes
    """
    if tree is None:
        return
        
    if tree.nodekind == NodeKind.DeclK and tree.decl == DeclKind.FunK:
        # The first child of a function declaration is its body
        if tree.child[0] is not None:
            tree.child[0].is_function_body = True
    
    # Traverse children and siblings
    for i in range(MAXCHILDREN):
        if tree.child[i] is not None:
            markFunctionBodies(tree.child[i])
    
    if tree.sibling is not None:
        markFunctionBodies(tree.sibling)

def insertNode(t):
    """Insert nodes in the symbol table during the first pass"""
    global current_function, function_return_type, Error
    
    if t.nodekind == NodeKind.DeclK:
        # Handle declarations
        if t.decl == DeclKind.VarK:
            # Variable declaration
            if st_lookup(t.name, current_scope_only=True) is not None:
                error(t.lineno, f"Variable '{t.name}' already declared in this scope")
            else:
                # Check that variables are not void
                if t.type == ExpType.Void and not t.is_array:
                    error(t.lineno, f"Variable '{t.name}' cannot be of type void")
                
                # Insert with correct type
                typ = "int" if t.type == ExpType.Integer else "void"
                st_insert(
                    name=t.name,
                    type_spec=typ,
                    kind='var',
                    lineno=t.lineno,
                    is_array=t.is_array,
                    size=t.array_size if t.is_array else None
                )
                
        elif t.decl == DeclKind.FunK:
            # Function declaration
            if st_lookup(t.name, current_scope_only=True) is not None:
                error(t.lineno, f"Function '{t.name}' already declared")
            else:
                # Save information about the current function
                current_function = t.name
                function_return_type = t.type
                
                # Create and register the function
                typ = "int" if t.type == ExpType.Integer else "void"
                st_insert(
                    name=t.name,
                    type_spec=typ,
                    kind='func',
                    lineno=t.lineno,
                    params=t.params,
                    return_type=t.type
                )
                
                # Create a new scope for the function
                st_enter_scope()
                
                # Insert parameters in the function scope
                for param in t.params:
                    # Check that parameters are not void unless it's the only one
                    if param.type == ExpType.Void and not param.is_array:
                        if len(t.params) > 1:
                            error(param.lineno, f"Parameter '{param.name}' cannot be of type void")
                    
                    param_type = "int" if param.type == ExpType.Integer else "void"
                    st_insert(
                        name=param.name,
                        type_spec=param_type,
                        kind='param',
                        lineno=t.lineno,
                        is_array=param.is_array
                    )
                
    elif t.nodekind == NodeKind.StmtK:
        # Handle statements with scopes
        if t.stmt == StmtKind.CompoundK:
            # For compound blocks that are not function bodies (since those already have their scope)
            if not hasattr(t, 'is_function_body') or t.is_function_body is not True:
                st_enter_scope()
    
    elif t.nodekind == NodeKind.ExpK:
        # For expressions, check that identifiers are declared
        if t.exp == ExpKind.IdK:
            if st_lookup(t.name) is None:
                error(t.lineno, f"Undeclared identifier '{t.name}'")
        elif t.exp == ExpKind.CallK:
            if st_lookup(t.name) is None:
                error(t.lineno, f"Undeclared function '{t.name}'")
        elif t.exp == ExpKind.SubscriptK:
            if st_lookup(t.name) is None:
                error(t.lineno, f"Undeclared array '{t.name}'")

def exitScope(t):
    """Handle scope exit during the first pass"""
    global current_function, function_return_type
    
    if t.nodekind == NodeKind.StmtK:
        if t.stmt == StmtKind.CompoundK:
            # For compound blocks that are not function bodies
            if not hasattr(t, 'is_function_body') or t.is_function_body is not True:
                st_exit_scope()
    
    elif t.nodekind == NodeKind.DeclK:
        if t.decl == DeclKind.FunK:
            # Exit the function scope
            st_exit_scope()
            current_function = None
            function_return_type = None

def checkNode(t):
    """Perform type checking on a node during the second pass"""
    global Error
    
    if t.nodekind == NodeKind.ExpK:
        checkExp(t)
    elif t.nodekind == NodeKind.StmtK:
        checkStmt(t)
    elif t.nodekind == NodeKind.DeclK:
        checkDecl(t)

def checkExp(t):
    """Check types for expression nodes"""
    global Error
    
    if t.exp == ExpKind.OpK:
        # Verify operators
        if t.child[0] is None or t.child[1] is None:
            error(t.lineno, "Operator needs two operands")
            t.type = ExpType.Integer  # Assume default type
            return
            
        # Check operand types
        left_type = t.child[0].type if hasattr(t.child[0], 'type') else ExpType.Integer
        right_type = t.child[1].type if hasattr(t.child[1], 'type') else ExpType.Integer
        
        # Set the resulting type according to the operator
        if t.op in [TokenType.LT, TokenType.LTE, TokenType.GT, TokenType.GTE, TokenType.EQ, TokenType.NEQ]:
            t.type = ExpType.Boolean
        else:
            t.type = ExpType.Integer
    
    elif t.exp == ExpKind.ConstK:
        # Constants are integers in C-
        t.type = ExpType.Integer
    
    elif t.exp == ExpKind.IdK:
        # Look up the identifier in the symbol table
        sym = st_lookup(t.name)
        if sym is not None:
            # Check if it's an array without an index
            if sym.is_array:
                t.type = ExpType.Array
            else:
                t.type = ExpType.Integer if sym.type_spec == "int" else ExpType.Void
        else:
            # This should not happen if insertNode is working correctly
            t.type = ExpType.Void  # Default type if there's an error
    
    elif t.exp == ExpKind.SubscriptK:
        # Check array access
        sym = st_lookup(t.name)
        if sym is not None:
            if not sym.is_array:
                error(t.lineno, f"'{t.name}' is not an array")
                t.type = ExpType.Integer  # Assume default type
            else:
                t.type = ExpType.Integer  # Array elements are integers
                
            # Check that the index is an integer
            if t.child[0] is not None:
                if hasattr(t.child[0], 'type') and t.child[0].type != ExpType.Integer:
                    error(t.lineno, "Array index must be an integer")
        else:
            # This should not happen if insertNode is working correctly
            t.type = ExpType.Integer  # Default type if there's an error
    
    elif t.exp == ExpKind.CallK:
        # Check function call
        sym = st_lookup(t.name)
        if sym is not None:
            if sym.type_spec == "void":
                t.type = ExpType.Void
            else:
                t.type = ExpType.Integer
                
            # Check parameters if information is available
            if sym.params:
                expected_params = sym.params
                
                # Check number of arguments
                arg_count = 0
                arg = t.child[0]
                while arg is not None:
                    arg_count += 1
                    arg = arg.sibling
                
                if arg_count != len(expected_params):
                    error(t.lineno, f"Function '{t.name}' expects {len(expected_params)} arguments, but received {arg_count}")
                
                # Check argument types
                arg = t.child[0]
                for i, param in enumerate(expected_params):
                    if arg is None:
                        break
                    
                    # In C-minus, all arguments should be type integer
                    if hasattr(arg, 'type') and arg.type not in [ExpType.Integer, ExpType.Array]:
                        error(t.lineno, f"Argument {i+1} must be of type integer")
                    
                    # Continue with array checking
                    # Check if param is a dict or a TreeNode
                    if isinstance(param, dict):
                        # If it's a dict, use the 'is_array' key
                        is_array = param.get('is_array', False)
                    else:
                        # If it's a TreeNode, use the is_array attribute
                        is_array = param.is_array if hasattr(param, 'is_array') else False
                    
                    # If the parameter is an array
                    if is_array:
                        if arg.exp != ExpKind.IdK:
                            error(t.lineno, f"Argument {i+1} must be an array")
                        else:
                            arg_sym = st_lookup(arg.name)
                            if arg_sym is None or not arg_sym.is_array:
                                error(t.lineno, f"Argument {i+1} must be an array")
                    
                    arg = arg.sibling
        else:
            # This should not happen if insertNode is working correctly
            t.type = ExpType.Integer  # Default type if there's an error

def checkStmt(t):
    """Check types for statement nodes"""
    global Error, function_return_type
    
    if t.stmt == StmtKind.IfK:
        # Check that the condition is boolean or integer
        if t.child[0] is not None:
            if hasattr(t.child[0], 'type') and t.child[0].type not in [ExpType.Boolean, ExpType.Integer]:
                error(t.lineno, "If condition must be boolean or integer")
    
    elif t.stmt == StmtKind.WhileK:
        # Check that the condition is boolean or integer
        if t.child[0] is not None:
            if hasattr(t.child[0], 'type') and t.child[0].type not in [ExpType.Boolean, ExpType.Integer]:
                error(t.lineno, "While condition must be boolean or integer")
    
    elif t.stmt == StmtKind.AssignK:
        # Check assignment
        if t.child[0] is None:
            return
            
        if t.child[0].exp == ExpKind.SubscriptK:
            # Assignment to array element
            sym = st_lookup(t.child[0].name)
            if sym is None:
                # This should not happen if insertNode is working correctly
                return
            
            if not sym.is_array:
                error(t.lineno, f"Cannot index non-array variable '{t.child[0].name}'")
            
            # Check assignment type
            if t.child[1] is not None:
                if hasattr(t.child[1], 'type') and t.child[1].type not in [ExpType.Integer, ExpType.Boolean]:
                    error(t.lineno, "Cannot assign non-integer value to array element")
        
        elif t.child[0].exp == ExpKind.IdK:
            # Assignment to variable
            sym = st_lookup(t.child[0].name)
            if sym is None:
                # This should not happen if insertNode is working correctly
                return
                
            # Check if it's an array (cannot assign to an entire array)
            if sym.is_array:
                error(t.lineno, f"Cannot assign to entire array '{t.child[0].name}'")
            
            # Check type
            if t.child[1] is not None:
                if hasattr(t.child[1], 'type') and t.child[1].type not in [ExpType.Integer, ExpType.Boolean]:
                    error(t.lineno, f"Cannot assign non-integer value to integer variable '{t.child[0].name}'")
    
    elif t.stmt == StmtKind.ReturnK:
        # Check return
        if t.child[0] is None:
            # Empty return, should be a void function
            if function_return_type != ExpType.Void:
                error(t.lineno, "Return without value in non-void function")
        else:
            # Return with value
            if function_return_type == ExpType.Void:
                error(t.lineno, "Return with value in void function")
            else:
                # Check return value type
                if hasattr(t.child[0], 'type') and t.child[0].type != ExpType.Integer:
                    error(t.lineno, "Return value must be integer")

def checkDecl(t):
    """Check types for declaration nodes"""
    global Error
    
    if t.decl == DeclKind.VarK:
        # Check that variables are not void
        if t.type == ExpType.Void and not t.is_array:
            error(t.lineno, f"Variable '{t.name}' cannot be of type void")
    
    elif t.decl == DeclKind.ParamK:
        # Check that parameters are not void unless it's the only parameter
        if t.type == ExpType.Void and not t.is_array:
            error(t.lineno, f"Parameter '{t.name}' cannot be of type void")

def buildSymtab(syntaxTree, imprime=True):
    """
    Build the symbol table through a preorder traversal
    of the syntax tree
    """
    global Error
    Error = False
    
    # Register predefined functions
    st_insert("input", "int", 'func', 0, params=[], return_type=ExpType.Integer)
    st_insert("output", "void", 'func', 0, params=[{"name": "x", "type": ExpType.Integer, "is_array": False}], return_type=ExpType.Void)
    
    # Mark compound nodes that are function bodies
    markFunctionBodies(syntaxTree)
    
    # First traversal: insert identifiers and handle scopes
    traverse(syntaxTree, insertNode, exitScope)
    
    if imprime:
        printSymTab()
    
    return Error

def typeCheck(syntaxTree):
    """
    Perform type checking through a postorder traversal
    of the syntax tree
    """
    global Error
    
    # Second traversal: check types
    traverse(syntaxTree, nullProc, checkNode)
    
    return Error

def semantica(syntaxTree, imprime=True):
    """Main function: build symbol table + type checking (with error detection)"""
    errores_symtab = buildSymtab(syntaxTree, imprime)
    errores_type = typeCheck(syntaxTree)
    return errores_symtab or errores_type 