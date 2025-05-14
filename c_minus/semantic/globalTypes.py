from enum import Enum

# TokenType para C-
class TokenType(Enum):
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
    ID = 310
    NUM = 311
    
    # Simbolos especiales
    PLUS = '+'
    MINUS = '-'
    TIMES = '*'
    DIVIDE = '/'
    LT = '<'
    LTE = '<='
    GT = '>'
    GTE = '>='
    EQ = '=='
    NEQ = '!='
    ASSIGN = '='
    SEMI = ';'
    COMMA = ','
    LPAREN = '('
    RPAREN = ')'
    LBRACKET = '['
    RBRACKET = ']'
    LBRACE = '{'
    RBRACE = '}'
    AND = '&&'
    OR = '||'

# Estados para el analizador lexico
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

# Tipo de nodo (sentencia, expresion o declaracion)
class NodeKind(Enum):
    StmtK = 0
    ExpK = 1
    DeclK = 2

# Tipos de sentencias para C-minus
class StmtKind(Enum):
    IfK = 0
    WhileK = 1
    AssignK = 2
    ReturnK = 3
    CompoundK = 4

# Tipos de expresiones para C-minus
class ExpKind(Enum):
    OpK = 0
    ConstK = 1
    IdK = 2
    CallK = 3
    SubscriptK = 4 # Para indexacion de arreglos

# Tipos de declaraciones para C-minus
class DeclKind(Enum):
    VarK = 0
    FunK = 1
    ParamK = 2

# Tipos de expresiones para comprobacion de tipos
class ExpType(Enum):
    Void = 0
    Integer = 1
    Boolean = 2
    Array = 3

# Maximo numero de hijos por nodo
MAXCHILDREN = 3

# Diccionario de palabras reservadas para busqueda eficiente
RESERVED_WORDS = {
    'else': TokenType.ELSE,
    'if': TokenType.IF,
    'int': TokenType.INT,
    'return': TokenType.RETURN,
    'void': TokenType.VOID,
    'while': TokenType.WHILE
}

class TreeNode:
    def __init__(self):
        self.child = [None] * MAXCHILDREN # Hijos del nodo
        self.sibling = None # Hermano del nodo
        self.lineno = 0 # Numero de linea
        self.nodekind = None # Tipo de nodo (StmtK, ExpK, DeclK)
        
        # Tipos especificos segun el tipo de nodo
        self.stmt = None # StmtKind
        self.exp = None # ExpKind
        self.decl = None # DeclKind
        
        # Atributos del nodo
        self.op = None # TokenType (para operadores)
        self.val = None # int (para constantes)
        self.name = None # str (para identificadores)
        self.type = None # ExpType (para checkeo de tipos)
        
        # Atributos adicionales para C-
        self.is_array = False # Indica si es un arreglo
        self.array_size = None # Tamaño del arreglo
        self.params = [] # Parametros (para funciones)
        self.is_function_body = False # Indica si es el cuerpo de una funcion