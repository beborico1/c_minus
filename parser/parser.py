from globalTypes import *
from Lexer import getToken, getLine, ungetToken

# Variables globales
programa = ""    # Contiene el programa completo como string
posicion = 0     # Posición actual en el programa
progLong = 0     # Longitud original del programa

# Variables para el parser
token = None         # Token actual
tokenString = ""     # Valor del token actual
lineno = 1           # Número de línea actual
Error = False        # Indica si se ha encontrado algún error

# Variable para indentación al imprimir el árbol
indentno = 0         # Cantidad de espacios de indentación

# Constantes
MAXCHILDREN = 3      # Número máximo de hijos por nodo del AST

def globales(prog, pos, long):
    """
    Recibe las variables globales del programa principal
    
    Args:
        prog: Programa completo
        pos: Posición inicial
        long: Longitud del programa
    """
    global programa, posicion, progLong
    programa = prog
    posicion = pos
    progLong = long

def syntaxError(message):
    """
    Reporta un error de sintaxis con información de la ubicación
    
    Args:
        message: Mensaje de error
    """
    global lineno, Error, tokenString
    
    Error = True
    line = getLine()
    
    # Calcular la posición para el indicador de error (^)
    # Intenta encontrar la posición del token en la línea
    pos = line.find(tokenString) if tokenString else 0
    if pos < 0:  # Si no se encuentra, usar una posición aproximada
        pos = 0
    
    print(f"\n>>> Error de sintaxis - Línea {lineno}: {message}")
    print(line)
    print(" " * pos + "^")
    
    if token is not None and token != TokenType.ERROR:
        print(f"   Se encontró: '{tokenString}' (token: {token.name})")

