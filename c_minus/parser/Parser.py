from globalTypes import *
from Lexer import getToken, getLine

# Variables globales
programa = "" # Contiene el programa completo como string
posicion = 0 # Posicion actual en el programa
progLong = 0 # Longitud original del programa

# Variables para el parser
token = None # Token actual
tokenString = "" # Valor del token actual
lineno = 1 # Numero de linea actual
Error = False # Indica si se ha encontrado algun error
recovering = False # Indica si estamos en modo de recuperacion de errores

# Variable para indentacion al imprimir el arbol
indentno = 0 # Cantidad de espacios de indentacion

# Constantes
MAXCHILDREN = 3 # Numero maximo de hijos por nodo del AST

def globales(prog, pos, long):
    """
    Recibe las variables globales del programa principal
    
    Args:
        prog: Programa completo
        pos: Posicion inicial
        long: Longitud del programa
    """
    global programa, posicion, progLong
    programa = prog
    posicion = pos
    progLong = long

def syntaxError(message):
    """
    Reporta un error de sintaxis con informacion de la ubicacion
    
    Args:
        message: Mensaje de error
    """
    global lineno, Error, tokenString, recovering
    
    # Si ya estamos en modo de recuperacion, no reportar mas errores
    if recovering:
        return
    
    Error = True
    line = getLine()
    
    # Calcular la posicion para el indicador de error (^)
    # Intenta encontrar la posicion del token en la linea
    pos = line.find(tokenString) if tokenString else 0
    if pos < 0: # Si no se encuentra, usar una posicion aproximada
        pos = 0
    
    print(f"\n>>> Error de sintaxis - Linea {lineno}: {message}")
    print(line)
    print(" " * pos + "^")
    
    if token is not None and token != TokenType.ERROR:
        print(f"   Se encontro: '{tokenString}' (token: {token.name})")

def match(expected):
    """
    Verifica si el token actual coincide con el esperado y avanza al siguiente
    
    Args:
        expected: Token esperado
    """
    global token, tokenString, lineno, recovering
    
    if token == expected:
        token, tokenString, lineno = getToken(False)
        recovering = False # Si el match es exitoso, ya no estamos en recuperacion
    else:
        if not recovering: # Solo reportar error si no estamos en modo recuperacion
            expected_name = expected.name if hasattr(expected, 'name') else str(expected)
            syntaxError(f"Se esperaba '{expected_name}', pero se encontro '{tokenString}'")
            # Intentar recuperarse del error
            recovering = True
            recover_from_error([expected])

# Funciones para crear nodos del AST

def newStmtNode(kind):
    """
    Crea un nuevo nodo de tipo sentencia
    
    Args:
        kind: Tipo de sentencia
        
    Returns:
        Nodo de sentencia
    """
    global lineno
    t = TreeNode()
    if t is not None:
        t.nodekind = NodeKind.StmtK
        t.stmt = kind
        t.lineno = lineno
    return t

def newExpNode(kind):
    """
    Crea un nuevo nodo de tipo expresion
    
    Args:
        kind: Tipo de expresion
        
    Returns:
        Nodo de expresion
    """
    global lineno
    t = TreeNode()
    if t is not None:
        t.nodekind = NodeKind.ExpK
        t.exp = kind
        t.lineno = lineno
        t.type = ExpType.Void
    return t

def newDeclNode(kind):
    """
    Crea un nuevo nodo de tipo declaracion
    
    Args:
        kind: Tipo de declaracion
        
    Returns:
        Nodo de declaracion
    """
    global lineno
    t = TreeNode()
    if t is not None:
        t.nodekind = NodeKind.DeclK
        t.decl = kind
        t.lineno = lineno
    return t

class TreeNode:
    """Nodo del Arbol Sintactico Abstracto (AST)"""
    
    def __init__(self):
        self.child = [None] * MAXCHILDREN # Hijos del nodo
        self.sibling = None # Hermano del nodo
        self.lineno = 0 # Linea donde aparece
        self.nodekind = None # Tipo de nodo (StmtK, ExpK, DeclK)
        
        # Para nodos de tipo StmtK
        self.stmt = None # Tipo de sentencia
        
        # Para nodos de tipo ExpK
        self.exp = None # Tipo de expresion
        self.op = None # Operador
        self.val = None # Valor
        self.name = None # Nombre
        self.type = None # Tipo
        
        # Para nodos de tipo DeclK
        self.decl = None # Tipo de declaracion
        self.is_array = False # Indica si es un arreglo
        self.array_size = None # Tamaño del arreglo
        self.params = [] # Parametros (para funciones)

