# -----------------------------------------------------------------------------
# semantica.py
#
# Implementación del análisis semántico para C-
# Incluye llenado e impresión de tabla de símbolos y chequeo de tipos.
# Autor: Omar Rivera Arenas
# -----------------------------------------------------------------------------

from globalTypes import *
from lexer import lineno, programa, get_line_text, posicion
from symtab import SymbolEntry, st_enter_scope, st_exit_scope, current_scope, scope_stack, scopes_done
import copy

# Tabla de símbolos global (stack de scopes)
# Estructura de símbolo
class Symbol:
    def __init__(self, name, kind, typ, lineno, is_array=False, size=None, params=None, return_type=None):
        self.name = name
        self.kind = kind  # 'var', 'func', 'param', etc.
        self.typ = typ    # TokenType.INT, TokenType.VOID, etc.
        self.lineno = lineno
        self.is_array = is_array
        self.size = size
        self.params = params if params is not None else []
        self.return_type = return_type
        self.lines = [lineno]  # Líneas donde se usa

class ErrorTypeClass:
    pass
ErrorType = ErrorTypeClass()

def report_error(lineno, col, msg):
    """Imprime error con línea fuente y caret bajo la columna."""
    # Buscar inicio y fin de la línea
    lines = programa.split('\n')
    if 1 <= lineno <= len(lines):
        line_text = lines[lineno-1]
    else:
        line_text = ""
    print(f"\n>> Error semántico (línea {lineno}, col {col}): {msg}")
    print(line_text)
    print(' ' * (col - 1) + '^')

def stringify(token_or_type):
    # Acepta TokenType / ExpType / NodeKind y devuelve solo el nombre
    return token_or_type.name if hasattr(token_or_type, "name") else str(token_or_type)

def printSymTab():
    from symtab import scopes_done
    print("\n--- Tabla de símbolos por scope ---")
    for level, table in enumerate(scopes_done):
        print(f"\nScope {level} (nivel {level}):")
        print(f"{'Nombre':<12}{'Tipo':<8}{'Kind':<9}{'Atributos':<25}{'Líneas':<15}")
        for e in table.values():
            tipo  = e.typ.name if hasattr(e.typ,"name") else (str(e.typ) if e.typ is not None else "")
            kind  = e.kind if e.kind is not None else ""
            attrs = []
            if kind == 'func':
                params = ','.join(p[0].name + ('[]' if p[1] else '') for p in e.params)
                attrs.append(f"params({params}) -> {e.return_type.name if hasattr(e.return_type,'name') else e.return_type}")
            elif e.is_array:
                attrs.append(f"array[{e.size}]")
            print(f"{e.name:<12}{tipo:<8}{kind:<9}{' '.join(attrs):<25}{e.lines}")
    print("\n--- Fin tabla de símbolos ---")


def tabla(tree, imprime=True):
    """Recorre el AST, llena e imprime la tabla de símbolos por scope."""
    global scope_stack, scopes_done
    from symtab import scope_stack, scopes_done
    scope_stack = [{}]
    scopes_done.clear()
    build_symtab(tree)
    if imprime:
        printSymTab()

def es_inicio_de_nuevo_scope(t):
    return hasattr(t, 'nodekind') and t.nodekind == NodeKind.StmtK and hasattr(t, 'stmt') and t.stmt == StmtKind.CompoundK

def es_fin_de_scope(t):
    return es_inicio_de_nuevo_scope(t)

def traverse(node, insertNode, exitNode):
    if node is None:
        return
    insertNode(node)
    for child in getattr(node, 'child', []):
        traverse(child, insertNode, exitNode)
    exitNode(node)

def build_symtab(tree):
    global scope_stack, scopes_done
    scope_stack = [{}]  # Scope 0 vive todo el tiempo
    scopes_done = []
    tree.is_global = True
    traverse(tree, insertNode, exitNode)

