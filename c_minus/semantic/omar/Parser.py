# ----------------------------------------------------------------------------
# 
# Programa basado en los documentos de clase proporcionados.
# Se utilizó también apoyo de herramientas de inteligencia artificial (como GPT) 
# para estructurar, corregir y perfeccionar algunas secciones del código.
#
# Autor: Omar Rivera Arenas
# Fecha: 28 de abril de 2025
#
# Descripción:
# Este archivo implementa el analizador sintáctico (parser) del lenguaje C-,
# usando un enfoque Top-Down Recursive Descent.
# Construye el Árbol Sintáctico Abstracto (AST) correspondiente al programa fuente.
# ----------------------------------------------------------------------------

from lexer import *
from lexer import lineno
from globalTypes import *

# Variables globales del parser
saved_token = None
saved_lexema = ""
saved_lineno = 1
saved_column = 1

# Funciones auxiliares

def syntaxError(msg):
    from lexer import lineno, programa, posicion, get_line_text
    print(f"\n>> Error sintáctico (línea {lineno}): {msg}")
    line_text = get_line_text(lineno)
    print(line_text)
    # Calcular la columna del token
    # Buscar la posición relativa en la línea
    line_start = programa.rfind('\n', 0, posicion) + 1
    col = posicion - line_start + 1
    print(' ' * (col - 1) + '^')

def match(expected):
    global saved_token, saved_lexema
    if saved_token == expected:
        getNextToken()
    else:
        syntaxError(f"Se esperaba {expected.name} y se recibió {saved_token.name}")
        getNextToken()

def getNextToken():
    global saved_token, saved_lexema, saved_lineno, saved_column
    saved_token, saved_lexema, saved_lineno, saved_column = getToken(imprime=False)

def newStmtNode(kind):
    t = TreeNode()
    t.nodekind = NodeKind.StmtK
    t.stmt = kind
    t.lineno = saved_lineno
    t.column = saved_column
    return t

def newExpNode(kind, name=None, val=None):
    t = TreeNode()
    t.nodekind = NodeKind.ExpK
    t.exp = kind
    t.lineno = saved_lineno
    t.column = saved_column
    if name is not None:
        t.name = name
    if val is not None:
        t.val = val
    return t

def parser(imprime=True):
    getNextToken()
    ast = declaration_list()
    
    # Check if we've consumed all tokens
    if saved_token != TokenType.ENDFILE:
        syntaxError(f"Unexpected token after program: {saved_token.name}")
    
    if imprime and ast:
        printTree(ast)
    return ast

def printTree(t, indent=0):
    while t is not None:
        print(" " * indent, end="")
        if t.nodekind == NodeKind.StmtK:
            if t.stmt is not None:
                print(f"Stmt: {t.stmt.name}")
            else:
                print("Stmt: Unknown")
        elif t.nodekind == NodeKind.ExpK:
            if t.exp == ExpKind.ConstK:
                print(f"Const: {t.val}")
            elif t.exp == ExpKind.IdK:
                print(f"Id: {t.name}")
            elif t.exp == ExpKind.CallK:
                print(f"Call: {t.name}")
            elif t.exp == ExpKind.OpK and t.op is not None:
                print(f"Op: {t.op.name}")
            else:
                print("ExpK (tipo desconocido)")
        else:
            print("Unknown node kind")
        
        for i, child in enumerate(t.child):
            if child is not None:
                print(" " * (indent + 2) + f"Child {i}:")
                printTree(child, indent + 4)
        if t.sibling is not None:
            print(" " * indent + "Sibling:")
        t = t.sibling


def declaration_list():
    t = declaration()
    p = t
    while saved_token in (TokenType.INT, TokenType.VOID):
        q = declaration()
        if p is not None:
            p.sibling = q
            p = q
    return t

def declaration():
    t = None
    if saved_token in (TokenType.INT, TokenType.VOID):
        typ_token = saved_token
        match(saved_token)
        # Unifica tipo a ExpType
        if typ_token == TokenType.INT:
            typ = ExpType.Integer
        else:
            typ = ExpType.Void
        if saved_token == TokenType.ID:
            id_name = saved_lexema
            match(TokenType.ID)
            if saved_token == TokenType.LPAREN:
                # Declaración de función
                func_node = newStmtNode(StmtKind.CompoundK)
                func_node.name = id_name
                func_node.is_function = True
                func_node.return_type = typ  # ExpType
                match(TokenType.LPAREN)
                param_nodes, param_info = param_list_ext()
                func_node.child[0] = param_nodes
                func_node.params = param_info
                match(TokenType.RPAREN)
                body = compound_stmt()
                body.is_func_body = True
                func_node.child[1] = body
                t = func_node
            else:
                # Declaración de variable
                t = newStmtNode(StmtKind.VarDeclK)
                t.name = id_name
                t.typ = typ
                t.var_type = typ
                t.is_array = False
                t.array_size = None
                t.size = None
                if saved_token == TokenType.LBRACKET:
                    t.is_array = True
                    match(TokenType.LBRACKET)
                    if saved_token == TokenType.NUM:
                        t.array_size = int(saved_lexema)
                        t.size = int(saved_lexema)
                        t.val = saved_lexema
                        match(TokenType.NUM)
                    match(TokenType.RBRACKET)
                match(TokenType.SEMI)
    return t

