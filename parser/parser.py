"""
Analizador sintáctico para el lenguaje C- basado en la técnica descendente recursivo
Implementación simplificada con todos los componentes en un solo archivo
"""
from enum import Enum

#
# DEFINICIONES DE TIPOS GLOBALES
#

# TokenType - Definición de todos los tokens del lenguaje C-
class TokenType(Enum):
    # Token especial para el fin de archivo
    ENDFILE = 300
    ERROR = 301
    
    # Palabras reservadas
    ELSE = 'else'
    IF = 'if'
    INT = 'int'
    RETURN = 'return'
    VOID = 'void'
    WHILE = 'while'
    
    # Tokens multicaracter
    ID = 310 # identificadores
    NUM = 311 # números
    
    # Símbolos especiales
    PLUS = '+' # suma
    MINUS = '-' # resta
    TIMES = '*' # multiplicación
    DIVIDE = '/' # división
    LT = '<' # menor que
    LTE = '<=' # menor o igual que
    GT = '>' # mayor que
    GTE = '>=' # mayor o igual que
    EQ = '==' # igual a
    NEQ = '!=' # no igual a
    ASSIGN = '=' # asignación
    SEMI = ';' # punto y coma
    COMMA = ',' # coma
    LPAREN = '(' # paréntesis izquierdo
    RPAREN = ')' # paréntesis derecho
    LBRACKET = '[' # corchete izquierdo
    RBRACKET = ']' # corchete derecho
    LBRACE = '{' # llave izquierda
    RBRACE = '}' # llave derecha

# Estados para el analizador léxico
class StateType(Enum):
    START = 0
    INCOMMENT = 1
    INNUM = 2
    INID = 3
    INASSIGN = 4
    INLT = 5
    INGT = 6
    INNOT = 7
    DONE = 8

# Tipo de nodo (sentencia, expresión o declaración)
class NodeKind(Enum):
    StmtK = 0
    ExpK = 1
    DeclK = 2

# Tipos de sentencias para C-
class StmtKind(Enum):
    IfK = 0
    WhileK = 1
    AssignK = 2
    ReturnK = 3
    CompoundK = 4

# Tipos de expresiones para C-
class ExpKind(Enum):
    OpK = 0
    ConstK = 1
    IdK = 2
    CallK = 3
    SubscriptK = 4  # Para indexación de arreglos

# Tipos de declaraciones para C-
class DeclKind(Enum):
    VarK = 0
    FunK = 1
    ParamK = 2

# Tipos de expresiones para comprobación de tipos
class ExpType(Enum):
    Void = 0
    Integer = 1
    Boolean = 2
    Array = 3

# Diccionario de palabras reservadas para búsqueda eficiente
RESERVED_WORDS = {
    'else': TokenType.ELSE,
    'if': TokenType.IF,
    'int': TokenType.INT,
    'return': TokenType.RETURN,
    'void': TokenType.VOID,
    'while': TokenType.WHILE
}

# Máximo número de hijos por nodo
MAXCHILDREN = 3

#
# ESTRUCTURA DEL ÁRBOL SINTÁCTICO
#

class TreeNode:
    """Clase para representar los nodos del árbol sintáctico"""
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
        self.val = None                    # Valor (para constantes)
        self.name = None                   # Nombre (para variables)
        self.type = None                   # Tipo de dato
        
        # Para nodos de tipo DeclK
        self.decl = None                   # Tipo de declaración
        self.is_array = False              # Indica si es un arreglo
        self.array_size = None             # Tamaño del arreglo
        self.params = []                   # Parámetros (para funciones)

#
# VARIABLES GLOBALES
#

# Variables globales para el lexer
programa = ""    # Contiene el string completo del programa
posicion = 0     # Posición actual en el programa
progLong = 0     # Longitud original del programa
lineno = 1       # Número de línea actual
linepos = 0      # Posición en la línea actual

# Variables para guardar estado
saved_token = None
saved_tokenString = None
saved_lineno = None

# Variables globales para el parser
token = None
tokenString = ""
Error = False
SyntaxTree = None

# Variable global para la indentación en la impresión del árbol
indentno = 0

#
# FUNCIONES DEL LEXER
#

def globales(prog, pos, long):
    """
    Función para recibir variables globales desde el programa principal
    
    Args:
        prog: String con el programa completo
        pos: Posición inicial
        long: Longitud del programa
    """
    global programa, posicion, progLong, lineno, linepos
    programa = prog
    posicion = pos
    progLong = long
    lineno = 1
    linepos = 0

