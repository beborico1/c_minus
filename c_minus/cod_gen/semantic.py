from globalTypes import *
from symtab import *

Error = False
current_function = None
function_return_type = None
# Agregar un mapeo de ámbitos para rastrear a qué ámbito pertenece cada nodo
node_scope_map = {}

def error(lineno, message):
    """Reportar un error semántico"""
    global Error
    Error = True
    print(f">>> Error semántico en línea {lineno}: {message}")

def warning(lineno, message):
    """Reportar una advertencia semántica"""
    print(f">>> Advertencia en línea {lineno}: {message}")

def traverse(t, preProc, postProc):
    """
    Recorrido genérico del árbol sintáctico:
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
    Marca los nodos compuestos que son cuerpos de función
    para manejar correctamente los ámbitos
    """
    if tree is None:
        return
        
    if tree.nodekind == NodeKind.DeclK and tree.decl == DeclKind.FunK:
        # El primer hijo de una declaración de función es su cuerpo
        if tree.child[0] is not None:
            tree.child[0].is_function_body = True
    
    # Recorrer hijos y hermanos
    for i in range(MAXCHILDREN):
        if tree.child[i] is not None:
            markFunctionBodies(tree.child[i])
    
    if tree.sibling is not None:
        markFunctionBodies(tree.sibling)

def insertNode(t):
    """Inserta nodos en la tabla de símbolos durante la primera pasada"""
    global current_function, function_return_type, Error, node_scope_map
    import symtab
    
    # Registrar el ámbito actual para este nodo
    node_scope_map[id(t)] = symtab.current_scope
    
    if t.nodekind == NodeKind.DeclK:
        if t.decl == DeclKind.VarK:
            # Declaración de variable
            if st_lookup(t.name, current_scope_only=True) is not None:
                error(t.lineno, f"Variable '{t.name}' ya declarada en este ámbito")
            else:
                # Verificar que las variables no sean void
                if t.type == ExpType.Void and not t.is_array:
                    error(t.lineno, f"Variable '{t.name}' no puede ser de tipo void")
                
                # Insertar con tipo correcto
                typ = "int" if t.type == ExpType.Integer else "void"
                attr = {"is_array": t.is_array, "size": t.array_size if t.is_array else None}
                st_insert(t.name, typ, t.lineno, attr)
                
        elif t.decl == DeclKind.FunK:
            # Declaración de función
            if st_lookup(t.name, current_scope_only=True) is not None:
                error(t.lineno, f"Función '{t.name}' ya declarada")
            else:
                # Guardar información sobre la función actual
                current_function = t.name
                function_return_type = t.type
                
                # Crear y registrar la función
                typ = "int" if t.type == ExpType.Integer else "void"
                attr = {"params": t.params, "scope": None}  # Almacenará el ámbito de la función
                st_insert(t.name, typ, t.lineno, attr)
                
                # Crear un nuevo ámbito para la función
                func_scope = st_enter_scope()
                
                # Almacenar el ámbito de la función
                func_sym = st_lookup(t.name)
                if func_sym and func_sym.attr:
                    func_sym.attr["scope"] = func_scope
                
                # Insertar parámetros en el ámbito de la función
                for param in t.params:
                    # Saltar parámetros void sin nombres
                    if not hasattr(param, 'name') or param.name is None:
                        continue
                    
                    # Asegurar que el parámetro tenga atributos apropiados
                    if not hasattr(param, 'type'):
                        param.type = ExpType.Integer
                    if not hasattr(param, 'is_array'):
                        param.is_array = False
                    
                    param_type = "int" if param.type == ExpType.Integer else "void"
                    param_attr = {"is_array": param.is_array}
                    
                    # Insertar parámetro con su número de línea si está disponible
                    param_lineno = param.lineno if hasattr(param, 'lineno') else t.lineno
                    st_insert(param.name, param_type, param_lineno, param_attr)
                
    elif t.nodekind == NodeKind.StmtK:
        # Manejo de sentencias con ámbitos
        if t.stmt == StmtKind.CompoundK:
            # Para bloques compuestos que no son cuerpo de función
            if not hasattr(t, 'is_function_body') or not t.is_function_body:
                st_enter_scope()

def exitScope(t):
    """Maneja la salida de ámbitos durante la primera pasada"""
    global current_function, function_return_type
    
    if t.nodekind == NodeKind.StmtK:
        if t.stmt == StmtKind.CompoundK:
            # Para bloques compuestos que no son cuerpo de función
            if not hasattr(t, 'is_function_body') or not t.is_function_body:
                st_exit_scope()
    
    elif t.nodekind == NodeKind.DeclK:
        if t.decl == DeclKind.FunK:
            # Salir del ámbito de la función
            st_exit_scope()
            current_function = None
            function_return_type = None