def param():
    if saved_token == TokenType.INT:
        match(TokenType.INT)
        typ = ExpType.Integer
        if saved_token == TokenType.ID:
            name = saved_lexema
            match(TokenType.ID)
            t = newExpNode(ExpKind.IdK)
            t.name = name
            t.lineno = saved_lineno
            t.typ = typ
            t.is_array = False
            t.array_size = None
            if saved_token == TokenType.LBRACKET:
                t.is_array = True
                match(TokenType.LBRACKET)
                match(TokenType.RBRACKET)
            return t

def param_list():
    # Retorna una lista de parámetros como nodos IdK conectados por sibling
    if saved_token == TokenType.VOID:
        match(TokenType.VOID)
        return None
    else:
        first = param()
        p = first
        while saved_token == TokenType.COMMA:
            match(TokenType.COMMA)
            q = param()
            p.sibling = q
            p = q
        return first

def param_list_ext():
    # Retorna (nodo de parámetros encadenados, lista de info de parámetros)
    if saved_token == TokenType.VOID:
        match(TokenType.VOID)
        return None, []
    else:
        first = param()
        param_info = []
        if first:
            param_info.append({'typ': first.typ, 'is_array': first.is_array, 'array_size': first.array_size})
        p = first
        while saved_token == TokenType.COMMA:
            match(TokenType.COMMA)
            q = param()
            if p:
                p.sibling = q
                p = q
            if q:
                param_info.append({'typ': q.typ, 'is_array': q.is_array, 'array_size': q.array_size})
        return first, param_info

def compound_stmt():
    t = newStmtNode(StmtKind.CompoundK)
    match(TokenType.LBRACE)
    t.child[0] = local_declarations()
    t.child[1] = statement_list()
    match(TokenType.RBRACE)
    return t

def local_declarations():
    t = None
    if saved_token in (TokenType.INT, TokenType.VOID):
        t = declaration()
        p = t
        while saved_token in (TokenType.INT, TokenType.VOID):
            q = declaration()
            if p is not None:
                p.sibling = q
                p = q
    return t

def statement_list():
    t = None
    if saved_token in (TokenType.IF, TokenType.WHILE, TokenType.RETURN,
                       TokenType.INPUT, TokenType.OUTPUT, TokenType.ID, TokenType.LBRACE):
        t = statement()
        p = t
        while saved_token in (TokenType.IF, TokenType.WHILE, TokenType.RETURN,
                              TokenType.INPUT, TokenType.OUTPUT, TokenType.ID, TokenType.LBRACE):
            q = statement()
            if p is not None:
                p.sibling = q
                p = q
    return t

def statement():
    t = None
    if saved_token == TokenType.IF:
        t = selection_stmt()
    elif saved_token == TokenType.WHILE:
        t = iteration_stmt()
    elif saved_token == TokenType.RETURN:
        t = return_stmt()
    elif saved_token == TokenType.INPUT:
        t = input_stmt()
    elif saved_token == TokenType.OUTPUT:
        t = output_stmt()
    elif saved_token == TokenType.LBRACE:
        t = compound_stmt()
    elif saved_token == TokenType.ID:
        id_name = saved_lexema
        match(TokenType.ID)
        if saved_token == TokenType.LBRACKET:
            t = array_assign_stmt(id_name)
        elif saved_token == TokenType.ASSIGN:
            t = assign_stmt(id_name)
        elif saved_token == TokenType.LPAREN:
            t = call_stmt(id_name)
        else:
            syntaxError("Sentencia no válida: identificador no seguido de '=', llamada o acceso a arreglo")
            getNextToken()
    else:
        t = expression_stmt()
    return t

def array_assign_stmt(id_name):
    t = newExpNode(ExpKind.OpK)
    t.op = TokenType.ASSIGN
    arr_node = newExpNode(ExpKind.IdK)
    arr_node.name = id_name
    arr_node.lineno = saved_lineno
    match(TokenType.LBRACKET)
    arr_node.child[0] = expression()
    match(TokenType.RBRACKET)
    t.child[0] = arr_node
    match(TokenType.ASSIGN)
    t.child[1] = expression()
    match(TokenType.SEMI)
    return t