def getChar():
    """
    Obtiene el siguiente caracter del programa
    
    Returns:
        Siguiente caracter del programa
    """
    global posicion, linepos
    if posicion < len(programa):
        c = programa[posicion]
        posicion += 1
        linepos += 1
        return c
    return '$'  # Fin de archivo

def ungetChar():
    """Retrocede un caracter"""
    global posicion, linepos
    if posicion > 0:
        posicion -= 1
        linepos -= 1

def peek():
    """
    Mira el siguiente caracter sin avanzar
    
    Returns:
        Siguiente caracter del programa
    """
    if posicion < len(programa):
        return programa[posicion]
    return '$'

def getLine():
    """
    Obtiene la línea actual completa
    
    Returns:
        String con la línea actual
    """
    global programa, posicion, linepos
    
    # Encontrar el inicio de la línea actual
    start = posicion - linepos
    
    # Encontrar el final de la línea
    end = start
    while end < len(programa) and programa[end] != '\n':
        end += 1
    
    return programa[start:end]

def printError(message, errorPos=None):
    """
    Imprime un mensaje de error con la línea y la posición
    
    Args:
        message: Mensaje de error
        errorPos: Posición del error en la línea
    """
    global lineno, linepos
    
    line = getLine()
    pos = errorPos if errorPos is not None else linepos - 1
    
    print(f"Línea {lineno}: {message}")
    print(line)
    print(" " * pos + "^")

def reservedLookup(tokenString):
    """
    Busca si un identificador es palabra reservada
    
    Args:
        tokenString: String a buscar
        
    Returns:
        TokenType correspondiente a la palabra reservada o TokenType.ID
    """
    # Usar el diccionario para búsqueda eficiente
    return RESERVED_WORDS.get(tokenString, TokenType.ID)

