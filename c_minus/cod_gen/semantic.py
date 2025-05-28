from globalTypes import *
from symtab import *

Error = False
current_function = None
function_return_type = None
# Add a scope mapping to track which scope each node belongs to
node_scope_map = {}

def error(lineno, message):
    """Reportar un error semantico"""
    global Error
    Error = True
    print(f">>> Error semantico en linea {lineno}: {message}")

def warning(lineno, message):
    """Reportar una advertencia semantica"""
    print(f">>> Advertencia en linea {lineno}: {message}")

def traverse(t, preProc, postProc):
    """
    Recorrido generico del arbol sintactico:
    - preProc se aplica en preorden
    - postProc se aplica en postorden
    """
    if t is not None:
        preProc(t)
        for i in range(MAXCHILDREN):
            traverse(t.child[i], preProc, postProc)
        postProc(t)
        traverse(t.sibling, preProc, postProc)

def nullProc(t):
    """Procedimiento que no hace nada"""
    pass

def markFunctionBodies(tree):
    """
    Marca los nodos compuestos que son cuerpos de funcion
    para manejar correctamente los ambitos
    """
    if tree is None:
        return
        
    if tree.nodekind == NodeKind.DeclK and tree.decl == DeclKind.FunK:
        # El primer hijo de una declaracion de funcion es su cuerpo
        if tree.child[0] is not None:
            tree.child[0].is_function_body = True
    
    # Recorrer hijos y hermanos
    for i in range(MAXCHILDREN):
        if tree.child[i] is not None:
            markFunctionBodies(tree.child[i])
    
    if tree.sibling is not None:
        markFunctionBodies(tree.sibling)

def insertNode(t):
    """Inserta nodos en la tabla de simbolos durante la primera pasada"""
    global current_function, function_return_type, Error, node_scope_map
    import symtab
    
    # Record the current scope for this node
    node_scope_map[id(t)] = symtab.current_scope
    
    if t.nodekind == NodeKind.DeclK:
        if t.decl == DeclKind.VarK:
            # Declaracion de variable
            if st_lookup(t.name, current_scope_only=True) is not None:
                error(t.lineno, f"Variable '{t.name}' ya declarada en este ambito")
            else:
                # Verificar que las variables no sean void
                if t.type == ExpType.Void and not t.is_array:
                    error(t.lineno, f"Variable '{t.name}' no puede ser de tipo void")
                
                # Insertar con tipo correcto
                typ = "int" if t.type == ExpType.Integer else "void"
                attr = {"is_array": t.is_array, "size": t.array_size if t.is_array else None}
                st_insert(t.name, typ, t.lineno, attr)
                
        elif t.decl == DeclKind.FunK:
            # Declaracion de funcion
            if st_lookup(t.name, current_scope_only=True) is not None:
                error(t.lineno, f"Funcion '{t.name}' ya declarada")
            else:
                # Guardar informacion sobre la funcion actual
                current_function = t.name
                function_return_type = t.type
                
                # Crear y registrar la funcion
                typ = "int" if t.type == ExpType.Integer else "void"
                attr = {"params": t.params, "scope": None}  # Will store function's scope
                st_insert(t.name, typ, t.lineno, attr)
                
                # Crear un nuevo ambito para la funcion
                func_scope = st_enter_scope()
                
                # Store the function's scope
                func_sym = st_lookup(t.name)
                if func_sym and func_sym.attr:
                    func_sym.attr["scope"] = func_scope
                
                # Insertar parametros en el ambito de la funcion
                for param in t.params:
                    # Skip void parameters without names
                    if not hasattr(param, 'name') or param.name is None:
                        continue
                    
                    # Ensure param has proper attributes
                    if not hasattr(param, 'type'):
                        param.type = ExpType.Integer
                    if not hasattr(param, 'is_array'):
                        param.is_array = False
                    
                    param_type = "int" if param.type == ExpType.Integer else "void"
                    param_attr = {"is_array": param.is_array}
                    
                    # Insert parameter with its line number if available
                    param_lineno = param.lineno if hasattr(param, 'lineno') else t.lineno
                    st_insert(param.name, param_type, param_lineno, param_attr)
                
    elif t.nodekind == NodeKind.StmtK:
        # Manejo de sentencias con ambitos
        if t.stmt == StmtKind.CompoundK:
            # Para bloques compuestos que no son cuerpo de funcion
            if not hasattr(t, 'is_function_body') or not t.is_function_body:
                st_enter_scope()