def parser(imprime = True):
    """
    Funcion principal del parser que genera el AST
    
    Args:
        imprime: Indica si se debe imprimir el AST
        
    Returns:
        Arbol sintactico abstracto
    """
    global token, tokenString, lineno, Error, recovering
    
    # Inicializar variables
    Error = False
    recovering = False
    
    # Obtener el primer token
    token, tokenString, lineno = getToken(False)
    
    # Construir el arbol sintactico
    syntax_tree = program()
    
    # Verificar si se llego al final del archivo
    if token != TokenType.ENDFILE:
        syntaxError("Codigo termina antes que el archivo")
    
    # Imprimir el AST si se requiere
    if imprime and syntax_tree is not None:
        print("\n=== Arbol Sintactico Abstracto (AST) ===\n")
        printTree(syntax_tree)
    
    return syntax_tree

def program():
    """
    Parsea un programa segun la gramatica de C-:
    program → declaration-list
    
    Returns:
        Nodo raiz del AST
    """
    return declaration_list()

def declaration_list():
    """
    Parsea una lista de declaraciones segun la gramatica de C-:
    declaration-list → declaration-list declaration | declaration
    
    Returns:
        Lista de nodos de declaracion
    """
    t = None # Primer nodo
    p = None # Ultimo nodo procesado
    
    # Procesar declaraciones mientras sean posibles
    while token in [TokenType.INT, TokenType.VOID]:
        q = declaration()
        
        if q is not None:
            if t is None:
                t = p = q
            else:
                p.sibling = q
                p = q
    
    return t

def declaration():
    """
    Parsea una declaracion segun la gramatica de C-:
    declaration → var-declaration | fun-declaration
    
    Returns:
        Nodo de declaracion
    """
    global token, tokenString
    
    # Verificar que sea un tipo valido
    if token not in [TokenType.INT, TokenType.VOID]:
        syntaxError("Se esperaba un tipo (int o void)")
        return None
    
    # Guardar el tipo especificador
    type_spec = token
    match(token)
    
    # Verificar que haya un identificador
    if token != TokenType.ID:
        syntaxError("Se esperaba un identificador")
        return None
    
    # Guardar el nombre del identificador
    id_name = tokenString
    match(TokenType.ID)
    
    # Determinar si es declaracion de variable o funcion
    if token == TokenType.SEMI or token == TokenType.LBRACKET:
    # Es una declaracion de variable
        return var_declaration(type_spec, id_name)
    elif token == TokenType.LPAREN:
    # Es una declaracion de funcion
        return fun_declaration(type_spec, id_name)
    else:
        syntaxError("Declaracion invalida")
        return None

def var_declaration(type_spec, id_name):
    """
    Parsea una declaracion de variable segun la gramatica de C-:
    var-declaration → type-specifier ID ; | type-specifier ID [ NUM ] ;
    
    Args:
        type_spec: Tipo especificador
        id_name: Nombre del identificador
        
    Returns:
        Nodo de declaracion de variable
    """
    global token, tokenString
    
    # Crear nodo para la declaracion
    t = newDeclNode(DeclKind.VarK)
    
    if t is not None:
        t.name = id_name
        t.type = ExpType.Integer if type_spec == TokenType.INT else ExpType.Void
        
        # Verificar si es un arreglo
        if token == TokenType.LBRACKET:
            t.is_array = True
            match(TokenType.LBRACKET)
            
            # Verificar que el tamaño sea un numero
            if token == TokenType.NUM:
                try:
                    t.array_size = int(tokenString)
                except ValueError:
                    syntaxError("Tamaño de arreglo invalido")
                    t.array_size = 0
                match(TokenType.NUM)
            else:
                syntaxError("Se esperaba un numero para el tamaño del arreglo")
            
            match(TokenType.RBRACKET)
        
        # Toda declaracion de variable termina con punto y coma
        match(TokenType.SEMI)
    
    return t

def fun_declaration(type_spec, id_name):
    """
    Parsea una declaracion de funcion segun la gramatica de C-:
    fun-declaration → type-specifier ID ( params ) compound-stmt
    
    Args:
        type_spec: Tipo especificador
        id_name: Nombre del identificador
        
    Returns:
        Nodo de declaracion de funcion
    """
    global token
    
    # Crear nodo para la declaracion
    t = newDeclNode(DeclKind.FunK)
    
    if t is not None:
        t.name = id_name
        t.type = ExpType.Integer if type_spec == TokenType.INT else ExpType.Void
        
        match(TokenType.LPAREN)
        
        # Parsear parametros
        t.params = params()
        
        match(TokenType.RPAREN)
        
        # Parsear cuerpo de la funcion
        t.child[0] = compound_stmt()
    
    return t