def getToken(imprime=True):
    """
    Obtiene el siguiente token del programa
    
    Args:
        imprime: Bandera para indicar si se imprime el token
        
    Returns:
        Tupla (token, tokenString, lineno)
    """
    global lineno, linepos, saved_token, saved_tokenString, saved_lineno
    
    # Verificar si hay un token guardado
    if saved_token is not None:
        token = saved_token
        tokenString = saved_tokenString
        line = saved_lineno
        
        # Limpiar el token guardado
        saved_token = None
        saved_tokenString = None
        saved_lineno = None
        
        # Imprimir el token si se requiere
        if imprime:
            print(f"{line:4d}: {token.name:10s} = {tokenString}")
        
        return token, tokenString, line
    
    # Inicializar variables
    tokenString = ""    # String para almacenar el token
    tokenType = None    # Tipo del token (valor de TokenType)
    state = StateType.START  # Estado actual - siempre comienza en START
    save = True         # Bandera para indicar si se guarda en tokenString
    
    # Loop principal del autómata
    while state != StateType.DONE:
        c = getChar()
        save = True
        
        if state == StateType.START:
            if c.isdigit():
                state = StateType.INNUM
            elif c.isalpha():
                state = StateType.INID
            elif c == '=':
                state = StateType.INASSIGN
            elif c == '<':
                state = StateType.INLT
            elif c == '>':
                state = StateType.INGT
            elif c == '!':
                state = StateType.INNOT
            elif c == '/':
                nextChar = peek()
                if nextChar == '*':
                    save = False
                    getChar()  # Consume el '*'
                    state = StateType.INCOMMENT
                else:
                    state = StateType.DONE
                    tokenType = TokenType.DIVIDE
            elif c in [' ', '\t', '\n', '\r']:
                save = False
                if c == '\n':
                    lineno += 1
                    linepos = 0
            else:
                state = StateType.DONE
                if c == '$':  # EOF
                    save = False
                    tokenType = TokenType.ENDFILE
                elif c == '+':
                    tokenType = TokenType.PLUS
                elif c == '-':
                    tokenType = TokenType.MINUS
                elif c == '*':
                    tokenType = TokenType.TIMES
                elif c == ';':
                    tokenType = TokenType.SEMI
                elif c == ',':
                    tokenType = TokenType.COMMA
                elif c == '(':
                    tokenType = TokenType.LPAREN
                elif c == ')':
                    tokenType = TokenType.RPAREN
                elif c == '[':
                    tokenType = TokenType.LBRACKET
                elif c == ']':
                    tokenType = TokenType.RBRACKET
                elif c == '{':
                    tokenType = TokenType.LBRACE
                elif c == '}':
                    tokenType = TokenType.RBRACE
                else:
                    tokenType = TokenType.ERROR
                    printError(f"Caracter ilegal: '{c}'")
        
        elif state == StateType.INCOMMENT:
            save = False
            if c == '*' and peek() == '/':
                getChar()  # Consume el '/'
                state = StateType.START
            elif c == '\n':
                lineno += 1
                linepos = 0
            elif c == '$':  # EOF en medio de un comentario
                state = StateType.DONE
                tokenType = TokenType.ERROR
                printError("Comentario sin cerrar")
        
        elif state == StateType.INNUM:
            if not c.isdigit():
                ungetChar()
                save = False
                state = StateType.DONE
                tokenType = TokenType.NUM
        
        elif state == StateType.INID:
            if not (c.isalpha() or c.isdigit()):
                ungetChar()
                save = False
                state = StateType.DONE
                tokenType = TokenType.ID
        
        elif state == StateType.INASSIGN:
            state = StateType.DONE
            if c == '=':
                tokenType = TokenType.EQ
            else:
                ungetChar()
                save = False
                tokenType = TokenType.ASSIGN
        
        elif state == StateType.INLT:
            state = StateType.DONE
            if c == '=':
                tokenType = TokenType.LTE
            else:
                ungetChar()
                save = False
                tokenType = TokenType.LT
        
        elif state == StateType.INGT:
            state = StateType.DONE
            if c == '=':
                tokenType = TokenType.GTE
            else:
                ungetChar()
                save = False
                tokenType = TokenType.GT
        
        elif state == StateType.INNOT:
            state = StateType.DONE
            if c == '=':
                tokenType = TokenType.NEQ
            else:
                ungetChar()
                save = False
                tokenType = TokenType.ERROR
                printError("Se esperaba '=' después de '!'")
        
        else:  # Nunca debería ocurrir
            state = StateType.DONE
            tokenType = TokenType.ERROR
            printError("Error en el analizador léxico")
        
        # Guardar el caracter en tokenString si es necesario
        if save and c != '$':
            tokenString += c
    
    # Si es un ID, verificar si es una palabra reservada
    if tokenType == TokenType.ID:
        tokenType = reservedLookup(tokenString)
    
    # Imprimir el token si se requiere
    if imprime:
        print(f"{lineno:4d}: {tokenType.name:10s} = {tokenString}")
    
    return tokenType, tokenString, lineno

#
# FUNCIONES PARA CREAR NODOS DEL AST
#

def newStmtNode(kind):
    """
    Crea un nuevo nodo de tipo sentencia (StmtK)
    
    Args:
        kind: Tipo de sentencia
        
    Returns:
        Nuevo nodo de tipo sentencia
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
    Crea un nuevo nodo de tipo expresión (ExpK)
    
    Args:
        kind: Tipo de expresión
        
    Returns:
        Nuevo nodo de tipo expresión
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
    Crea un nuevo nodo de tipo declaración (DeclK)
    
    Args:
        kind: Tipo de declaración
        
    Returns:
        Nuevo nodo de tipo declaración
    """
    global lineno
    t = TreeNode()
    if t is not None:
        t.nodekind = NodeKind.DeclK
        t.decl = kind
        t.lineno = lineno
    return t

#
# FUNCIONES PARA EL PARSER
#

def syntaxError(message):
    """
    Reporta un error de sintaxis
    
    Args:
        message: Mensaje de error
    """
    global Error, lineno
    print(f">>> Error de sintaxis en línea {lineno}: {message}")
    Error = True

def match(expected):
    """
    Verifica si el token actual coincide con el esperado
    y avanza al siguiente token
    
    Args:
        expected: Token esperado
    """
    global token, tokenString, lineno
    
    if token == expected:
        token, tokenString, lineno = getToken(False)
    else:
        syntaxError(f"Token inesperado -> se encontró {tokenString}")
        # Avanzar para evitar bucle infinito
        token, tokenString, lineno = getToken(False)

