from globalTypes import *

# Variables globales
programa = "" # Contiene el string completo del programa
posicion = 0 # Posicion actual en el programa
progLong = 0 # Longitud original del programa
lineno = 1 # Numero de linea actual
linepos = 0 # Posicion en la linea actual

# Variables para guardar el estado para lookahead
saved_position = None
saved_linepos = None
saved_lineno = None

def globales(prog, pos, long):
    """Funcion para recibir variables globales desde el programa principal"""
    global programa, posicion, progLong
    programa = prog
    posicion = pos
    progLong = long

def reservedLookup(tokenString):
    """Busca si un identificador es palabra reservada"""
    # Usar el diccionario para busqueda eficiente
    return RESERVED_WORDS.get(tokenString, TokenType.ID)

def getChar():
    """Obtiene el siguiente caracter del programa"""
    global posicion, linepos
    if posicion < len(programa):
        c = programa[posicion]
        posicion += 1
        linepos += 1
        return c
    return '$' # Fin de archivo

def ungetChar():
    """Retrocede un caracter"""
    global posicion, linepos
    if posicion > 0:
        posicion -= 1
        linepos -= 1

def peek():
    """Mira el siguiente caracter sin avanzar"""
    if posicion < len(programa):
        return programa[posicion]
    return '$'

def getLine():
    """Obtiene la linea actual completa"""
    global programa, posicion
    
    # Encontrar el inicio de la linea actual
    start = posicion - linepos
    
    # Encontrar el final de la linea
    end = start
    while end < len(programa) and programa[end] != '\n':
        end += 1
    
    return programa[start:end]

def getLinePosition():
    """Obtiene la posicion actual en la linea"""
    global linepos
    return linepos

def printError(message, errorPos=None):
    """Imprime un mensaje de error con la linea y la posicion"""
    global lineno, linepos
    
    line = getLine()
    pos = errorPos if errorPos is not None else linepos - 1
    
    print(f"Linea {lineno}: {message}")
    print(line)
    print(" " * pos + "^")

def saveState():
    """Guarda el estado actual del scanner para lookahead"""
    global posicion, linepos, lineno, saved_position, saved_linepos, saved_lineno
    saved_position = posicion
    saved_linepos = linepos
    saved_lineno = lineno

def restoreState():
    """Restaura el estado guardado del scanner"""
    global posicion, linepos, lineno, saved_position, saved_linepos, saved_lineno
    if saved_position is not None:
        posicion = saved_position
        linepos = saved_linepos
        lineno = saved_lineno
        
        # Limpiar el estado guardado
        saved_position = None
        saved_linepos = None
        saved_lineno = None
        return True
    return False

def getToken(imprime=True):
    """Obtiene el siguiente token del programa"""
    global lineno, linepos
    
    # Inicializar variables
    tokenString = "" # String para almacenar el token
    tokenType = None # Tipo del token (valor de TokenType)
    state = StateType.START # Estado actual - siempre comienza en START
    save = True # Bandera para indicar si se guarda en tokenString
    
    # Loop principal del automata
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
                    getChar() # Consume el '*'
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
                if c == '$': # EOF
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
                getChar() # Consume el '/'
                state = StateType.START
            elif c == '\n':
                lineno += 1
                linepos = 0
            elif c == '$': # EOF en medio de un comentario
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
                printError("Se esperaba '=' despues de '!'")
        
        else: # Nunca deberia ocurrir
            state = StateType.DONE
            tokenType = TokenType.ERROR
            printError("Error en el analizador lexico")
        
        # Guardar el caracter en tokenString si es necesario
        if save and c != '$':
            tokenString += c
    
    # Si es un ID, verificar si es una palabra reservada
    if tokenType == TokenType.ID:
        tokenType = reservedLookup(tokenString)
    
    # Imprimir el token si se requiere
    if imprime and tokenType != TokenType.ERROR:
        print(f"{lineno:4d}: {tokenType.name:10s} = {tokenString}")
    
    return tokenType, tokenString, lineno