def params():
    """
    Parsea parametros segun la gramatica de C-:
    params → param-list | void
    
    Returns:
        Lista de parametros
    """
    global token
    
    params_list = []
    
    # Verificar si los parametros son void (sin parametros)
    if token == TokenType.VOID:
        match(TokenType.VOID)
        
        # Verificar si hay mas parametros
        if token == TokenType.RPAREN:
            return params_list
        
        # Si no es cierre de parentesis, es un error de declaracion
        syntaxError("Parametro void debe ser el unico cuando se usa")
    
    # Parsear lista de parametros
    return param_list()

def param_list():
    """
    Parsea una lista de parametros segun la gramatica de C-:
    param-list → param-list , param | param
    
    Returns:
        Lista de parametros
    """
    global token
    
    params_list = []
    
    # Parsear el primer parametro
    param_node = param()
    if param_node is not None:
        params_list.append(param_node)
    
    # Parsear parametros adicionales
    while token == TokenType.COMMA:
        match(TokenType.COMMA)
        param_node = param()
        if param_node is not None:
            params_list.append(param_node)
    
    return params_list

def param():
    """
    Parsea un parametro segun la gramatica de C-:
    param → type-specifier ID | type-specifier ID [ ]
    
    Returns:
        Nodo del parametro
    """
    global token, tokenString
    
    # Crear nodo para el parametro
    t = newDeclNode(DeclKind.ParamK)
    
    if t is not None:
        # Obtener tipo del parametro
        if token == TokenType.INT:
            t.type = ExpType.Integer
        elif token == TokenType.VOID:
            t.type = ExpType.Void
        else:
            syntaxError("Se esperaba int o void")
            return None
        
        match(token)
        
        # Obtener nombre del parametro
        if token != TokenType.ID:
            syntaxError("Se esperaba un identificador")
            return None
        
        t.name = tokenString
        match(TokenType.ID)
        
        # Verificar si es un parametro de arreglo
        if token == TokenType.LBRACKET:
            t.is_array = True
            match(TokenType.LBRACKET)
            match(TokenType.RBRACKET)
    
    return t

def compound_stmt():
    """
    Parsea una sentencia compuesta segun la gramatica de C-:
    compound-stmt → { local-declarations statement-list }
    
    Returns:
        Nodo de sentencia compuesta
    """
    global token
    
    # Crear nodo para la sentencia compuesta
    t = newStmtNode(StmtKind.CompoundK)
    
    match(TokenType.LBRACE)
    
    if t is not None:
        # Parsear declaraciones locales
        t.child[0] = local_declarations()
        
        # Parsear lista de sentencias
        t.child[1] = statement_list()
    
    match(TokenType.RBRACE)
    
    return t

def local_declarations():
    """
    Parsea declaraciones locales segun la gramatica de C-:
    local-declarations → local-declarations var-declaration | empty
    
    Returns:
        Lista de nodos de declaracion local
    """
    global token, tokenString
    
    t = None
    
    # Parsear declaraciones de variables locales
    while token == TokenType.INT or token == TokenType.VOID:
        # Guardar el tipo especificador
        type_spec = token
        match(token)
        
        # Verificar que haya un identificador
        if token != TokenType.ID:
            syntaxError("Se esperaba un identificador")
            continue
        
        # Guardar el nombre del identificador
        id_name = tokenString
        match(TokenType.ID)
        
        # Crear nodo para la declaracion de variable
        p = var_declaration(type_spec, id_name)
        
        # Agregar a la lista de declaraciones
        if p is not None:
            if t is None:
                t = p
            else:
                # Agregar al final de la lista de hermanos
                temp = t
                while temp.sibling is not None:
                    temp = temp.sibling
                temp.sibling = p
    
    return t

def statement_list():
    """
    Parsea una lista de sentencias segun la gramatica de C-:
    statement-list → statement-list statement | empty
    
    Returns:
        Lista de nodos de sentencia
    """
    global token
    
    t = None
    
    # Parsear sentencias hasta encontrar un corchete de cierre
    while token != TokenType.RBRACE and token != TokenType.ENDFILE:
        p = statement()
        
        if p is not None:
            if t is None:
                t = p
            else:
                # Agregar al final de la lista de hermanos
                temp = t
                while temp.sibling is not None:
                    temp = temp.sibling
                temp.sibling = p
    
    return t

def statement():
    """
    Parsea una sentencia segun la gramatica de C-:
    statement → expression-stmt | compound-stmt | selection-stmt | iteration-stmt | return-stmt
    
    Returns:
        Nodo de sentencia
    """
    global token
    
    t = None
    
    if token == TokenType.IF:
        t = selection_stmt()
    elif token == TokenType.WHILE:
        t = iteration_stmt()
    elif token == TokenType.RETURN:
        t = return_stmt()
    elif token == TokenType.LBRACE:
        t = compound_stmt()
    else:
        t = expression_stmt()
    
    return t