def exitScope(t):
    """Maneja la salida de ambitos durante la primera pasada"""
    global current_function, function_return_type
    
    if t.nodekind == NodeKind.StmtK:
        if t.stmt == StmtKind.CompoundK:
            # Para bloques compuestos que no son cuerpo de funcion
            if not hasattr(t, 'is_function_body') or not t.is_function_body:
                st_exit_scope()
    
    elif t.nodekind == NodeKind.DeclK:
        if t.decl == DeclKind.FunK:
            # Salir del ambito de la funcion
            st_exit_scope()
            current_function = None
            function_return_type = None

def enterScopeForCheck(t):
    """Enter appropriate scope for type checking"""
    global current_function, function_return_type
    import symtab
    
    if t.nodekind == NodeKind.DeclK and t.decl == DeclKind.FunK:
        # Store function info
        current_function = t.name
        function_return_type = t.type
        
        # Get the function's scope from symbol table
        func_sym = st_lookup(t.name)
        if func_sym and func_sym.attr and "scope" in func_sym.attr:
            # Enter the function's scope
            target_scope = func_sym.attr["scope"]
            # We need to manipulate the scope stack to enter the right scope
            symtab.current_scope = target_scope
            if target_scope not in symtab.scope_stack:
                symtab.scope_stack.append(target_scope)
    
    elif t.nodekind == NodeKind.StmtK and t.stmt == StmtKind.CompoundK:
        # For compound statements, check if we have a recorded scope
        node_id = id(t)
        if node_id in node_scope_map:
            target_scope = node_scope_map[node_id]
            symtab.current_scope = target_scope
            if target_scope not in symtab.scope_stack:
                symtab.scope_stack.append(target_scope)

def exitScopeForCheck(t):
    """Exit scope after type checking"""
    global current_function, function_return_type
    import symtab
    
    if t.nodekind == NodeKind.DeclK and t.decl == DeclKind.FunK:
        # Exit function scope
        if len(symtab.scope_stack) > 1:
            symtab.scope_stack.pop()
            symtab.current_scope = symtab.scope_stack[-1]
        current_function = None
        function_return_type = None
    
    elif t.nodekind == NodeKind.StmtK and t.stmt == StmtKind.CompoundK:
        # Exit compound statement scope
        if not hasattr(t, 'is_function_body') or not t.is_function_body:
            if len(symtab.scope_stack) > 1:
                symtab.scope_stack.pop()
                symtab.current_scope = symtab.scope_stack[-1]

def checkNode(t):
    """Realiza verificacion de tipos en un nodo durante la segunda pasada"""
    global Error
    
    if t.nodekind == NodeKind.ExpK:
        checkExp(t)
    elif t.nodekind == NodeKind.StmtK:
        checkStmt(t)
    elif t.nodekind == NodeKind.DeclK:
        checkDecl(t)