def assign_stmt(id_name):
    t = newExpNode(ExpKind.OpK)
    t.op = TokenType.ASSIGN
    t.child[0] = newExpNode(ExpKind.IdK)
    t.child[0].name = id_name
    t.child[0].lineno = saved_lineno
    match(TokenType.ASSIGN)
    t.child[1] = expression()
    match(TokenType.SEMI)
    return t

def selection_stmt():
    t = newStmtNode(StmtKind.IfK)
    match(TokenType.IF)
    match(TokenType.LPAREN)
    t.child[0] = expression()
    match(TokenType.RPAREN)
    t.child[1] = statement()
    if saved_token == TokenType.ELSE:
        match(TokenType.ELSE)
        t.child[2] = statement()
    return t

def iteration_stmt():
    t = newStmtNode(StmtKind.WhileK)
    match(TokenType.WHILE)
    match(TokenType.LPAREN)
    t.child[0] = expression()
    match(TokenType.RPAREN)
    t.child[1] = statement()
    return t

def return_stmt():
    t = newStmtNode(StmtKind.ReturnK)
    match(TokenType.RETURN)
    if saved_token != TokenType.SEMI:
        t.child[0] = expression()
    match(TokenType.SEMI)
    return t

def input_stmt():
    t = newStmtNode(StmtKind.InputK)
    match(TokenType.INPUT)
    match(TokenType.LPAREN)
    t.child[0] = expression()
    match(TokenType.RPAREN)
    match(TokenType.SEMI)
    return t

def output_stmt():
    t = newStmtNode(StmtKind.OutputK)
    match(TokenType.OUTPUT)
    match(TokenType.LPAREN)
    t.child[0] = expression()
    match(TokenType.RPAREN)
    match(TokenType.SEMI)
    return t

def expression_stmt():
    t = None
    if saved_token == TokenType.SEMI:
        match(TokenType.SEMI)
    else:
        t = expression()
        match(TokenType.SEMI)
    return t

def expression():
    t = simple_exp()
    if saved_token in (TokenType.LT, TokenType.LTE, TokenType.GT, TokenType.GTE, TokenType.EQ, TokenType.NEQ):
        p = newExpNode(ExpKind.OpK)
        p.op = saved_token
        p.child[0] = t
        match(saved_token)
        p.child[1] = simple_exp()
        t = p
    return t

def simple_exp():
    t = term()
    while saved_token in (TokenType.PLUS, TokenType.MINUS):
        p = newExpNode(ExpKind.OpK)
        p.op = saved_token
        p.child[0] = t
        match(saved_token)
        p.child[1] = term()
        t = p
    return t

def term():
    t = factor()
    while saved_token in (TokenType.TIMES, TokenType.DIVIDE):
        p = newExpNode(ExpKind.OpK)
        p.op = saved_token
        p.child[0] = t
        match(saved_token)
        p.child[1] = factor()
        t = p
    return t

def factor():
    t = None
    if saved_token == TokenType.LPAREN:
        match(TokenType.LPAREN)
        t = expression()
        match(TokenType.RPAREN)
    elif saved_token == TokenType.NUM:
        t = newExpNode(ExpKind.ConstK)
        t.val = saved_lexema
        t.lineno = saved_lineno
        match(TokenType.NUM)
    elif saved_token == TokenType.ID:
        id_name = saved_lexema
        match(TokenType.ID)
        if saved_token == TokenType.LBRACKET:
            # ID [ exp ]  --> SubscriptK
            t = newExpNode(ExpKind.SubscriptK)
            t.name = id_name
            t.lineno = saved_lineno
            match(TokenType.LBRACKET)
            t.child[0] = expression()
            match(TokenType.RBRACKET)
        elif saved_token == TokenType.LPAREN:
            # ID ( args ) --> CallK
            t = newExpNode(ExpKind.CallK)
            t.name = id_name
            t.lineno = saved_lineno
            match(TokenType.LPAREN)
            t.child[0] = args()
            match(TokenType.RPAREN)
        else:
            # ID simple
            t = newExpNode(ExpKind.IdK)
            t.name = id_name
            t.lineno = saved_lineno
    else:
        syntaxError("Se esperaba una expresión válida")
        getNextToken()
    return t

def call_stmt(id_name):
    t = newExpNode(ExpKind.CallK)
    t.name = id_name
    t.lineno = saved_lineno
    match(TokenType.LPAREN)
    t.child[0] = args()
    match(TokenType.RPAREN)
    return t

def args():
    if saved_token == TokenType.RPAREN:
        return None  # Sin argumentos
    t = expression()
    p = t
    while saved_token == TokenType.COMMA:
        match(TokenType.COMMA)
        q = expression()
        p.sibling = q
        p = q
    return t
# Fin del código