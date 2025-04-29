from enum import Enum

# TokenType - Definicion de todos los tokens del lenguaje C-
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
    
    # Simbolos especiales
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

# Diccionario de palabras reservadas para busqueda eficiente
RESERVED_WORDS = {
    'else': TokenType.ELSE,
    'if': TokenType.IF,
    'int': TokenType.INT,
    'return': TokenType.RETURN,
    'void': TokenType.VOID,
    'while': TokenType.WHILE
}