def checkExp(t):
    """Verifica tipos para nodos de expresion"""
    global Error
    
    if t.exp == ExpKind.OpK:
        # Verificar operadores
        if t.child[0] is None or t.child[1] is None:
            error(t.lineno, "Operador necesita dos operandos")
            t.type = ExpType.Integer  # Asumir tipo por defecto
            return
            
        # Verificar que ambos operandos sean enteros
        left_type = getattr(t.child[0], 'type', None)
        right_type = getattr(t.child[1], 'type', None)
        
        if left_type != ExpType.Integer:
            error(t.lineno, f"Operando izquierdo del operador {t.op.name} debe ser entero")
        if right_type != ExpType.Integer:
            error(t.lineno, f"Operando derecho del operador {t.op.name} debe ser entero")
            
        # Establecer el tipo resultante segun el operador
        if t.op in [TokenType.LT, TokenType.LTE, TokenType.GT, TokenType.GTE, TokenType.EQ, TokenType.NEQ]:
            t.type = ExpType.Boolean
        else:
            t.type = ExpType.Integer
    
    elif t.exp == ExpKind.ConstK:
        # Las constantes ya tienen su tipo asignado
        if not hasattr(t, 'type') or t.type != ExpType.Integer:
            t.type = ExpType.Integer
    
    elif t.exp == ExpKind.IdK:
        # Verificar que el identificador esté declarado
        sym = st_lookup(t.name)
        if sym is None:
            error(t.lineno, f"Identificador '{t.name}' no declarado")
    
    elif t.exp == ExpKind.SubscriptK:
        # Verificar acceso a arreglo
        sym = st_lookup(t.name)
        if sym is None:
            error(t.lineno, f"Identificador '{t.name}' no declarado")
        elif not sym.attr or not sym.attr.get('is_array'):
            error(t.lineno, f"'{t.name}' no es un arreglo")
            
        # Verificar que el indice sea entero
        if t.child[0] is not None:
            idx_type = getattr(t.child[0], 'type', None)
            if idx_type != ExpType.Integer:
                error(t.lineno, "El indice del arreglo debe ser entero")
    
    elif t.exp == ExpKind.CallK:
        # Verificar llamada a funcion
        sym = st_lookup(t.name)
        if sym is None:
            error(t.lineno, f"Identificador '{t.name}' no declarado")
        else:
            # Verificar parametros si hay informacion disponible
            if sym.attr and 'params' in sym.attr:
                expected_params = sym.attr['params']
                
                # Verificar cantidad de argumentos
                arg_count = 0
                arg = t.child[0]
                while arg is not None:
                    arg_count += 1
                    arg = arg.sibling
                
                if arg_count != len(expected_params):
                    error(t.lineno, f"Funcion '{t.name}' espera {len(expected_params)} argumentos, pero recibio {arg_count}")
                
                # Verificar tipos de argumentos
                arg = t.child[0]
                for i, param in enumerate(expected_params):
                    if arg is None:
                        break
                    
                    # Get parameter info
                    if hasattr(param, 'type'):
                        # It's a TreeNode
                        param_type = 'int' if param.type == ExpType.Integer else 'void'
                        is_array = param.is_array if hasattr(param, 'is_array') else False
                    else:
                        # It's a dict
                        param_type = param.get('type', 'int')
                        is_array = param.get('is_array', False)
                    
                    arg_type = getattr(arg, 'type', None)
                    if param_type == 'int' and arg_type != ExpType.Integer:
                        error(t.lineno, f"Argumento {i+1} debe ser entero")
                    
                    # Si el parametro es un arreglo
                    if is_array:
                        if arg.exp != ExpKind.IdK:
                            error(t.lineno, f"Argumento {i+1} debe ser un arreglo")
                        else:
                            arg_sym = st_lookup(arg.name)
                            if arg_sym is None or not arg_sym.attr or not arg_sym.attr.get('is_array'):
                                error(t.lineno, f"Argumento {i+1} debe ser un arreglo")
                    
                    arg = arg.sibling

def checkStmt(t):
    """Verifica tipos para nodos de sentencia"""
    global Error, function_return_type
    
    if t.stmt == StmtKind.IfK:
        # Verificar que la condicion sea booleana o entera
        if t.child[0] is not None:
            cond_type = getattr(t.child[0], 'type', None)
            if cond_type is not None and cond_type != ExpType.Boolean and cond_type != ExpType.Integer:
                error(t.lineno, "La condicion del if debe ser booleana o entera")
    
    elif t.stmt == StmtKind.WhileK:
        # Verificar que la condicion sea booleana o entera
        if t.child[0] is not None:
            cond_type = getattr(t.child[0], 'type', None)
            if cond_type is not None and cond_type != ExpType.Boolean and cond_type != ExpType.Integer:
                error(t.lineno, "La condicion del while debe ser booleana o entera")
    
    elif t.stmt == StmtKind.AssignK:
        # Verificar asignacion
        if t.child[0] is None:
            return
            
        if t.child[0].exp == ExpKind.SubscriptK:
            # Asignacion a elemento de arreglo
            if t.child[1] is not None:
                # Verificar que el valor asignado sea entero
                val_type = getattr(t.child[1], 'type', None)
                if val_type != ExpType.Integer:
                    error(t.lineno, "Solo se pueden asignar valores enteros a elementos de arreglo")
        
        elif t.child[0].exp == ExpKind.IdK:
            # Asignacion a variable
            sym = st_lookup(t.child[0].name)
            if sym is None:
                error(t.lineno, f"Identificador '{t.child[0].name}' no declarado")
            else:
                # Verificar si es un arreglo (no se puede asignar a un arreglo completo)
                if sym.attr and sym.attr.get('is_array'):
                    error(t.lineno, f"No se puede asignar a un arreglo completo '{t.child[0].name}'")
                
                # Verificar tipo
                if t.child[1] is not None:
                    var_type = ExpType.Integer if sym.type_spec == "int" else ExpType.Void
                    val_type = getattr(t.child[1], 'type', None)
                    if var_type == ExpType.Integer and val_type != ExpType.Integer:
                        error(t.lineno, f"No se puede asignar un valor no entero a la variable entera '{t.child[0].name}'")
    
    elif t.stmt == StmtKind.ReturnK:
        # Verificar retorno
        if t.child[0] is None:
            # Retorno vacio, debe ser funcion void
            if function_return_type != ExpType.Void:
                error(t.lineno, "Retorno sin valor en funcion no void")
        else:
            # Retorno con valor
            if function_return_type == ExpType.Void:
                error(t.lineno, "Retorno con valor en funcion void")
            else:
                ret_type = getattr(t.child[0], 'type', None)
                if function_return_type == ExpType.Integer and ret_type != ExpType.Integer:
                    error(t.lineno, "El valor de retorno debe ser entero")

