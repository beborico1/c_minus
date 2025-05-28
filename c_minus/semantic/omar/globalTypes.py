from enum import Enum, auto

class TokenType(Enum):
    # Tokens especiales
    ENDFILE = 0      # Fin de archivo
    ERROR = 1        # Token inválido

    # Palabras reservadas
    INT = 2
    VOID = 3
    IF = 4
    ELSE = 5
    WHILE = 6
    RETURN = 7
    INPUT = 8
    OUTPUT = 9

    # Tokens básicos
    ID = 11          # Identificadores
    NUM = 12         # Constantes numéricas

    # Operadores y símbolos
    ASSIGN = 13
    EQ = 14
    NEQ = 15
    LT = 16
    LTE = 17
    GT = 18
    GTE = 19
    PLUS = 20
    MINUS = 21
    TIMES = 22
    DIVIDE = 23
    SEMI = 24
    COMMA = 25
    LPAREN = 26
    RPAREN = 27
    LBRACE = 28
    RBRACE = 29
    LBRACKET = 30
    RBRACKET = 31

class StateType(Enum):
    # Estados utilizados en el DFA del lexer
    START = 0
    INNUM = 1
    INID = 2
    DONE = 3
    INCOMMENT = 4

# Diccionario de palabras reservadas para búsqueda rápida
reserved_words = {
    "int": TokenType.INT,
    "void": TokenType.VOID,
    "if": TokenType.IF,
    "else": TokenType.ELSE,
    "while": TokenType.WHILE,
    "return": TokenType.RETURN,
    "input": TokenType.INPUT,
    "output": TokenType.OUTPUT,
}

# Tipos de nodos en el árbol sintáctico
class NodeKind(Enum):
    StmtK = 0
    ExpK = 1

class StmtKind(Enum):
    IfK = 0
    RepeatK = 1
    AssignK = 2
    ReadK = 3
    WriteK = 4
    VarDeclK = 5
    CompoundK = 6
    WhileK = 7
    ReturnK = 8
    OutputK = 9
    InputK = 10

class ExpKind(Enum):
    OpK = auto()
    ConstK = auto()
    IdK = auto()
    CallK = auto()
    SubscriptK = auto() 

class ExpType(Enum):
    Void = 0
    Integer = 1
    Boolean = 2

# Constante para el máximo número de hijos en un nodo
MAXCHILDREN = 3

# Definición de la clase TreeNode para el AST
class TreeNode:
    def __init__(self):
        self.child = [None] * MAXCHILDREN
        self.sibling = None
        self.lineno = 0
        self.column = 1  # Nueva: columna de inicio del token
        self.nodekind = None
        self.stmt = None
        self.exp = None
        self.op = None
        self.val = None
        self.name = None
        self.type = None
        # Extensiones para AST enriquecido
        self.typ = None         # Tipo de variable o parámetro (TokenType.INT, TokenType.VOID)
        self.is_array = False   # True si es arreglo
        self.array_size = None # Tamaño del arreglo si aplica
        self.return_type = None # Tipo de retorno de función (TokenType.INT, TokenType.VOID)
        self.params = []        # Lista de parámetros (cada uno: dict con typ, is_array, array_size)