def expression_stmt():
    """
    Parsea una sentencia de expresion segun la gramatica de C-:
    expression-stmt → expression ; | ;
    
    Returns:
        Nodo de sentencia de expresion
    """
    global token
    
    t = None
    
    if token == TokenType.SEMI:
        # Sentencia vacia
        match(TokenType.SEMI)
    else:
        # Sentencia con expresion
        t = expression()
        
        match(TokenType.SEMI)
    
    return t

def selection_stmt():
    """
    Parsea una sentencia de seleccion segun la gramatica de C-:
    selection-stmt → if ( expression ) statement | if ( expression ) statement else statement
    
    Returns:
        Nodo de sentencia if
    """
    global token
    
    # Crear nodo para la sentencia if
    t = newStmtNode(StmtKind.IfK)
    
    match(TokenType.IF)
    match(TokenType.LPAREN)
    
    if t is not None:
        # Parsear la condicion
        t.child[0] = expression()
    
    match(TokenType.RPAREN)
    
    if t is not None:
        # Parsear la sentencia 'then'
        t.child[1] = statement()
    
    if token == TokenType.ELSE:
        match(TokenType.ELSE)
        
        if t is not None:
            # Parsear la sentencia 'else'
            t.child[2] = statement()
    
    return t

def iteration_stmt():
    """
    Parsea una sentencia de iteracion segun la gramatica de C-:
    iteration-stmt → while ( expression ) statement
    
    Returns:
        Nodo de sentencia while
    """
    global token
    
    # Crear nodo para la sentencia while
    t = newStmtNode(StmtKind.WhileK)
    
    match(TokenType.WHILE)
    match(TokenType.LPAREN)
    
    if t is not None:
        # Parsear la condicion
        t.child[0] = expression()
    
    match(TokenType.RPAREN)
    
    if t is not None:
        # Parsear el cuerpo del ciclo
        t.child[1] = statement()
    
    return t

def expression_safe():
    """
    Version segura de expression que maneja mejor los errores
    en expresiones complejas.
    
    Returns:
        Nodo de expresion o None si hay error
    """
    global token, tokenString, recovering
    
    debug_token("Inicio expression_safe")
    
    try:
        # Intentar parsear normalmente
        result = expression()
        debug_token("Exito en expression_safe")
        return result
    except Exception as e:
        syntaxError(f"Error en expresion: {str(e)}")
        
        # Si hay un error, intentar recuperarse
        if not recovering:
            recovering = True
            # Intentar continuar despues de error
            expression_end_tokens = [TokenType.SEMI, TokenType.RPAREN, TokenType.RBRACKET, TokenType.COMMA]
            
            print("   Intentando recuperar expresion...")
            
            # Avanzar hasta el final de la expresion
            while token not in expression_end_tokens and token != TokenType.ENDFILE:
                token, tokenString, lineno = getToken(False)
            
            if token in expression_end_tokens:
                print(f"   Recuperacion exitosa hasta token: {token.name}")
                # Crear un nodo vacio para continuar
                t = newExpNode(ExpKind.IdK)
                t.name = "error_recovery"
                return t
        
        return None

def try_to_continue():
    """
    Intenta seguir la compilacion despues de un error grave
    
    Esta funcion intenta llevar el estado del parser a un punto
    donde pueda continuar el analisis sintactico despues de 
    encontrar un error grave en una expresion.
    """
    global token, tokenString, lineno, recovering
    
    print("   Intentando continuar despues de error grave...")
    
    # Primero buscamos un terminador de expresion
    expr_terminators = [TokenType.SEMI, TokenType.RPAREN, TokenType.RBRACKET, TokenType.COMMA]
    
    while token not in expr_terminators and token != TokenType.ENDFILE:
        token, tokenString, lineno = getToken(False)
    
    if token != TokenType.ENDFILE:
        print(f"   Continuacion exitosa en token: {token.name}")
        recovering = False
        return True
    else:
        print("   No se pudo continuar - fin del archivo")
        return False