def checkDecl(t):
    """Verifica tipos para nodos de declaracion"""
    global Error
    
    if t.decl == DeclKind.VarK:
        # Verificar que las variables no sean void
        if t.type == ExpType.Void and not t.is_array:
            error(t.lineno, f"Variable '{t.name}' no puede ser de tipo void")
    
    elif t.decl == DeclKind.ParamK:
        # Verificar que los parametros no sean void a menos que sea el unico parametro
        if t.type == ExpType.Void and not t.is_array:
            error(t.lineno, f"Parametro '{t.name}' no puede ser de tipo void")

def buildSymtab(syntaxTree, imprime=True):
    """
    Construye la tabla de simbolos mediante un recorrido 
    en preorden del arbol sintactico
    """
    global Error, node_scope_map
    Error = False
    
    # Reset symbol table
    from symtab import table, scope_stack, current_scope, scope_count
    table.clear()
    scope_stack.clear()
    scope_stack.append(0)
    st_exit_scope()  # This will reset current_scope to 0
    node_scope_map.clear()
    
    # Registrar funciones predefinidas
    st_insert("input", "int", 0, {"params": []})
    st_insert("output", "void", 0, {"params": [{"name": "x", "type": "int", "is_array": False}]})
    
    # Marcar nodos compuestos que son cuerpos de funcion
    markFunctionBodies(syntaxTree)
    
    # Primer recorrido: insertar identificadores y manejar ambitos
    traverse(syntaxTree, insertNode, exitScope)
    
    if imprime:
        printSymTab()
    
    return Error

def typeCheckTraverse(t):
    """Special traversal for type checking that maintains scope context"""
    if t is None:
        return
    
    # Enter scope if needed
    enterScopeForCheck(t)
    
    # Check the node
    checkNode(t)
    
    # Process children
    for i in range(MAXCHILDREN):
        if t.child[i] is not None:
            typeCheckTraverse(t.child[i])
    
    # Exit scope if needed
    exitScopeForCheck(t)
    
    # Process siblings
    if t.sibling is not None:
        typeCheckTraverse(t.sibling)

def typeCheck(syntaxTree):
    """
    Realiza la verificacion de tipos mediante un recorrido 
    en postorden del arbol sintactico
    """
    global Error, current_function, function_return_type
    
    # Reset function tracking
    current_function = None
    function_return_type = None
    
    # Reset scopes to start fresh
    from symtab import scope_stack, current_scope
    # Keep only global scope
    while len(scope_stack) > 1:
        scope_stack.pop()
    st_exit_scope()  # Reset to scope 0
    
    # Do a special traversal that maintains scope context
    typeCheckTraverse(syntaxTree)
    
    return Error

def semantica(syntaxTree, imprime=True):
    """
    Función principal para análisis semántico que combina 
    construcción de tabla de símbolos y verificación de tipos
    """
    global Error
    Error = False
    
    if imprime:
        print("\n=== Iniciando análisis semántico ===")
    
    # Construir tabla de símbolos
    buildSymtab(syntaxTree, imprime)
    
    if not Error:
        # IMPORTANT: Infer types before type checking
        from symtab import inferTypes
        if imprime:
            print("Inferring Types...")
        inferTypes(syntaxTree)
        
        # Verificar tipos
        if imprime:
            print("Checking Types...")
        typeCheck(syntaxTree)
        if imprime:
            print("Type Checking Finished")
    
    if imprime:
        if Error:
            print("=== Análisis semántico completado con errores ===")
        else:
            print("=== Análisis semántico completado exitosamente ===")
    
    return not Error