def parser(imprime = True):
    """
    Función principal del analizador sintáctico que genera el AST
    
    Args:
        imprime: Bandera para indicar si se debe imprimir el AST
        
    Returns:
        AST: Árbol sintáctico abstracto del programa
    """
    global token, tokenString, lineno, Error, SyntaxTree
    
    # Inicializar variables
    Error = False
    
    # Obtener el primer token
    token, tokenString, lineno = getToken(imprime)
    
    # Construir el árbol sintáctico
    SyntaxTree = parse_program()
    
    # Verificar si se llegó al final del archivo
    if token != TokenType.ENDFILE:
        syntaxError("Código termina antes que el archivo")
        
    # Imprimir el árbol sintáctico
    if imprime and SyntaxTree is not None:
        printTree(SyntaxTree)
        
    return SyntaxTree

def parse_program():
    """
    Parsea un programa según la gramática de C-:
    program → declaration-list
    
    Returns:
        Árbol sintáctico del programa
    """
    return parse_declaration_list()

def parse_declaration_list():
    """
    Parsea una lista de declaraciones según la gramática de C-:
    declaration-list → declaration-list declaration | declaration
    
    Returns:
        Árbol sintáctico de la lista de declaraciones
    """
    global token
    
    t = None
    p = None
    
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
        Árbol sintáctico de la declaración
    """
    global token, tokenString
    
    # Guardar el tipo especificador
    type_spec = token
    
    # Verificar que sea un tipo válido
    if token not in [TokenType.INT, TokenType.VOID]:
        syntaxError("Se esperaba un tipo de especificador (int o void)")
        return None
    
    match(token)
    
    # Guardar el nombre del identificador
    if token != TokenType.ID:
        syntaxError("Se esperaba un identificador")
        return None
    
    id_name = tokenString
    match(TokenType.ID)
    
    # Verificar si es una declaración de variable o función
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
        Árbol sintáctico de la declaración de variable
    """
    global token, tokenString
    
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
                t.array_size = int(tokenString)
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
        Árbol sintáctico de la declaración de función
    """
    global token
    
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
        Árbol sintáctico de la sentencia compuesta
    """
    global token
    
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
        Árbol sintáctico de las declaraciones locales
    """
    global token, tokenString
    
    t = None
    
    # Parsear declaraciones de variables locales
    while token == TokenType.INT or token == TokenType.VOID:
        p = None
        
        # Guardar el tipo especificador
        type_spec = token
        match(token)
        
        # Guardar el nombre del identificador
        if token != TokenType.ID:
            syntaxError("Se esperaba un identificador")
            token, tokenString, lineno = getToken(False)
            continue
        
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
        Árbol sintáctico de la lista de sentencias
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
        Árbol sintáctico de la sentencia
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
        Árbol sintáctico de la sentencia de expresión
    """
    global token
    
    t = None
    
    if token == TokenType.SEMI:
        # Sentencia vacía
        match(TokenType.SEMI)
    else:
        t = parse_expression()
        match(TokenType.SEMI)
    
    return t

def parse_selection_stmt():
    """
    Parsea una sentencia de selección según la gramática de C-:
    selection-stmt → if ( expression ) statement | if ( expression ) statement else statement
    
    Returns:
        Árbol sintáctico de la sentencia de selección
    """
    global token
    
    t = newStmtNode(StmtKind.IfK)
    
    match(TokenType.IF)
    match(TokenType.LPAREN)
    
    if t is not None:
        t.child[0] = parse_expression()
    
    match(TokenType.RPAREN)
    
    if t is not None:
        t.child[1] = parse_statement()
    
    if token == TokenType.ELSE:
        match(TokenType.ELSE)
        
        if t is not None:
            t.child[2] = parse_statement()
    
    return t

def parse_iteration_stmt():
    """
    Parsea una sentencia de iteración según la gramática de C-:
    iteration-stmt → while ( expression ) statement
    
    Returns:
        Árbol sintáctico de la sentencia de iteración
    """
    global token
    
    t = newStmtNode(StmtKind.WhileK)
    
    match(TokenType.WHILE)
    match(TokenType.LPAREN)
    
    if t is not None:
        t.child[0] = parse_expression()
    
    match(TokenType.RPAREN)
    
    if t is not None:
        t.child[1] = parse_statement()
    
    return t