def match(expected):
    """
    Verifica si el token actual coincide con el esperado y avanza al siguiente
    
    Args:
        expected: Token esperado
    """
    global token, tokenString, lineno
    
    if token == expected:
        token, tokenString, lineno = getToken(False)
    else:
        syntaxError(f"Se esperaba '{expected}', pero se encontró '{tokenString}'")

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
    Crea un nuevo nodo de tipo expresión
    
    Args:
        kind: Tipo de expresión
        
    Returns:
        Nodo de expresión
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
    Crea un nuevo nodo de tipo declaración
    
    Args:
        kind: Tipo de declaración
        
    Returns:
        Nodo de declaración
    """
    global lineno
    t = TreeNode()
    if t is not None:
        t.nodekind = NodeKind.DeclK
        t.decl = kind
        t.lineno = lineno
    return t

class TreeNode:
    """Nodo del Árbol Sintáctico Abstracto (AST)"""
    
    def __init__(self):
        self.child = [None] * MAXCHILDREN  # Hijos del nodo
        self.sibling = None                # Hermano del nodo
        self.lineno = 0                    # Línea donde aparece
        self.nodekind = None               # Tipo de nodo (StmtK, ExpK, DeclK)
        
        # Para nodos de tipo StmtK
        self.stmt = None                   # Tipo de sentencia
        
        # Para nodos de tipo ExpK
        self.exp = None                    # Tipo de expresión
        self.op = None                     # Operador
        self.val = None                    # Valor
        self.name = None                   # Nombre
        self.type = None                   # Tipo
        
        # Para nodos de tipo DeclK
        self.decl = None                   # Tipo de declaración
        self.is_array = False              # Indica si es un arreglo
        self.array_size = None             # Tamaño del arreglo
        self.params = []                   # Parámetros (para funciones)

def parser(imprime = True):
    """
    Función principal del parser que genera el AST
    
    Args:
        imprime: Indica si se debe imprimir el AST
        
    Returns:
        Árbol sintáctico abstracto
    """
    global token, tokenString, lineno, Error
    
    # Inicializar variables
    Error = False
    
    # Obtener el primer token
    token, tokenString, lineno = getToken(False)
    
    # Construir el árbol sintáctico
    syntax_tree = parse_program()
    
    # Verificar si se llegó al final del archivo
    if token != TokenType.ENDFILE:
        syntaxError("Código termina antes que el archivo")
    
    # Imprimir el AST si se requiere
    if imprime and syntax_tree is not None:
        print("\n=== Árbol Sintáctico Abstracto (AST) ===\n")
        printTree(syntax_tree)
    
    return syntax_tree

def parse_program():
    """
    Parsea un programa según la gramática de C-:
    program → declaration-list
    
    Returns:
        Nodo raíz del AST
    """
    return parse_declaration_list()

def parse_declaration_list():
    """
    Parsea una lista de declaraciones según la gramática de C-:
    declaration-list → declaration-list declaration | declaration
    
    Returns:
        Lista de nodos de declaración
    """
    t = None  # Primer nodo
    p = None  # Último nodo procesado
    
    # Procesar declaraciones mientras sean posibles
    while token in [TokenType.INT, TokenType.VOID]:
        q = parse_declaration()
        
        if q is not None:
            if t is None:
                t = p = q
            else:
                p.sibling = q
                p = q
    
    return t

def parse_declaration():
    """
    Parsea una declaración según la gramática de C-:
    declaration → var-declaration | fun-declaration
    
    Returns:
        Nodo de declaración
    """
    global token, tokenString
    
    # Verificar que sea un tipo válido
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
    
    # Determinar si es declaración de variable o función
    if token == TokenType.SEMI or token == TokenType.LBRACKET:
        # Es una declaración de variable
        return parse_var_declaration(type_spec, id_name)
    elif token == TokenType.LPAREN:
        # Es una declaración de función
        return parse_fun_declaration(type_spec, id_name)
    else:
        syntaxError("Declaración inválida")
        return None

def parse_var_declaration(type_spec, id_name):
    """
    Parsea una declaración de variable según la gramática de C-:
    var-declaration → type-specifier ID ; | type-specifier ID [ NUM ] ;
    
    Args:
        type_spec: Tipo especificador
        id_name: Nombre del identificador
        
    Returns:
        Nodo de declaración de variable
    """
    global token, tokenString
    
    # Crear nodo para la declaración
    t = newDeclNode(DeclKind.VarK)
    
    if t is not None:
        t.name = id_name
        t.type = ExpType.Integer if type_spec == TokenType.INT else ExpType.Void
        
        # Verificar si es un arreglo
        if token == TokenType.LBRACKET:
            t.is_array = True
            match(TokenType.LBRACKET)
            
            # Verificar que el tamaño sea un número
            if token == TokenType.NUM:
                try:
                    t.array_size = int(tokenString)
                except ValueError:
                    syntaxError("Tamaño de arreglo inválido")
                    t.array_size = 0
                match(TokenType.NUM)
            else:
                syntaxError("Se esperaba un número para el tamaño del arreglo")
            
            match(TokenType.RBRACKET)
        
        # Toda declaración de variable termina con punto y coma
        match(TokenType.SEMI)
    
    return t

def parse_fun_declaration(type_spec, id_name):
    """
    Parsea una declaración de función según la gramática de C-:
    fun-declaration → type-specifier ID ( params ) compound-stmt
    
    Args:
        type_spec: Tipo especificador
        id_name: Nombre del identificador
        
    Returns:
        Nodo de declaración de función
    """
    global token
    
    # Crear nodo para la declaración
    t = newDeclNode(DeclKind.FunK)
    
    if t is not None:
        t.name = id_name
        t.type = ExpType.Integer if type_spec == TokenType.INT else ExpType.Void
        
        match(TokenType.LPAREN)
        
        # Parsear parámetros
        t.params = parse_params()
        
        match(TokenType.RPAREN)
        
        # Parsear cuerpo de la función
        t.child[0] = parse_compound_stmt()
    
    return t

def parse_params():
    """
    Parsea parámetros según la gramática de C-:
    params → param-list | void
    
    Returns:
        Lista de parámetros
    """
    global token
    
    params_list = []
    
    # Verificar si los parámetros son void (sin parámetros)
    if token == TokenType.VOID:
        match(TokenType.VOID)
        
        # Verificar si hay más parámetros
        if token == TokenType.RPAREN:
            return params_list
        
        # Si no es cierre de paréntesis, es un error de declaración
        syntaxError("Parámetro void debe ser el único cuando se usa")
    
    # Parsear lista de parámetros
    return parse_param_list()

def parse_param_list():
    """
    Parsea una lista de parámetros según la gramática de C-:
    param-list → param-list , param | param
    
    Returns:
        Lista de parámetros
    """
    global token
    
    params_list = []
    
    # Parsear el primer parámetro
    param_node = parse_param()
    if param_node is not None:
        params_list.append(param_node)
    
    # Parsear parámetros adicionales
    while token == TokenType.COMMA:
        match(TokenType.COMMA)
        param_node = parse_param()
        if param_node is not None:
            params_list.append(param_node)
    
    return params_list

def parse_param():
    """
    Parsea un parámetro según la gramática de C-:
    param → type-specifier ID | type-specifier ID [ ]
    
    Returns:
        Nodo del parámetro
    """
    global token, tokenString
    
    # Crear nodo para el parámetro
    t = newDeclNode(DeclKind.ParamK)
    
    if t is not None:
        # Obtener tipo del parámetro
        if token == TokenType.INT:
            t.type = ExpType.Integer
        elif token == TokenType.VOID:
            t.type = ExpType.Void
        else:
            syntaxError("Se esperaba int o void")
            return None
        
        match(token)
        
        # Obtener nombre del parámetro
        if token != TokenType.ID:
            syntaxError("Se esperaba un identificador")
            return None
        
        t.name = tokenString
        match(TokenType.ID)
        
        # Verificar si es un parámetro de arreglo
        if token == TokenType.LBRACKET:
            t.is_array = True
            match(TokenType.LBRACKET)
            match(TokenType.RBRACKET)
    
    return t

def parse_compound_stmt():
    """
    Parsea una sentencia compuesta según la gramática de C-:
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
        t.child[0] = parse_local_declarations()
        
        # Parsear lista de sentencias
        t.child[1] = parse_statement_list()
    
    match(TokenType.RBRACE)
    
    return t