def return_stmt():
    """
    Parsea una sentencia de retorno segun la gramatica de C-:
    return-stmt → return ; | return expression ;
    
    Returns:
        Nodo de sentencia return
    """
    global token, tokenString, recovering
    
    debug_token("Inicio return_stmt")
    
    # Crear nodo para la sentencia return
    t = newStmtNode(StmtKind.ReturnK)
    
    match(TokenType.RETURN)
    
    # Verificar si hay una expresion
    if token != TokenType.SEMI:
        if t is not None:
            debug_token("Antes de expression")
            # Guardar el estado de recuperacion actual
            was_recovering = recovering
            
            try:
                # Desactivar el modo de recuperacion para esta expresion especifica
                recovering = False
                
                # Usar expression directamente (debe funcionar para expresiones complejas)
                t.child[0] = expression()
                debug_token("Despues de expression")
            except Exception as e:
                syntaxError(f"Error al parsear expresion de retorno: {str(e)}")
                recovering = True
                
                # En caso de error, crear un nodo de identificador simple como respaldo
                error_node = newExpNode(ExpKind.IdK)
                error_node.name = "error_recovery"
                t.child[0] = error_node
                
                # Recuperarse directamente al punto y coma
                while token != TokenType.SEMI and token != TokenType.ENDFILE:
                    token, tokenString, lineno = getToken(False)
            finally:
                # Restaurar el estado de recuperacion anterior
                recovering = was_recovering
    
    # Despues de procesar la expresion, debe seguir un punto y coma
    match(TokenType.SEMI)
    debug_token("Fin return_stmt")
    
    return t


def expression():
    """
    Parsea una expresion segun la gramatica de C-:
    expression → var = expression | simple-expression
    
    Returns:
        Arbol sintactico de la expresion
    """
    global token, tokenString
    
    debug_token("Inicio expression")
    
    # Verificar si comienza con un identificador (potencial asignacion)
    if token == TokenType.ID:
        # Guardar informacion del identificador
        id_name = tokenString
        match(TokenType.ID)
        debug_token("Despues de match ID en expression")
        
        # Verificar si es un acceso a arreglo
        if token == TokenType.LBRACKET:
            debug_token("Detectado acceso a arreglo en expression")
            t = newExpNode(ExpKind.SubscriptK)
            if t is not None:
                t.name = id_name
                match(TokenType.LBRACKET)
                t.child[0] = expression()  # Indice del arreglo
                match(TokenType.RBRACKET)
                
                # Verificar si es una asignacion a un elemento del arreglo
                if token == TokenType.ASSIGN:
                    debug_token("Detectada asignacion a arreglo en expression")
                    p = newStmtNode(StmtKind.AssignK)
                    p.child[0] = t  # Variable (arreglo[index])
                    match(TokenType.ASSIGN)
                    p.child[1] = expression()  # Valor
                    return p
                else:
                    # Es un acceso a arreglo en una expresion
                    return simple_expression_rest(t)
        
        # Verificar si es una asignacion
        elif token == TokenType.ASSIGN:
            debug_token("Detectada asignacion en expression")
            t = newStmtNode(StmtKind.AssignK)
            if t is not None:
                # Crear nodo para la variable
                p = newExpNode(ExpKind.IdK)
                p.name = id_name
                t.child[0] = p # Variable
                match(TokenType.ASSIGN)
                t.child[1] = expression() # Valor
            return t
        else:
            # Es una expresion simple que comienza con ID
            debug_token("ID simple en expression")
            t = newExpNode(ExpKind.IdK)
            t.name = id_name
            
            # Verificar si es una llamada a funcion
            if token == TokenType.LPAREN:
                debug_token("Detectada llamada a funcion en expression")
                t.exp = ExpKind.CallK
                match(TokenType.LPAREN)
                t.child[0] = args()
                match(TokenType.RPAREN)
                debug_token("Despues de llamada a funcion en expression")
            
            # Continuar con posibles operaciones
            return simple_expression_rest(t)
    else:
        # Es una expresion simple
        debug_token("Expresion simple en expression")
        t = simple_expression()
        debug_token("Despues de expresion simple en expression")
        return t

def simple_expression():
    """
    Parsea una expresion simple segun la gramatica de C-:
    simple-expression → additive-expression relop additive-expression | additive-expression
    
    Returns:
        Arbol sintactico de la expresion simple
    """
    # Primero parseamos la primera parte de la expresion aditiva
    left = additive_expression()
    
    # Ahora continuamos con la parte opcional (operador relacional)
    return simple_expression_rest(left)

def simple_expression_rest(left):
    """
    Parsea la parte restante de una expresion simple
    (parte opcional con operador relacional o logico)
    
    Args:
        left: Nodo de la primera expresion aditiva
        
    Returns:
        Arbol sintactico de la expresion simple completa
    """
    global token
    
    debug_token("Inicio simple_expression_rest")
    
    # Verificamos si hay un operador relacional o logico
    if token in [TokenType.LT, TokenType.LTE, TokenType.GT, TokenType.GTE, TokenType.EQ, TokenType.NEQ, TokenType.AND, TokenType.OR]:
        # Creamos el nodo para el operador
        p = newExpNode(ExpKind.OpK)
        
        if p is not None:
            p.child[0] = left
            p.op = token
            
            # Consumimos el operador
            match(token)
            
            # Parseamos la segunda expresion
            p.child[1] = simple_expression()
            
            return p
    
    # Si no hay operador relacional o logico, continuamos con expresiones aditivas
    # o terminos (multiplicacion/division)
    if token in [TokenType.PLUS, TokenType.MINUS]:
        return additive_expression_with_left(left)
    elif token in [TokenType.TIMES, TokenType.DIVIDE]:
        return term_with_left(left)
    else:
        return left