def parse_return_stmt():
    """
    Parsea una sentencia de retorno según la gramática de C-:
    return-stmt → return ; | return expression ;
    
    Returns:
        Árbol sintáctico de la sentencia de retorno
    """
    global token
    
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
        Árbol sintáctico de la expresión
    """
    global token, tokenString
    
    # Guardar el token actual para verificar si es una asignación
    if token == TokenType.ID:
        # Almacenar el ID actual
        id_name = tokenString
        match(TokenType.ID)
        
        # Verificar si es una variable seguida de una asignación
        if token == TokenType.ASSIGN:
            # Es una asignación
            t = newStmtNode(StmtKind.AssignK)
            
            if t is not None:
                # Crear nodo para la variable
                var_node = newExpNode(ExpKind.IdK)
                var_node.name = id_name
                
                # Verificar si es un acceso a arreglo
                if token == TokenType.LBRACKET:
                    match(TokenType.LBRACKET)
                    var_node.exp = ExpKind.SubscriptK
                    var_node.child[0] = parse_expression()
                    match(TokenType.RBRACKET)
                
                # Asignar la variable como primer hijo de la asignación
                t.child[0] = var_node
                
                # Parsear la parte derecha de la asignación
                match(TokenType.ASSIGN)
                t.child[1] = parse_expression()
            
            return t
        else:
            # Es una variable en una expresión simple
            # Retroceder (lo que no podemos hacer directamente)
            # En su lugar, crear un nodo para la variable y continuar
            t = newExpNode(ExpKind.IdK)
            t.name = id_name
            
            # Verificar si es un acceso a arreglo
            if token == TokenType.LBRACKET:
                match(TokenType.LBRACKET)
                t.exp = ExpKind.SubscriptK
                t.child[0] = parse_expression()
                match(TokenType.RBRACKET)
            elif token == TokenType.LPAREN:
                # Es una llamada a función
                t = newExpNode(ExpKind.CallK)
                t.name = id_name
                
                match(TokenType.LPAREN)
                
                # Parsear argumentos
                t.child[0] = parse_args()
                
                match(TokenType.RPAREN)
            
            # Continuar con el resto de la expresión simple
            return parse_simple_expression_tail(t)
    
    # No es una asignación, es una expresión simple
    return parse_simple_expression()

def parse_var():
    """
    Parsea una variable según la gramática de C-:
    var → ID | ID [ expression ]
    
    Returns:
        Árbol sintáctico de la variable
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
    
    t = parse_additive_expression()
    
    return parse_simple_expression_tail(t)

def parse_simple_expression_tail(left):
    """
    Parsea la cola de una expresión simple
    
    Args:
        left: Parte izquierda de la expresión
        
    Returns:
        Árbol sintáctico de la expresión simple
    """
    global token
    
    # Verificar si hay un operador de comparación
    if token in [TokenType.LT, TokenType.LTE, TokenType.GT, TokenType.GTE, TokenType.EQ, TokenType.NEQ]:
        t = newExpNode(ExpKind.OpK)
        
        if t is not None:
            t.child[0] = left
            t.op = token
            
            match(token)
            
            t.child[1] = parse_additive_expression()
        
        return t
    
    return left

def parse_additive_expression():
    """
    Parsea una expresión aditiva según la gramática de C-:
    additive-expression → additive-expression addop term | term
    
    Returns:
        Árbol sintáctico de la expresión aditiva
    """
    global token
    
    t = parse_term()
    
    while token in [TokenType.PLUS, TokenType.MINUS]:
        p = newExpNode(ExpKind.OpK)
        
        if p is not None:
            p.child[0] = t
            p.op = token
            
            match(token)
            
            p.child[1] = parse_term()
            
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
    
    t = parse_factor()
    
    while token in [TokenType.TIMES, TokenType.DIVIDE]:
        p = newExpNode(ExpKind.OpK)
        
        if p is not None:
            p.child[0] = t
            p.op = token
            
            match(token)
            
            p.child[1] = parse_factor()
            
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
        t = newExpNode(ExpKind.ConstK)
        
        if t is not None:
            t.val = int(tokenString)
        
        match(TokenType.NUM)
    elif token == TokenType.ID:
        id_name = tokenString
        match(TokenType.ID)
        
        if token == TokenType.LPAREN:
            # Es una llamada a función
            t = newExpNode(ExpKind.CallK)
            t.name = id_name
            
            match(TokenType.LPAREN)
            t.child[0] = parse_args()
            match(TokenType.RPAREN)
        else:
            # Es una variable
            t = newExpNode(ExpKind.IdK)
            t.name = id_name
            
            # Verificar si es un acceso a arreglo
            if token == TokenType.LBRACKET:
                t.exp = ExpKind.SubscriptK
                
                match(TokenType.LBRACKET)
                t.child[0] = parse_expression()
                match(TokenType.RBRACKET)
    elif token == TokenType.LPAREN:
        match(TokenType.LPAREN)
        t = parse_expression()
        match(TokenType.RPAREN)
    else:
        syntaxError("Token inesperado")
        token, tokenString, lineno = getToken(False)
    
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