def insertNode(t):
    from symtab import st_insert, st_enter_scope
    # FUNCIÓN (CompoundK con nombre y tipo)
    if (t.nodekind == NodeKind.StmtK
        and t.stmt == StmtKind.CompoundK
        and getattr(t, "name", None)
        and getattr(t, "return_type", None)):
        st_insert(
            name=t.name,
            kind='func',
            typ=t.return_type,
            params=[(p['typ'], p['is_array']) for p in t.params],
            return_type=t.return_type,
            lineno=t.lineno
        )
        st_enter_scope()
        return
    elif t.nodekind == NodeKind.StmtK and t.stmt == StmtKind.VarDeclK:
        st_insert(
            name=t.name,
            kind='var',
            typ=getattr(t, 'var_type', None),
            lineno=t.lineno
        )
    # BLOQUE compuesto normal (no global, no función, no cuerpo de función)
    elif (t.nodekind == NodeKind.StmtK and
          t.stmt == StmtKind.CompoundK and
          not getattr(t, "is_global", False) and not getattr(t, "name", None) and not getattr(t, "return_type", None) and not getattr(t, "is_func_body", False)):
        st_enter_scope()
    # Uso de identificador
    if hasattr(t, 'exp') and t.exp == ExpKind.IdK and hasattr(t, 'name') and t.name:
        entry = None
        for scope in reversed(scope_stack):
            if t.name in scope:
                entry = scope[t.name]
                break
        if entry:
            if t.lineno not in entry.lines:
                entry.lines.append(t.lineno)

def exitNode(t):
    from symtab import st_exit_scope
    if (t.nodekind == NodeKind.StmtK and
        t.stmt == StmtKind.CompoundK and
        not getattr(t, "is_global", False)):
        st_exit_scope()

def symtab_insert(name, kind, typ, lineno, is_array=False, size=None, params=None, return_type=None):
    if not scope_stack:
        scope_stack.append({})
    current_scope = scope_stack[-1]
    if name in current_scope:
        print_semantic_error(f"Identificador '{name}' ya declarado en este scope", lineno, name)
    else:
        current_scope[name] = Symbol(name, kind, typ, lineno, is_array, size, params, return_type)

def print_semantic_error(msg, lineno, lexema):
    # Buscar la columna del lexema en la línea fuente
    lines = programa.split('\n')
    if 1 <= lineno <= len(lines):
        line_text = lines[lineno-1]
        col = line_text.find(str(lexema)) + 1 if lexema and str(lexema) in line_text else 1
    else:
        col = 1
    report_error(lineno, col, msg)

def semantica(tree, imprime=True):
    """Función principal: tabla + chequeo de tipos (con errores de tipo)."""
    tabla(tree, imprime)
    type_check(tree)

def lookup_symbol(name):
    for scope in reversed(scope_stack):  # Busca desde el scope actual hacia el global
        if name in scope:
            return scope[name]
    return None