def term_with_left(left):
    """
    Continua el parseo de un termino a partir de un factor inicial ya parseado
    
    Args:
        left: Nodo del factor inicial ya parseado
        
    Returns:
        Arbol sintactico del termino completo
    """
    global token
    
    debug_token("Inicio term_with_left")
    
    # Comenzamos con el factor ya parseado
    t = left
    
    # Ciclo para manejar operadores de multiplicacion/division
    while token in [TokenType.TIMES, TokenType.DIVIDE]:
        debug_token(f"Encontrado operador: {token.name}")
        
        # Creamos el nodo para el operador
        p = newExpNode(ExpKind.OpK)
        
        if p is not None:
            p.child[0] = t
            p.op = token
            
            # Guardar estado antes de match para depuracion
            match(token)
            debug_token("Despues de match operador, antes de factor")
            
            # Parseamos el siguiente factor
            try:
                p.child[1] = factor()
                debug_token("Despues de segundo factor")
                
                # Actualizamos el nodo principal
                t = p
            except Exception as e:
                syntaxError(f"Error al parsear factor despues de {token.name}: {str(e)}")
                # Intentar recuperarse del error
                recover_from_error([TokenType.SEMI, TokenType.RPAREN])
                break
    
    debug_token("Fin term_with_left")
    return t

def additive_expression_with_left(left):
    """
    Continua el parseo de una expresion aditiva a partir de un termino inicial ya parseado
    
    Args:
        left: Nodo del termino inicial ya parseado
        
    Returns:
        Arbol sintactico de la expresion aditiva completa
    """
    global token
    
    debug_token("Inicio additive_expression_with_left")
    
    # Comenzamos con el termino ya parseado
    t = left
    
    # Ciclo para manejar operadores de suma/resta
    while token in [TokenType.PLUS, TokenType.MINUS]:
        # Creamos el nodo para el operador
        p = newExpNode(ExpKind.OpK)
        
        if p is not None:
            p.child[0] = t
            p.op = token
            
            match(token)
            
            # Parseamos el siguiente termino
            p.child[1] = term()
            
            # Actualizamos el nodo principal
            t = p
    
    debug_token("Fin additive_expression_with_left")
    return t

def additive_expression():
    """
    Parsea una expresion aditiva segun la gramatica de C-:
    additive-expression → additive-expression addop term | term
    
    Returns:
        Arbol sintactico de la expresion aditiva
    """
    global token
    
    debug_token("Inicio additive_expression")
    
    # Parseamos el primer termino
    t = term()
    
    # Utilizamos la funcion auxiliar para continuar el parseo
    result = additive_expression_with_left(t)
    
    debug_token("Fin additive_expression")
    return result

def term():
    """
    Parsea un termino segun la gramatica de C-:
    term → term mulop factor | factor
    
    Returns:
        Arbol sintactico del termino
    """
    global token
    
    debug_return_token("Inicio term")
    
    # Parseamos el primer factor
    t = factor()
    debug_return_token("Despues de primer factor en term")
    
    # Ciclo para manejar operadores de multiplicacion/division
    while token in [TokenType.TIMES, TokenType.DIVIDE]:
        debug_return_token(f"Encontrado operador: {token.name}")
        
        # Creamos el nodo para el operador
        p = newExpNode(ExpKind.OpK)
        
        if p is not None:
            p.child[0] = t
            p.op = token
            
            # Guardar estado antes de match para depuracion
            match(token)
            debug_return_token("Despues de match operador, antes de factor")
            
            # Parseamos el siguiente factor
            try:
                p.child[1] = factor()
                debug_return_token("Despues de segundo factor")
                
                # Actualizamos el nodo principal
                t = p
            except Exception as e:
                syntaxError(f"Error al parsear factor despues de {token.name}: {str(e)}")
                # Intentar recuperarse del error
                recover_from_error([TokenType.SEMI, TokenType.RPAREN])
                break
    
    debug_return_token("Fin term")
    return t

