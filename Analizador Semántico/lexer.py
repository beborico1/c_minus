# ----------------------------------------------------------------------------
# 
# Programa basado en los documentos de clase.
# Se utilizó también apoyo de herramientas de inteligencia artificial (como GPT) 
# para estructurar, corregir y perfeccionar algunas secciones del código.
#
# Autor: Omar Rivera Arenas
# Fecha: 28 de abril de 2025
#
# Descripción:
# Este archivo implementa el analizador léxico (scanner) del lenguaje C-,
# encargado de convertir el texto fuente en una secuencia de tokens para el parser.
# ----------------------------------------------------------------------------

from globalTypes import *

# Variables globales del lexer
programa = ""
posicion = 0
progLong = 0
lineno = 1

def globales(prog, pos, long):
    global programa, posicion, progLong
    programa = prog
    posicion = pos
    progLong = long

def reserved_lookup(lexema):
    """Verifica si un lexema es una palabra reservada."""
    return reserved_words.get(lexema, TokenType.ID)

def getToken(imprime=True):
    """Obtiene el siguiente token del string fuente."""
    global programa, posicion, progLong, lineno

    state = StateType.START
    lexema = ""
    token = None
    token_column = None
    start_pos = posicion
    # Calcular columna de inicio
    line_start = programa.rfind('\n', 0, posicion) + 1
    token_column = posicion - line_start + 1

    while state != StateType.DONE:
        if posicion >= progLong:
            return TokenType.ENDFILE, "$", lineno, token_column
        c = programa[posicion]
        save = True
        if state == StateType.START:
            if c in " \t\n":
                save = False
                if c == "\n":
                    lineno += 1
                posicion += 1
                # Recalcular columna para el siguiente token
                line_start = programa.rfind('\n', 0, posicion) + 1
                token_column = posicion - line_start + 1
                continue
            elif c.isdigit():
                state = StateType.INNUM
            elif c.isalpha():
                state = StateType.INID
            else:
                state = StateType.DONE
                # símbolos y operadores
                if c == '=':
                    if programa[posicion + 1] == '=':
                        lexema = "=="
                        posicion += 1
                        save = False
                        token = TokenType.EQ
                    else:
                        token = TokenType.ASSIGN
                elif c == '!':
                    if programa[posicion + 1] == '=':
                        lexema = "!="
                        posicion += 1
                        save = False
                        token = TokenType.NEQ
                    else:
                        token = TokenType.ERROR
                elif c == '<':
                    if programa[posicion + 1] == '=':
                        lexema = "<="
                        posicion += 1
                        save = False
                        token = TokenType.LTE
                    else:
                        token = TokenType.LT
                elif c == '>':
                    if programa[posicion + 1] == '=':
                        lexema = ">="
                        posicion += 1
                        save = False
                        token = TokenType.GTE
                    else:
                        token = TokenType.GT
                elif c == '+': token = TokenType.PLUS
                elif c == '-': token = TokenType.MINUS
                elif c == '*': token = TokenType.TIMES
                elif c == '/': token = TokenType.DIVIDE
                elif c == ';': token = TokenType.SEMI
                elif c == ',': token = TokenType.COMMA
                elif c == '(': token = TokenType.LPAREN
                elif c == ')': token = TokenType.RPAREN
                elif c == '{': token = TokenType.LBRACE
                elif c == '}': token = TokenType.RBRACE
                elif c == '[': token = TokenType.LBRACKET
                elif c == ']': token = TokenType.RBRACKET
                elif c == '$': token = TokenType.ENDFILE
                else: token = TokenType.ERROR
        elif state == StateType.INNUM:
            if c.isalpha():
                state = StateType.DONE
                token = TokenType.ERROR
                save = False
                print(f"Error léxico: número mal formado en '{lexema + c}'")
                continue
            elif not c.isdigit():
                state = StateType.DONE
                token = TokenType.NUM
                save = False
                continue
        elif state == StateType.INID:
            if not c.isalnum():
                state = StateType.DONE
                token = reserved_lookup(lexema)
                save = False
                continue
        if save:
            lexema += c
        posicion += 1
    if imprime:
        print(f"{token.name:10s} = {lexema}")
    return token, lexema, lineno, token_column

def get_line_text(lineno):
    return programa.split('\n')[lineno - 1]