def enterScopeForCheck(t):
    """Entrar al ámbito apropiado para verificación de tipos"""
    global current_function, function_return_type
    import symtab
    
    if t.nodekind == NodeKind.DeclK and t.decl == DeclKind.FunK:
        # Almacenar información de la función
        current_function = t.name
        function_return_type = t.type
        
        # Obtener el ámbito de la función desde la tabla de símbolos
        func_sym = st_lookup(t.name)
        if func_sym and func_sym.attr and "scope" in func_sym.attr:
            # Entrar al ámbito de la función
            target_scope = func_sym.attr["scope"]
            # Necesitamos manipular la pila de ámbitos para entrar al ámbito correcto
            symtab.current_scope = target_scope
            if target_scope not in symtab.scope_stack:
                symtab.scope_stack.append(target_scope)
    
    elif t.nodekind == NodeKind.StmtK and t.stmt == StmtKind.CompoundK:
        # Para declaraciones compuestas, verificar si tenemos un ámbito registrado
        node_id = id(t)
        if node_id in node_scope_map:
            target_scope = node_scope_map[node_id]
            symtab.current_scope = target_scope
            if target_scope not in symtab.scope_stack:
                symtab.scope_stack.append(target_scope)

def exitScopeForCheck(t):
    """Salir del ámbito después de la verificación de tipos"""
    global current_function, function_return_type
    import symtab
    
    if t.nodekind == NodeKind.DeclK and t.decl == DeclKind.FunK:
        # Salir del ámbito de la función
        if len(symtab.scope_stack) > 1:
            symtab.scope_stack.pop()
            symtab.current_scope = symtab.scope_stack[-1]
        current_function = None
        function_return_type = None
    
    elif t.nodekind == NodeKind.StmtK and t.stmt == StmtKind.CompoundK:
        # Salir del ámbito de la declaración compuesta
        if not hasattr(t, 'is_function_body') or not t.is_function_body:
            if len(symtab.scope_stack) > 1:
                symtab.scope_stack.pop()
                symtab.current_scope = symtab.scope_stack[-1]

def checkNode(t):
    """Realiza verificación de tipos en un nodo durante la segunda pasada"""
    global Error
    
    if t.nodekind == NodeKind.ExpK:
        checkExp(t)
    elif t.nodekind == NodeKind.StmtK:
        checkStmt(t)
    elif t.nodekind == NodeKind.DeclK:
        checkDecl(t)

def checkExp(t):
    """Verifica tipos para nodos de expresión"""
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
            
        # Establecer el tipo resultante según el operador
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
            
        # Verificar que el índice sea entero
        if t.child[0] is not None:
            idx_type = getattr(t.child[0], 'type', None)
            if idx_type != ExpType.Integer:
                error(t.lineno, "El índice del arreglo debe ser entero")
    
    elif t.exp == ExpKind.CallK:
        # Verificar llamada a función
        sym = st_lookup(t.name)
        if sym is None:
            error(t.lineno, f"Identificador '{t.name}' no declarado")
        else:
            # Verificar parámetros si hay información disponible
            if sym.attr and 'params' in sym.attr:
                expected_params = sym.attr['params']
                
                # Verificar cantidad de argumentos
                arg_count = 0
                arg = t.child[0]
                while arg is not None:
                    arg_count += 1
                    arg = arg.sibling
                
                if arg_count != len(expected_params):
                    error(t.lineno, f"Función '{t.name}' espera {len(expected_params)} argumentos, pero recibió {arg_count}")
                
                # Verificar tipos de argumentos
                arg = t.child[0]
                for i, param in enumerate(expected_params):
                    if arg is None:
                        break
                    
                    # Obtener información del parámetro
                    if hasattr(param, 'type'):
                        # Es un TreeNode
                        param_type = 'int' if param.type == ExpType.Integer else 'void'
                        is_array = param.is_array if hasattr(param, 'is_array') else False
                    else:
                        # Es un diccionario
                        param_type = param.get('type', 'int')
                        is_array = param.get('is_array', False)
                    
                    arg_type = getattr(arg, 'type', None)
                    if param_type == 'int' and arg_type != ExpType.Integer:
                        error(t.lineno, f"Argumento {i+1} debe ser entero")
                    
                    # Si el parámetro es un arreglo
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
        # Verificar que la condición sea booleana o entera
        if t.child[0] is not None:
            cond_type = getattr(t.child[0], 'type', None)
            if cond_type is not None and cond_type != ExpType.Boolean and cond_type != ExpType.Integer:
                error(t.lineno, "La condición del if debe ser booleana o entera")
    
    elif t.stmt == StmtKind.WhileK:
        # Verificar que la condición sea booleana o entera
        if t.child[0] is not None:
            cond_type = getattr(t.child[0], 'type', None)
            if cond_type is not None and cond_type != ExpType.Boolean and cond_type != ExpType.Integer:
                error(t.lineno, "La condición del while debe ser booleana o entera")
    
    elif t.stmt == StmtKind.AssignK:
        # Verificar asignación
        if t.child[0] is None:
            return
            
        if t.child[0].exp == ExpKind.SubscriptK:
            # Asignación a elemento de arreglo
            if t.child[1] is not None:
                # Verificar que el valor asignado sea entero
                val_type = getattr(t.child[1], 'type', None)
                if val_type != ExpType.Integer:
                    error(t.lineno, "Solo se pueden asignar valores enteros a elementos de arreglo")
        
        elif t.child[0].exp == ExpKind.IdK:
            # Asignación a variable
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
            # Retorno vacío, debe ser función void
            if function_return_type != ExpType.Void:
                error(t.lineno, "Retorno sin valor en función no void")
        else:
            # Retorno con valor
            if function_return_type == ExpType.Void:
                error(t.lineno, "Retorno con valor en función void")
            else:
                ret_type = getattr(t.child[0], 'type', None)
                if function_return_type == ExpType.Integer and ret_type != ExpType.Integer:
                    error(t.lineno, "El valor de retorno debe ser entero")

