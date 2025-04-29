from enum import Enum

# TokenType - Definición de todos los tokens del lenguaje C-minus
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
    NUM = 311 # numeros
    
    # Símbolos especiales
    PLUS = '+' # suma
    MINUS = '-' # resta
    TIMES = '*' # multiplicacion
    DIVIDE = '/' # division
    LT = '<' # menor que
    LTE = '<=' # menor o igual que
    GT = '>' # mayor que
    GTE = '>=' # mayor o igual que
    EQ = '==' # igual a
    NEQ = '!=' # no igual a
    ASSIGN = '=' # asignacion
    SEMI = ';' # punto y coma
    COMMA = ',' # coma
    LPAREN = '(' # parentesis izquierdo
    RPAREN = ')' # parentesis derecho
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
    SubscriptK = 4  # Para indexación de arreglos

# Tipos de declaraciones para C-minus
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