def factor():
    """
    Parsea un factor segun la gramatica de C-:
    factor → ( expression ) | var | call | NUM
    
    Returns:
        Arbol sintactico del factor
    """
    global token, tokenString
    
    debug_return_token("Inicio factor")
    
    t = None
    
    if token == TokenType.NUM:
        # Caso de constante numerica
        t = newExpNode(ExpKind.ConstK)
        
        if t is not None:
            try:
                t.val = int(tokenString)
            except ValueError:
                t.val = 0
                syntaxError("Valor numerico invalido")
        
        match(TokenType.NUM)
        
    elif token == TokenType.LPAREN:
        # Caso de expresion entre parentesis
        match(TokenType.LPAREN)
        debug_return_token("Antes de expresion dentro de parentesis")
        t = expression()
        debug_return_token("Despues de expresion dentro de parentesis")
        match(TokenType.RPAREN)
        
    elif token == TokenType.ID:
        # Puede ser un identificador simple, un acceso a arreglo o una llamada a funcion
        id_name = tokenString
        
        match(TokenType.ID)
        debug_return_token("Despues de match ID")
        
        # Comprobar si es una llamada a funcion
        if token == TokenType.LPAREN:
            debug_return_token("Detectada llamada a funcion")
            t = newExpNode(ExpKind.CallK)
            
            if t is not None:
                t.name = id_name
                
                match(TokenType.LPAREN)
                t.child[0] = args()
                match(TokenType.RPAREN)
                debug_return_token("Despues de llamada a funcion")
            
        # Comprobar si es un acceso a arreglo
        elif token == TokenType.LBRACKET:
            t = newExpNode(ExpKind.SubscriptK)
            
            if t is not None:
                t.name = id_name
                
                match(TokenType.LBRACKET)
                t.child[0] = expression()
                match(TokenType.RBRACKET)
            
        else:
            # Es un identificador simple
            debug_return_token("ID simple")
            t = newExpNode(ExpKind.IdK)
            
            if t is not None:
                t.name = id_name
            
    else:
        syntaxError(f"Token inesperado en factor: {tokenString}")
        # Avanzar al siguiente token para recuperacion
        token, tokenString, lineno = getToken(False)
    
    debug_return_token("Fin factor")
    return t

def args():
    """
    Parsea argumentos segun la gramatica de C-:
    args → arg-list | empty
    
    Returns:
        Arbol sintactico de los argumentos
    """
    global token
    
    t = None
    
    if token != TokenType.RPAREN:
        t = arg_list()
    
    return t

def arg_list():
    """
    Parsea una lista de argumentos segun la gramatica de C-:
    arg-list → arg-list , expression | expression
    
    Returns:
        Arbol sintactico de la lista de argumentos
    """
    global token
    
    t = expression()
    
    p = t
    
    while token == TokenType.COMMA:
        match(TokenType.COMMA)
        
        q = expression()
        
        if q is not None:
            if t is None:
                t = p = q
            else:
                p.sibling = q
                p = q
    
    return t

def debug_token(message="Estado actual"):
    """
    Imprime informacion de depuracion sobre el token actual
    
    Args:
        message: Mensaje descriptivo para la depuracion
    """
    global token, tokenString, lineno
    
    print(f"\n--- DEBUG: {message} ---")
    print(f"Token: {token}")
    print(f"TokenString: '{tokenString}'")
    print(f"Linea: {lineno}")
    print("-------------------\n")

def debug_return_token(message="Estado actual"):
    """
    Imprime informacion de depuracion sobre el token actual
    especificamente para depurar sentencias de retorno
    
    Args:
        message: Mensaje descriptivo para la depuracion
    """
    global token, tokenString, lineno
    
    print(f"\n--- RETURN DEBUG: {message} ---")
    print(f"Token: {token}")
    print(f"TokenString: '{tokenString}'")
    print(f"Linea: {lineno}")
    print("-------------------\n")

def return_stmt():
    """
    Parsea una sentencia de retorno segun la gramatica de C-:
    return-stmt → return ; | return expression ;
    
    Returns:
        Nodo de sentencia return
    """
    global token, tokenString
    
    debug_token("Inicio return_stmt")
    
    # Crear nodo para la sentencia return
    t = newStmtNode(StmtKind.ReturnK)
    
    match(TokenType.RETURN)
    
    # Verificar si hay una expresion
    if token != TokenType.SEMI:
        debug_token("Antes de parsear expresion en return")
        t.child[0] = expression()
        debug_token("Despues de parsear expresion en return")
    
    match(TokenType.SEMI)
    
    debug_token("Fin return_stmt")
    return t


