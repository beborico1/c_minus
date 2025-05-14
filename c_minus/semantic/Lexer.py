from globalTypes import *

# Variables globales
programa = "" # Contiene el string completo del programa
posicion = 0 # Posicion actual en el programa
progLong = 0 # Longitud original del programa
lineno = 1 # Numero de linea actual
linepos = 0 # Posicion en la linea actual

# Variable para guardar el estado para lookahead
saved_state = None

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
    
def getChar():
    """
    Obtiene el siguiente caracter del programa
    
    Returns:
        Siguiente caracter o EOF
    """
    global posicion, progLong, lineno, linepos
    
    if posicion >= progLong:
        return '$' # Fin de archivo
    
    # Obtener el siguiente caracter
    c = programa[posicion]
    posicion += 1
    linepos += 1
    
    # Incrementar contador de linea si encontramos '\n'
    if c == '\n':
        lineno += 1
        linepos = 0
    
    return c

def ungetChar():
    """
    Retrocede un caracter en el programa
    """
    global posicion, lineno, linepos
    
    if posicion > 0:
        posicion -= 1
        
        # Si retrocedemos sobre un salto de linea, decrementar linea
        if programa[posicion] == '\n':
            lineno -= 1
            # Calcular la posicion en la linea anterior
            linepos = 0
            pos = posicion - 1
            while pos >= 0 and programa[pos] != '\n':
                linepos += 1
                pos -= 1
        else:
            linepos -= 1

def getLine():
    """
    Obtiene la linea actual completa para mostrar errores
    
    Returns:
        Linea actual como string
    """
    global programa, posicion, progLong
    
    # Encontrar el inicio de la linea actual
    inicio = posicion - linepos
    
    # Encontrar el final de la linea
    fin = inicio
    while fin < progLong and programa[fin] != '\n':
        fin += 1
    
    return programa[inicio:fin]

def printError(message, errorPos=None):
    """
    Imprime un mensaje de error con la linea y la posicion
    
    Args:
        message: Mensaje de error
        errorPos: Posicion del error en la linea
    """
    global linepos, lineno
    
    # Obtener la linea actual
    line = getLine()
    pos = errorPos if errorPos is not None else linepos - 1
    
    print(f"Línea {lineno}: {message}")
    print(line)
    print(" " * pos + "^")

def save_state():
    """
    Guarda el estado actual del analizador para lookahead
    """
    global saved_state, posicion, linepos, lineno
    saved_state = (posicion, linepos, lineno)

def restore_state():
    """
    Restaura el estado guardado previamente
    """
    global saved_state, posicion, linepos, lineno
    if saved_state is not None:
        posicion, linepos, lineno = saved_state
        # Limpiar el estado guardado
        saved_state = None

def reserved_lookup(word):
    """
    Busca una palabra en el diccionario de palabras reservadas
    
    Args:
        word: Palabra a buscar
        
    Returns:
        Token correspondiente a la palabra reservada o ID si no es reservada
    """
    if word in RESERVED_WORDS:
        return RESERVED_WORDS[word]
    return TokenType.ID

