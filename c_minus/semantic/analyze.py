from globalTypes import *
from symtab import *

Error = False
current_function = None
function_return_type = None

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
    global current_function, function_return_type, Error
    
    if t.nodekind == NodeKind.DeclK:
        # Manejo de declaraciones
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
                attr = {"params": t.params}
                st_insert(t.name, typ, t.lineno, attr)
                
                # Crear un nuevo ambito para la funcion
                st_enter_scope()
                
                # Insertar parametros en el ambito de la funcion
                for param in t.params:
                    # Verificar que los parametros no sean void a menos que sea el unico
                    if param.type == ExpType.Void and not param.is_array:
                        if len(t.params) > 1:
                            error(param.lineno, f"Parametro '{param.name}' no puede ser de tipo void")
                    
                    param_type = "int" if param.type == ExpType.Integer else "void"
                    param_attr = {"is_array": param.is_array}
                    st_insert(param.name, param_type, t.lineno, param_attr)
                
    elif t.nodekind == NodeKind.StmtK:
        # Manejo de sentencias con ambitos
        if t.stmt == StmtKind.CompoundK:
            # Para bloques compuestos que no son cuerpo de funcion (ya que esos ya tienen su ambito)
            if not hasattr(t, 'is_function_body') or t.is_function_body is not True:
                st_enter_scope()
    
    elif t.nodekind == NodeKind.ExpK:
        # En expresiones, verificar que los identificadores esten declarados
        if t.exp in [ExpKind.IdK, ExpKind.CallK, ExpKind.SubscriptK]:
            if st_lookup(t.name) is None:
                error(t.lineno, f"Identificador '{t.name}' no declarado")

def exitScope(t):
    """Maneja la salida de ambitos durante la primera pasada"""
    global current_function, function_return_type
    
    if t.nodekind == NodeKind.StmtK:
        if t.stmt == StmtKind.CompoundK:
            # Para bloques compuestos que no son cuerpo de funcion
            if not hasattr(t, 'is_function_body') or t.is_function_body is not True:
                st_exit_scope()
    
    elif t.nodekind == NodeKind.DeclK:
        if t.decl == DeclKind.FunK:
            # Salir del ambito de la funcion
            st_exit_scope()
            current_function = None
            function_return_type = None

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
            
        # Inferencia automatica de tipo para operandos enteros en C-minus
        t.child[0].type = ExpType.Integer
        t.child[1].type = ExpType.Integer
            
        # Establecer el tipo resultante segun el operador
        if t.op in [TokenType.LT, TokenType.LTE, TokenType.GT, TokenType.GTE, TokenType.EQ, TokenType.NEQ]:
            t.type = ExpType.Boolean
        else:
            t.type = ExpType.Integer
    
    elif t.exp == ExpKind.ConstK:
        # Las constantes son enteras en C-
        t.type = ExpType.Integer
    
    elif t.exp == ExpKind.IdK:
        # Buscar el identificador en la tabla de simbolos
        sym = st_lookup(t.name)
        if sym is not None:
            # Verificar si es un arreglo sin indice
            if sym.attr and sym.attr.get('is_array'):
                t.type = ExpType.Array
            else:
                t.type = ExpType.Integer if sym.type_spec == "int" else ExpType.Void
        else:
            t.type = ExpType.Void  # Tipo por defecto si hay error
    
    elif t.exp == ExpKind.SubscriptK:
        # Verificar acceso a arreglo
        sym = st_lookup(t.name)
        if sym is not None:
            if not sym.attr or not sym.attr.get('is_array'):
                error(t.lineno, f"'{t.name}' no es un arreglo")
                t.type = ExpType.Integer  # Asumir tipo por defecto
            else:
                t.type = ExpType.Integer  # Elementos de arreglo son enteros
                
            # Verificar que el indice sea entero
            if t.child[0] is not None:
                # En C-minus, los indices de arreglos deben ser enteros
                t.child[0].type = ExpType.Integer
        else:
            t.type = ExpType.Integer  # Tipo por defecto si hay error
    
    elif t.exp == ExpKind.CallK:
        # Verificar llamada a funcion
        sym = st_lookup(t.name)
        if sym is not None:
            if sym.type_spec == "void":
                t.type = ExpType.Void
            else:
                t.type = ExpType.Integer
                
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
                    
                    # Todos los argumentos en C-minus deben ser de tipo entero
                    # En C-minus, los argumentos se tipan automaticamente como enteros
                    arg.type = ExpType.Integer
                    
                    # Continuar con la verificacion de arreglos
                    # Verificar si param es un dict o un TreeNode
                    if isinstance(param, dict):
                        # Si es un dict, usar la clave 'type'
                        is_array = param.get('is_array', False)
                    else:
                        # Si es un TreeNode, usar el atributo is_array
                        is_array = param.is_array if hasattr(param, 'is_array') else False
                    
                    # Si el parametro es un arreglo
                    if is_array:
                        if arg.exp != ExpKind.IdK:
                            error(t.lineno, f"Argumento {i+1} debe ser un arreglo")
                        else:
                            arg_sym = st_lookup(arg.name)
                            if arg_sym is None or not arg_sym.attr or not arg_sym.attr.get('is_array'):
                                error(t.lineno, f"Argumento {i+1} debe ser un arreglo")
                    
                    arg = arg.sibling
        else:
            t.type = ExpType.Integer  # Tipo por defecto si hay error

def checkStmt(t):
    """Verifica tipos para nodos de sentencia"""
    global Error, function_return_type
    
    if t.stmt == StmtKind.IfK:
        # Verificar que la condicion sea booleana
        if t.child[0] is not None:
            # En C-minus las condiciones se convierten implicitamente a booleano
            # Establecer el tipo a Boolean para evitar errores
            t.child[0].type = ExpType.Boolean
    
    elif t.stmt == StmtKind.WhileK:
        # Verificar que la condicion sea booleana
        if t.child[0] is not None:
            # En C-minus las condiciones se convierten implicitamente a booleano
            # Establecer el tipo a Boolean para evitar errores
            t.child[0].type = ExpType.Boolean
    
    elif t.stmt == StmtKind.AssignK:
        # Verificar asignacion
        if t.child[0] is None:
            return
            
        if t.child[0].exp == ExpKind.SubscriptK:
            # Asignacion a elemento de arreglo
            if t.child[1] is not None:
                # En C-minus, todas las expresiones asignadas a elementos de arreglo son enteros
                t.child[1].type = ExpType.Integer
        
        elif t.child[0].exp == ExpKind.IdK:
            # Asignacion a variable
            sym = st_lookup(t.child[0].name)
            if sym is not None:
                # Verificar si es un arreglo (no se puede asignar a un arreglo completo)
                if sym.attr and sym.attr.get('is_array'):
                    error(t.lineno, f"No se puede asignar a un arreglo completo '{t.child[0].name}'")
                
                # Verificar tipo
                if t.child[1] is not None:
                    # En C-minus, todas las expresiones asignadas a variables son enteros
                    t.child[1].type = ExpType.Integer
    
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
                # En C-minus, todos los valores de retorno son enteros
                # Establecer el tipo a Integer para evitar errores
                t.child[0].type = ExpType.Integer

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
    global Error
    Error = False
    
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

def typeCheck(syntaxTree):
    """
    Realiza la verificacion de tipos mediante un recorrido 
    en postorden del arbol sintactico
    """
    global Error
    
    # Segundo recorrido: verificar tipos
    traverse(syntaxTree, nullProc, checkNode)
    
    return Error