def recover_from_error(sync_tokens=None):
    """
    Intenta recuperarse de un error de sintaxis avanzando hasta un token de sincronizacion
    """
    global token, tokenString, lineno, recovering, posicion
    
    if sync_tokens is None:
        sync_tokens = [
            TokenType.SEMI, # Fin de sentencia
            TokenType.RBRACE, # Fin de bloque
            TokenType.ELSE, # Inicio de else
            TokenType.IF, # Inicio de if
            TokenType.WHILE, # Inicio de while
            TokenType.RETURN, # Inicio de return
            TokenType.INT, # Inicio de declaracion
            TokenType.VOID # Inicio de declaracion
        ]
    
    print("   Intentando recuperarse del error...")
    
    # Guardar informacion del token actual para evitar bucles
    current_token = token
    current_pos = posicion
    
    # Caso especial para expresiones aritmeticas
    if token in [TokenType.TIMES, TokenType.DIVIDE, TokenType.PLUS, TokenType.MINUS]:
        print("   Detectado operador aritmetico, avanzando hasta fin de expresion...")
        
        # Avanzar al siguiente token inmediatamente
        token, tokenString, lineno = getToken(False)
        
        # Buscar el fin de la expresion (punto y coma, parentesis, etc.)
        max_tokens = 15 # Limite razonable para evitar bucles infinitos
        count = 0
        
        while token not in [TokenType.SEMI, TokenType.RPAREN, TokenType.RBRACKET, 
                           TokenType.COMMA, TokenType.RBRACE] and token != TokenType.ENDFILE and count < max_tokens:
            token, tokenString, lineno = getToken(False)
            count += 1
        
        if token == TokenType.SEMI:
            print(f"   Recuperacion exitosa, encontrado punto y coma")
            recovering = False
            return
    
    # Procedimiento estandar de recuperacion
    token, tokenString, lineno = getToken(False) # Avanzar al menos un token
    
    # Si no avanzamos (raro pero posible), forzar avance
    if current_pos == posicion:
        token, tokenString, lineno = getToken(False)
    
    # Buscar token de sincronizacion
    max_tokens = 10
    count = 0
    
    while token not in sync_tokens and token != TokenType.ENDFILE and count < max_tokens:
        token, tokenString, lineno = getToken(False)
        count += 1
        
        # Si encontramos un punto y coma, terminar la busqueda
        if token == TokenType.SEMI:
            break
    
    if token != TokenType.ENDFILE:
        print(f"   Recuperacion exitosa en token: {token.name}")
        recovering = False
    else:
        print("   No se pudo recuperar - fin del archivo")

def printSpaces():
    """
    Imprime espacios para la indentacion del arbol
    """
    global indentno
    print("  " * indentno, end="")

def printTree(tree):
    """
    Imprime el arbol sintactico
    
    Args:
        tree: Arbol sintactico a imprimir
    """
    global indentno
    
    indentno += 1
    
    while tree is not None:
        printSpaces()
        
        if tree.nodekind == NodeKind.StmtK:
            if tree.stmt == StmtKind.IfK:
                print("If")
            elif tree.stmt == StmtKind.WhileK:
                print("While")
            elif tree.stmt == StmtKind.AssignK:
                print("Assign to:")
            elif tree.stmt == StmtKind.ReturnK:
                print("Return")
            elif tree.stmt == StmtKind.CompoundK:
                print("Compound")
            else:
                print("Unknown StmtNode kind")
        elif tree.nodekind == NodeKind.ExpK:
            if tree.exp == ExpKind.OpK:
                print(f"Op: {tree.op.name}")
            elif tree.exp == ExpKind.ConstK:
                print(f"Const: {tree.val}")
            elif tree.exp == ExpKind.IdK:
                print(f"Id: {tree.name}")
            elif tree.exp == ExpKind.CallK:
                print(f"Call: {tree.name}")
            elif tree.exp == ExpKind.SubscriptK:
                print(f"Subscript: {tree.name}")
            else:
                print("Unknown ExpNode kind")
        elif tree.nodekind == NodeKind.DeclK:
            if tree.decl == DeclKind.VarK:
                if tree.is_array:
                    print(f"Var Declaration: {tree.name}[{tree.array_size}]")
                else:
                    print(f"Var Declaration: {tree.name}")
            elif tree.decl == DeclKind.FunK:
                print(f"Function Declaration: {tree.name}")
            elif tree.decl == DeclKind.ParamK:
                if tree.is_array:
                    print(f"Parameter: {tree.name}[]")
                else:
                    print(f"Parameter: {tree.name}")
            else:
                print("Unknown DeclNode kind")
        else:
            print("Unknown node kind")
        
        # Imprimir cada hijo del nodo actual
        for i in range(MAXCHILDREN):
            if tree.child[i] is not None:
                printTree(tree.child[i])
        
        # Moverse al siguiente hermano
        tree = tree.sibling
    
    indentno -= 1