def type_check(node, current_func=None):
    if node is None:
        return ErrorType
    tipos = []
    for child in node.child:
        tipos.append(type_check(child, current_func))

    # --- Expresiones aritméticas ---
    if node.nodekind == NodeKind.ExpK and node.exp == ExpKind.OpK:
        if node.op in (TokenType.PLUS, TokenType.MINUS, TokenType.TIMES, TokenType.DIVIDE):
            if all(t == ExpType.Integer for t in tipos):
                return ExpType.Integer
            else:
                report_error(node.lineno, getattr(node, 'column', 1), "Operadores aritméticos requieren enteros")
                return ErrorType
        if node.op in (TokenType.LT, TokenType.GT, TokenType.LTE, TokenType.GTE, TokenType.EQ, TokenType.NEQ):
            if all(t == ExpType.Integer for t in tipos):
                return ExpType.Boolean
            else:
                report_error(node.lineno, getattr(node, 'column', 1), "Comparadores requieren enteros")
                return ErrorType
        if node.op == TokenType.ASSIGN:
            left_type = tipos[0]
            right_type = tipos[1]
            if left_type != ExpType.Integer or right_type != ExpType.Integer:
                report_error(node.lineno, getattr(node, 'column', 1), "Tipo incompatible en asignación")
                return ErrorType
            return ExpType.Integer

    # --- Constantes ---
    if node.nodekind == NodeKind.ExpK and node.exp == ExpKind.ConstK:
        return ExpType.Integer

    # --- Acceso a arreglo: SubscriptK ---
    if node.nodekind == NodeKind.ExpK and node.exp == ExpKind.SubscriptK:
        from symtab import scope_stack
        entry = None
        for scope in reversed(scope_stack):
            if node.name in scope:
                entry = scope[node.name]
                break
        if entry is None:
            report_error(node.lineno, getattr(node, 'column', 1), f"Variable '{node.name}' no declarada")
            return ErrorType
        if not getattr(entry, 'is_array', False):
            report_error(node.lineno, getattr(node, 'column', 1), f"'{node.name}' no es un arreglo")
            return ErrorType
        # Chequea que el índice sea int
        idx_type = type_check(node.child[0], current_func)
        if idx_type != ExpType.Integer:
            report_error(node.lineno, getattr(node, 'column', 1), "Índice de arreglo debe ser entero")
            return ErrorType
        return ExpType.Integer  # Tipo base del arreglo

    # --- Identificadores (variables simples) ---
    if node.nodekind == NodeKind.ExpK and node.exp == ExpKind.IdK:
        from symtab import scope_stack
        entry = None
        for scope in reversed(scope_stack):
            if node.name in scope:
                entry = scope[node.name]
                break
        if entry:
            # Acceso a arreglo: node.child[0] es el índice
            if entry.is_array:
                if node.child[0] is not None:
                    idx_type = type_check(node.child[0], current_func)
                    if idx_type != ExpType.Integer:
                        report_error(node.lineno, getattr(node, 'column', 1), "Índice de arreglo debe ser entero")
                        return ErrorType
                    return ExpType.Integer  # Acceso a elemento
                else:
                    return ExpType.Integer  # Referencia al arreglo completo
            else:
                if node.child[0] is not None:
                    report_error(node.lineno, getattr(node, 'column', 1), "Variable no es arreglo, no se puede indexar")
                    return ErrorType
                return ExpType.Integer
        else:
            report_error(node.lineno, getattr(node, 'column', 1), f"Variable '{node.name}' no declarada")
            return ErrorType

    # --- Llamadas a función ---
    if node.nodekind == NodeKind.ExpK and node.exp == ExpKind.CallK:
        from symtab import scope_stack
        entry = None
        for scope in reversed(scope_stack):
            if node.name in scope:
                entry = scope[node.name]
                break
        if entry is None or entry.kind != 'func':
            report_error(node.lineno, getattr(node, 'column', 1), f"Función '{node.name}' no declarada")
            return ErrorType
        # Verificar argumentos
        expected_params = entry.params
        actual_args = []
        arg = node.child[0]
        while arg is not None:
            actual_args.append(arg)
            arg = arg.sibling
        if len(actual_args) != len(expected_params):
            report_error(node.lineno, getattr(node, 'column', 1), f"Número incorrecto de argumentos en llamada a '{node.name}'")
            return entry.return_type or ErrorType
        for i, (arg_node, param_info) in enumerate(zip(actual_args, expected_params)):
            arg_type = type_check(arg_node, current_func)
            param_typ = param_info[0] if isinstance(param_info, (list, tuple)) else param_info.get('typ', ExpType.Integer)
            # Solo chequeo de tipo base (ExpType)
            if arg_type != param_typ:
                report_error(node.lineno, getattr(node, 'column', 1), f"Tipo incorrecto para argumento {i+1} en llamada a '{node.name}'")
        return entry.return_type or ErrorType

    # --- Sentencias de control ---
    if node.nodekind == NodeKind.StmtK:
        # if
        if node.stmt == StmtKind.IfK:
            cond_type = tipos[0]
            if cond_type not in (ExpType.Boolean, ExpType.Integer):
                report_error(node.lineno, getattr(node, 'column', 1), "Condición de if debe ser booleana o entera")
        # while
        if node.stmt == StmtKind.WhileK:
            cond_type = tipos[0]
            if cond_type not in (ExpType.Boolean, ExpType.Integer):
                report_error(node.lineno, getattr(node, 'column', 1), "Condición de while debe ser booleana o entera")
        # return
        if node.stmt == StmtKind.ReturnK:
            # Buscar tipo de retorno de la función actual
            func_type = current_func['return_type'] if current_func else None
            ret_type = tipos[0] if len(tipos) > 0 else None
            if func_type is not None:
                if ret_type != func_type:
                    report_error(node.lineno, getattr(node, 'column', 1), "Tipo de retorno incorrecto")
        # CompoundK (bloque): si es función, actualizar current_func
        if node.stmt == StmtKind.CompoundK and hasattr(node, 'name') and node.name:
            # Es un bloque de función
            current_func = {'return_type': node.return_type}

    # Chequear hermanos
    type_check(node.sibling, current_func)
    return ErrorType