def getToken(imprime=True):
    """
    Obtiene el siguiente token del programa
    
    Args:
        imprime: Indica si se debe imprimir el token
        
    Returns:
        Una tupla (token, tokenString, lineno)
    """
    global lineno, linepos
    
    # Reiniciar tokenString
    tokenString = ""
    
    # Estado inicial del automata
    state = StateType.START
    
    # Bandera para indicar si se guarda en tokenString
    save = True
    
    # Loop principal del automata
    while state != StateType.DONE:
        c = getChar()
        save = True
        
        if state == StateType.START:
            if c.isalpha():
                state = StateType.INID
            elif c.isdigit():
                state = StateType.INNUM
            elif c == ' ' or c == '\t' or c == '\n':
                save = False
            elif c == '&':
                save = False
                c2 = getChar()
                if c2 == '&':
                    tokenString = '&&'
                    state = StateType.DONE
                    tokenType = TokenType.AND
                else:
                    ungetChar()
                    tokenType = TokenType.ERROR
                    printError("Se esperaba '&' después de '&'")
                    state = StateType.DONE
            elif c == '|':
                save = False
                c2 = getChar()
                if c2 == '|':
                    tokenString = '||'
                    state = StateType.DONE
                    tokenType = TokenType.OR
                else:
                    ungetChar()
                    tokenType = TokenType.ERROR
                    printError("Se esperaba '|' después de '|'")
                    state = StateType.DONE
            elif c == '*':
                state = StateType.DONE
                tokenType = TokenType.TIMES
            elif c == '+':
                state = StateType.DONE
                tokenType = TokenType.PLUS
            elif c == '-':
                state = StateType.DONE
                tokenType = TokenType.MINUS
            elif c == '/':
                save = False
                c2 = getChar()
                if c2 == '*':
                    save = False
                    state = StateType.INCOMMENT
                else:
                    ungetChar()
                    state = StateType.DONE
                    tokenType = TokenType.DIVIDE
                    tokenString = '/'
            elif c == '$': # EOF
                save = False
                state = StateType.DONE
                tokenType = TokenType.ENDFILE
            elif c == '=':
                state = StateType.INASSIGN
            elif c == '<':
                state = StateType.INLT
            elif c == '>':
                state = StateType.INGT
            elif c == '!':
                state = StateType.INNOT
            elif c == ';':
                state = StateType.DONE
                tokenType = TokenType.SEMI
            elif c == ',':
                state = StateType.DONE
                tokenType = TokenType.COMMA
            elif c == '(':
                state = StateType.DONE
                tokenType = TokenType.LPAREN
            elif c == ')':
                state = StateType.DONE
                tokenType = TokenType.RPAREN
            elif c == '[':
                state = StateType.DONE
                tokenType = TokenType.LBRACKET
            elif c == ']':
                state = StateType.DONE
                tokenType = TokenType.RBRACKET
            elif c == '{':
                state = StateType.DONE
                tokenType = TokenType.LBRACE
            elif c == '}':
                state = StateType.DONE
                tokenType = TokenType.RBRACE
            else:
                state = StateType.DONE
                tokenType = TokenType.ERROR
                printError(f"Carácter ilegal: '{c}'")
                
        elif state == StateType.INCOMMENT:
            save = False
            if c == '*':
                c2 = getChar() # Consume el '*'
                if c2 == '/':
                    state = StateType.START
                else:
                    ungetChar()
            elif c == '$': # EOF en medio de un comentario
                save = False
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
            if not c.isalnum():
                ungetChar()
                save = False
                state = StateType.DONE
                tokenType = TokenType.ID
        
        elif state == StateType.INASSIGN:
            if c == '=':
                state = StateType.DONE
                tokenType = TokenType.EQ
            else:
                ungetChar()
                save = False
                state = StateType.DONE
                tokenType = TokenType.ASSIGN
        
        elif state == StateType.INLT:
            if c == '=':
                state = StateType.DONE
                tokenType = TokenType.LTE
            else:
                ungetChar()
                save = False
                state = StateType.DONE
                tokenType = TokenType.LT
        
        elif state == StateType.INGT:
            if c == '=':
                state = StateType.DONE
                tokenType = TokenType.GTE
            else:
                ungetChar()
                save = False
                state = StateType.DONE
                tokenType = TokenType.GT
        
        elif state == StateType.INNOT:
            if c == '=':
                state = StateType.DONE
                tokenType = TokenType.NEQ
            else:
                ungetChar()
                save = False
                state = StateType.DONE
                tokenType = TokenType.ERROR
                printError("Se esperaba '=' después de '!'")
                
        else: # Nunca deberia ocurrir
            save = False
            state = StateType.DONE
            tokenType = TokenType.ERROR
            printError("Error en el analizador léxico")
        
        # Guardar el caracter en tokenString si es necesario
        if save and c != '$':
            tokenString += c
    
    # Si es un ID, verificar si es una palabra reservada
    if tokenType == TokenType.ID:
        tokenType = reserved_lookup(tokenString)
    
    # Establecer variables globales
    current_token = tokenType
    
    # Imprimir el token si se requiere
    if imprime and tokenType != TokenType.ERROR:
        print(f"{lineno:4d}: {tokenType.name:10s} = {tokenString}")
    
    return (tokenType, tokenString, lineno)