def parse_local_declarations():
    """
    Parsea declaraciones locales según la gramática de C-:
    local-declarations → local-declarations var-declaration | empty
    
    Returns:
        Lista de nodos de declaración local
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
        
        # Crear nodo para la declaración de variable
        p = parse_var_declaration(type_spec, id_name)
        
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

def parse_statement_list():
    """
    Parsea una lista de sentencias según la gramática de C-:
    statement-list → statement-list statement | empty
    
    Returns:
        Lista de nodos de sentencia
    """
    global token
    
    t = None
    
    # Parsear sentencias hasta encontrar un corchete de cierre
    while token != TokenType.RBRACE and token != TokenType.ENDFILE:
        p = parse_statement()
        
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

def parse_statement():
    """
    Parsea una sentencia según la gramática de C-:
    statement → expression-stmt | compound-stmt | selection-stmt | iteration-stmt | return-stmt
    
    Returns:
        Nodo de sentencia
    """
    global token
    
    t = None
    
    if token == TokenType.IF:
        t = parse_selection_stmt()
    elif token == TokenType.WHILE:
        t = parse_iteration_stmt()
    elif token == TokenType.RETURN:
        t = parse_return_stmt()
    elif token == TokenType.LBRACE:
        t = parse_compound_stmt()
    else:
        t = parse_expression_stmt()
    
    return t

def parse_expression_stmt():
    """
    Parsea una sentencia de expresión según la gramática de C-:
    expression-stmt → expression ; | ;
    
    Returns:
        Nodo de sentencia de expresión
    """
    global token
    
    t = None
    
    if token == TokenType.SEMI:
        # Sentencia vacía
        match(TokenType.SEMI)
    else:
        # Sentencia con expresión
        t = parse_expression()
        
        if token == TokenType.SEMI:
            match(TokenType.SEMI)
        else:
            syntaxError("Se esperaba ';'")
    
    return t

def parse_selection_stmt():
    """
    Parsea una sentencia de selección según la gramática de C-:
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
        # Parsear la condición
        t.child[0] = parse_expression()
    
    match(TokenType.RPAREN)
    
    if t is not None:
        # Parsear la sentencia 'then'
        t.child[1] = parse_statement()
    
    if token == TokenType.ELSE:
        match(TokenType.ELSE)
        
        if t is not None:
            # Parsear la sentencia 'else'
            t.child[2] = parse_statement()
    
    return t