def checkDecl(t):
    """Verifica tipos para nodos de declaración"""
    global Error
    
    if t.decl == DeclKind.VarK:
        # Verificar que las variables no sean void
        if t.type == ExpType.Void and not t.is_array:
            error(t.lineno, f"Variable '{t.name}' no puede ser de tipo void")
    
    elif t.decl == DeclKind.ParamK:
        # Verificar que los parámetros no sean void a menos que sea el único parámetro
        if t.type == ExpType.Void and not t.is_array:
            error(t.lineno, f"Parámetro '{t.name}' no puede ser de tipo void")

def buildSymtab(syntaxTree, imprime=True):
    """
    Construye la tabla de símbolos mediante un recorrido 
    en preorden del árbol sintáctico
    """
    global Error, node_scope_map
    Error = False
    
    # Reiniciar tabla de símbolos
    from symtab import table, scope_stack, current_scope, scope_count
    table.clear()
    scope_stack.clear()
    scope_stack.append(0)
    st_exit_scope()  # Esto reiniciará current_scope a 0
    node_scope_map.clear()
    
    # Registrar funciones predefinidas
    st_insert("input", "int", 0, {"params": []})
    st_insert("output", "void", 0, {"params": [{"name": "x", "type": "int", "is_array": False}]})
    
    # Marcar nodos compuestos que son cuerpos de función
    markFunctionBodies(syntaxTree)
    
    # Primer recorrido: insertar identificadores y manejar ámbitos
    traverse(syntaxTree, insertNode, exitScope)
    
    if imprime:
        printSymTab()
    
    return Error

def typeCheckTraverse(t):
    """Recorrido especial para verificación de tipos que mantiene el contexto de ámbito"""
    if t is None:
        return
    
    # Entrar al ámbito si es necesario
    enterScopeForCheck(t)
    
    # Verificar el nodo
    checkNode(t)
    
    # Procesar hijos
    for i in range(MAXCHILDREN):
        if t.child[i] is not None:
            typeCheckTraverse(t.child[i])
    
    # Salir del ámbito si es necesario
    exitScopeForCheck(t)
    
    # Procesar hermanos
    if t.sibling is not None:
        typeCheckTraverse(t.sibling)

def typeCheck(syntaxTree):
    """
    Realiza la verificación de tipos mediante un recorrido 
    en postorden del árbol sintáctico
    """
    global Error, current_function, function_return_type
    
    # Reiniciar seguimiento de funciones
    current_function = None
    function_return_type = None
    
    # Reiniciar ámbitos para empezar fresco
    from symtab import scope_stack, current_scope
    # Mantener solo el ámbito global
    while len(scope_stack) > 1:
        scope_stack.pop()
    st_exit_scope()  # Reiniciar al ámbito 0
    
    # Hacer un recorrido especial que mantenga el contexto de ámbito
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
        # IMPORTANTE: Inferir tipos antes de la verificación de tipos
        from symtab import inferTypes
        if imprime:
            print("Infiriendo Tipos...")
        inferTypes(syntaxTree)
        
        # Verificar tipos
        if imprime:
            print("Verificando Tipos...")
        typeCheck(syntaxTree)
        if imprime:
            print("Verificación de Tipos Terminada")
    
    if imprime:
        if Error:
            print("=== Análisis semántico completado con errores ===")
        else:
            print("=== Análisis semántico completado exitosamente ===")
    
    return not Error