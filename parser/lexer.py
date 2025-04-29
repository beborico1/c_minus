from globalTypes import *

# Variables globales
programa = "" # Contiene el string completo del programa
posicion = 0 # Posicion actual en el programa
progLong = 0 # Longitud original del programa
lineno = 1 # Numero de linea actual
linepos = 0 # Posicion en la linea actual

# Variable para guardar el estado para lookahead
saved_token = None
saved_tokenString = None
saved_lineno = None

def globales(prog, pos, long):
    """
    Funcion para recibir variables globales desde el programa principal
    
    Args:
        prog: String con el programa completo
        pos: Posicion inicial
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
    return '$' # Fin de archivo

def ungetChar():
    """
    Retrocede un caracter
    """
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
    Obtiene la linea actual completa
    
    Returns:
        String con la linea actual
    """
    global programa, posicion, linepos
    
    # Encontrar el inicio de la linea actual
    start = posicion - linepos
    
    # Encontrar el final de la linea
    end = start
    while end < len(programa) and programa[end] != '\n':
        end += 1
    
    return programa[start:end]

def getLinePosition():
    """
    Obtiene la posicion actual en la linea
    
    Returns:
        Posicion en la linea actual
    """
    global linepos
    return linepos

def printError(message, errorPos=None):
    """
    Imprime un mensaje de error con la linea y la posicion
    
    Args:
        message: Mensaje de error
        errorPos: Posicion del error en la linea
    """
    global lineno, linepos
    
    line = getLine()
    pos = errorPos if errorPos is not None else linepos - 1
    
    print(f"Linea {lineno}: {message}")
    print(line)
    print(" " * pos + "^")

def saveToken():
    """
    Guarda el token actual para lookahead
    """
    global token, tokenString, lineno, saved_token, saved_tokenString, saved_lineno
    
    saved_token = token
    saved_tokenString = tokenString
    saved_lineno = lineno

def ungetToken():
    """
    Restaura el token previamente guardado
    
    Returns:
        True si se restauro un token, False en caso contrario
    """
    global token, tokenString, lineno, saved_token, saved_tokenString, saved_lineno
    
    if saved_token is not None:
        token = saved_token
        tokenString = saved_tokenString
        lineno = saved_lineno
        
        # Limpiar el estado guardado
        saved_token = None
        saved_tokenString = None
        saved_lineno = None
        return True
    return False

def reservedLookup(tokenString):
    """
    Busca si un identificador es palabra reservada
    
    Args:
        tokenString: String a buscar
        
    Returns:
        TokenType correspondiente a la palabra reservada o TokenType.ID
    """
    # Usar el diccionario para busqueda eficiente
    return RESERVED_WORDS.get(tokenString, TokenType.ID)

def getToken(imprime=True):
    """
    Obtiene el siguiente token del programa
    
    Args:
        imprime: Indica si se debe imprimir el token
        
    Returns:
        Tupla (token, tokenString, lineno)
    """
    global token, tokenString, lineno, linepos, posicion
    
    # Reiniciar tokenString
    tokenString = ""
    
    # Estado inicial del automata
    state = StateType.START
    
    # Bandera para indicar si se guarda en tokenString
    
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
            elif c == '&':
                nextChar = peek()
                if nextChar == '&':
                    save = True
                    getChar() # Consume el segundo '&'
                    state = StateType.DONE
                    tokenType = TokenType.AND
                else:
                    state = StateType.DONE
                    tokenType = TokenType.ERROR
                    printError("Se esperaba '&' despues de '&'")
            elif c == '|':
                nextChar = peek()
                if nextChar == '|':
                    save = True
                    getChar() # Consume el segundo '|'
                    state = StateType.DONE
                    tokenType = TokenType.OR
                else:
                    state = StateType.DONE
                    tokenType = TokenType.ERROR
                    printError("Se esperaba '|' despues de '|'")
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
    
    # Establecer variables globales
    token = tokenType
    
    # Imprimir el token si se requiere
    if imprime and tokenType != TokenType.ERROR:
        print(f"{lineno:4d}: {tokenType.name:10s} = {tokenString}")
    
    return (token, tokenString, lineno)