def parse_iteration_stmt():
    """
    Parsea una sentencia de iteración según la gramática de C-:
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
        # Parsear la condición
        t.child[0] = parse_expression()
    
    match(TokenType.RPAREN)
    
    if t is not None:
        # Parsear el cuerpo del ciclo
        t.child[1] = parse_statement()
    
    return t

def parse_return_stmt():
    """
    Parsea una sentencia de retorno según la gramática de C-:
    return-stmt → return ; | return expression ;
    
    Returns:
        Nodo de sentencia return
    """
    global token
    
    # Crear nodo para la sentencia return
    t = newStmtNode(StmtKind.ReturnK)
    
    match(TokenType.RETURN)
    
    # Verificar si hay una expresión
    if token != TokenType.SEMI:
        if t is not None:
            t.child[0] = parse_expression()
    
    match(TokenType.SEMI)
    
    return t

def parse_expression():
    """
    Parsea una expresión según la gramática de C-:
    expression → var = expression | simple-expression
    
    Returns:
        Nodo de expresión
    """
    global token, tokenString
    
    # Verificar si comienza con un identificador (potencial asignación)
    if token == TokenType.ID:
        # Guardar información del identificador
        id_name = tokenString
        
        match(TokenType.ID)
        
        # Comprobar si es un acceso a arreglo
        if token == TokenType.LBRACKET:
            # Es un acceso a arreglo
            t = newExpNode(ExpKind.SubscriptK)
            
            if t is not None:
                t.name = id_name
                
                match(TokenType.LBRACKET)
                t.child[0] = parse_expression()
                match(TokenType.RBRACKET)
                
                # Verificar si es una asignación
                if token == TokenType.ASSIGN:
                    p = newStmtNode(StmtKind.AssignK)
                    
                    if p is not None:
                        p.child[0] = t  # Variable
                        
                        match(TokenType.ASSIGN)
                        p.child[1] = parse_expression()  # Valor
                    
                    return p
                else:
                    # Es un acceso a arreglo como parte de una expresión
                    return t
            
        # Comprobar si es una asignación simple
        elif token == TokenType.ASSIGN:
            t = newStmtNode(StmtKind.AssignK)
            
            if t is not None:
                # Crear nodo para la variable
                p = newExpNode(ExpKind.IdK)
                p.name = id_name
                
                t.child[0] = p  # Variable
                
                match(TokenType.ASSIGN)
                t.child[1] = parse_expression()  # Valor
            
            return t
            
        # Comprobar si es una llamada a función
        elif token == TokenType.LPAREN:
            t = newExpNode(ExpKind.CallK)
            
            if t is not None:
                t.name = id_name
                
                match(TokenType.LPAREN)
                t.child[0] = parse_args()
                match(TokenType.RPAREN)
            
            return t
            
        else:
            # Es un identificador simple como parte de una expresión
            t = newExpNode(ExpKind.IdK)
            
            if t is not None:
                t.name = id_name
            
            # Devolver el identificador y continuar con la expresión simple
            ungetToken()
            return parse_simple_expression()
    
    # Si no es una asignación, es una expresión simple
    return parse_simple_expression()

def parse_var():
    """
    Parsea una variable según la gramática de C-:
    var → ID | ID [ expression ]
    
    Returns:
        Nodo de variable
    """
    global token, tokenString
    
    # Verificar que el token actual sea un identificador
    if token != TokenType.ID:
        syntaxError("Se esperaba un identificador")
        return None
    
    # Crear nodo para la variable
    t = newExpNode(ExpKind.IdK)
    t.name = tokenString
    
    match(TokenType.ID)
    
    # Verificar si es un acceso a arreglo
    if token == TokenType.LBRACKET:
        t.exp = ExpKind.SubscriptK
        
        match(TokenType.LBRACKET)
        t.child[0] = parse_expression()
        match(TokenType.RBRACKET)
    
    return t

def parse_simple_expression():
    """
    Parsea una expresión simple según la gramática de C-:
    simple-expression → additive-expression relop additive-expression | additive-expression
    
    Returns:
        Árbol sintáctico de la expresión simple
    """
    global token
    
    # Parseamos la primera expresión aditiva
    t = parse_additive_expression()
    
    # Verificamos si hay un operador relacional
    if token in [TokenType.LT, TokenType.LTE, TokenType.GT, TokenType.GTE, TokenType.EQ, TokenType.NEQ]:
        # Creamos el nodo para el operador
        p = newExpNode(ExpKind.OpK)
        
        if p is not None:
            p.child[0] = t
            p.op = token
            
            match(token)
            
            # Parseamos la segunda expresión aditiva
            p.child[1] = parse_additive_expression()
            
            return p
    
    return t

def parse_additive_expression():
    """
    Parsea una expresión aditiva según la gramática de C-:
    additive-expression → additive-expression addop term | term
    
    Returns:
        Árbol sintáctico de la expresión aditiva
    """
    global token
    
    # Parseamos el primer término
    t = parse_term()
    
    # Ciclo para manejar operadores de suma/resta
    while token in [TokenType.PLUS, TokenType.MINUS]:
        # Creamos el nodo para el operador
        p = newExpNode(ExpKind.OpK)
        
        if p is not None:
            p.child[0] = t
            p.op = token
            
            match(token)
            
            # Parseamos el siguiente término
            p.child[1] = parse_term()
            
            # Actualizamos el nodo principal
            t = p
    
    return t

def parse_term():
    """
    Parsea un término según la gramática de C-:
    term → term mulop factor | factor
    
    Returns:
        Árbol sintáctico del término
    """
    global token
    
    # Parseamos el primer factor
    t = parse_factor()
    
    # Ciclo para manejar operadores de multiplicación/división
    while token in [TokenType.TIMES, TokenType.DIVIDE]:
        # Creamos el nodo para el operador
        p = newExpNode(ExpKind.OpK)
        
        if p is not None:
            p.child[0] = t
            p.op = token
            
            match(token)
            
            # Parseamos el siguiente factor
            p.child[1] = parse_factor()
            
            # Actualizamos el nodo principal
            t = p
    
    return t

def parse_factor():
    """
    Parsea un factor según la gramática de C-:
    factor → ( expression ) | var | call | NUM
    
    Returns:
        Árbol sintáctico del factor
    """
    global token, tokenString
    
    t = None
    
    if token == TokenType.NUM:
        # Caso de constante numérica
        t = newExpNode(ExpKind.ConstK)
        
        if t is not None:
            t.val = int(tokenString)
        
        match(TokenType.NUM)
        
    elif token == TokenType.LPAREN:
        # Caso de expresión entre paréntesis
        match(TokenType.LPAREN)
        t = parse_expression()
        match(TokenType.RPAREN)
        
    elif token == TokenType.ID:
        # Puede ser un identificador simple, un acceso a arreglo o una llamada a función
        id_name = tokenString
        
        match(TokenType.ID)
        
        # Comprobar si es una llamada a función
        if token == TokenType.LPAREN:
            t = newExpNode(ExpKind.CallK)
            
            if t is not None:
                t.name = id_name
                
                match(TokenType.LPAREN)
                t.child[0] = parse_args()
                match(TokenType.RPAREN)
            
        # Comprobar si es un acceso a arreglo
        elif token == TokenType.LBRACKET:
            t = newExpNode(ExpKind.SubscriptK)
            
            if t is not None:
                t.name = id_name
                
                match(TokenType.LBRACKET)
                t.child[0] = parse_expression()
                match(TokenType.RBRACKET)
            
        else:
            # Es un identificador simple
            t = newExpNode(ExpKind.IdK)
            
            if t is not None:
                t.name = id_name
            
    else:
        syntaxError(f"Token inesperado: {tokenString}")
    
    return t

def parse_call():
    """
    Parsea una llamada a función según la gramática de C-:
    call → ID ( args )
    
    Returns:
        Nodo de llamada a función
    """
    global token, tokenString
    
    # Verificar que el token actual sea un identificador
    if token != TokenType.ID:
        syntaxError("Se esperaba un identificador de función")
        return None
    
    # Crear nodo para la llamada
    t = newExpNode(ExpKind.CallK)
    
    if t is not None:
        t.name = tokenString
        
        match(TokenType.ID)
        match(TokenType.LPAREN)
        
        # Parsear argumentos
        t.child[0] = parse_args()
        
        match(TokenType.RPAREN)
    
    return t

def parse_args():
    """
    Parsea argumentos según la gramática de C-:
    args → arg-list | empty
    
    Returns:
        Árbol sintáctico de los argumentos
    """
    global token
    
    t = None
    
    if token != TokenType.RPAREN:
        t = parse_arg_list()
    
    return t

def parse_arg_list():
    """
    Parsea una lista de argumentos según la gramática de C-:
    arg-list → arg-list , expression | expression
    
    Returns:
        Árbol sintáctico de la lista de argumentos
    """
    global token
    
    t = parse_expression()
    
    p = t
    
    while token == TokenType.COMMA:
        match(TokenType.COMMA)
        
        q = parse_expression()
        
        if q is not None:
            if t is None:
                t = p = q
            else:
                p.sibling = q
                p = q
    
    return t

def printSpaces():
    """
    Imprime espacios para la indentación del árbol
    """
    global indentno
    print("  " * indentno, end="")

def printTree(tree):
    """
    Imprime el árbol sintáctico
    
    Args:
        tree: Árbol sintáctico a imprimir
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
                print("Unknown ExpNode kind")
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