#
# FUNCIÓN PARA IMPRIMIR EL ÁRBOL SINTÁCTICO
#

def printSpaces():
    """Imprime espacios para la indentación del árbol"""
    global indentno
    print("  " * indentno, end="")

def printTree(tree):
    """
    Imprime el árbol sintáctico
    
    Args:
        tree: Árbol sintáctico a imprimir
    """
    global indentno
    
    indentno += 2
    
    while tree is not None:
        printSpaces()
        
        if tree.nodekind == NodeKind.StmtK:
            if tree.stmt == StmtKind.IfK:
                print(f"If")
            elif tree.stmt == StmtKind.WhileK:
                print(f"While")
            elif tree.stmt == StmtKind.AssignK:
                print(f"Assign to: {tree.child[0].name}")
            elif tree.stmt == StmtKind.ReturnK:
                print(f"Return")
            elif tree.stmt == StmtKind.CompoundK:
                print(f"Compound")
            else:
                print(f"Unknown ExpNode kind")
        elif tree.nodekind == NodeKind.ExpK:
            if tree.exp == ExpKind.OpK:
                print(f"Op: {tree.op}")
            elif tree.exp == ExpKind.ConstK:
                print(f"Const: {tree.val}")
            elif tree.exp == ExpKind.IdK:
                print(f"Id: {tree.name}")
            elif tree.exp == ExpKind.CallK:
                print(f"Call: {tree.name}")
            else:
                print(f"Unknown ExpNode kind")
        elif tree.nodekind == NodeKind.DeclK:
            if tree.decl == DeclKind.VarK:
                if tree.is_array:
                    print(f"Var Declaration: {tree.name}[{tree.array_size}]")
                else:
                    print(f"Var Declaration: {tree.name}")
            elif tree.decl == DeclKind.FunK:
                print(f"Function Declaration: {tree.name}")
                # Imprimir parámetros
                if tree.params:
                    printSpaces()
                    print("Parameters:")
                    for param in tree.params:
                        printSpaces()
                        print(f"  {param.name}{' []' if param.is_array else ''}")
            elif tree.decl == DeclKind.ParamK:
                if tree.is_array:
                    print(f"Parameter: {tree.name}[]")
                else:
                    print(f"Parameter: {tree.name}")
            else:
                print(f"Unknown DeclNode kind")
        else:
            print(f"Unknown node kind")
        
        # Imprimir cada hijo del nodo actual
        for i in range(MAXCHILDREN):
            if tree.child[i] is not None:
                printTree(tree.child[i])
        
        # Moverse al siguiente hermano para una recorrido en anchura
        tree = tree.sibling
    
    indentno -= 2  # Reducir la indentación

# Función principal para ejecutar el parser
if __name__ == "__main__":
    # Abrir y leer el archivo fuente
    filename = input("Ingrese el nombre del archivo a compilar (default: sample.c-): ") or "sample.c-"
    try:
        with open(filename, 'r') as f:
            programa_str = f.read()     # lee todo el archivo a compilar
            prog_long = len(programa_str)   # longitud original del programa
            programa_str = programa_str + '$'   # agregar un caracter $ que represente EOF
            pos = 0       # posición del caracter actual del string
            
            # Inicializar variables globales
            print(f"\nInicializando compilador con archivo: {filename}, longitud: {prog_long}")
            globales(programa_str, pos, prog_long)
            
            # Parsear el programa
            print("\nAnálisis sintáctico en proceso...")
            print("--------------------------------")
            
            AST = parser(True)  # True para imprimir el AST
            
            print("\nAnálisis sintáctico completado.")
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo '{filename}'")
    except Exception as e:
        print(f"Error inesperado: {e}")
        # Imprimir más detalles sobre el error
        import traceback
        traceback.print_exc()