def recover_from_error(sync_tokens=None):
    """
    Intenta recuperarse de un error de sintaxis avanzando hasta un token de sincronización
    
    Args:
        sync_tokens: Lista opcional de tokens de sincronización
    """
    global token, tokenString, lineno
    
    # Tokens de sincronización predeterminados si no se proporcionan
    if sync_tokens is None:
        sync_tokens = [
            TokenType.SEMI,      # Fin de sentencia
            TokenType.RBRACE,    # Fin de bloque
            TokenType.ELSE,      # Inicio de else
            TokenType.IF,        # Inicio de if
            TokenType.WHILE,     # Inicio de while
            TokenType.RETURN,    # Inicio de return
            TokenType.INT,       # Inicio de declaración
            TokenType.VOID       # Inicio de declaración
        ]
    
    print("   Intentando recuperarse del error...")
    
    # Avanzar hasta encontrar un token de sincronización
    while token not in sync_tokens and token != TokenType.ENDFILE:
        token, tokenString, lineno = getToken(False)
    
    if token != TokenType.ENDFILE:
        print(f"   Recuperación exitosa en token: {token.name}")
    else:
        print("   No se pudo recuperar - fin del archivo")

def match(expected):
    """
    Verifica si el token actual coincide con el esperado y avanza al siguiente
    
    Args:
        expected: Token esperado
    """
    global token, tokenString, lineno
    
    if token == expected:
        token, tokenString, lineno = getToken(False)
    else:
        expected_name = expected.name if hasattr(expected, 'name') else str(expected)
        syntaxError(f"Se esperaba '{expected_name}', pero se encontró '{tokenString}'")
        # Intentar recuperarse del error
        recover_from_error()