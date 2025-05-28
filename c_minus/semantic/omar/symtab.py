# symtab.py

import copy

class SymbolEntry:
    def __init__(self, name, kind, typ,
                 is_array=False, size=None,
                 params=None, return_type=None, lineno=0):
        self.name = name
        self.kind = kind          # 'var' | 'param' | 'func'
        self.typ = typ            # INT | VOID | BOOL
        self.is_array = is_array
        self.size = size          # solo para arrays
        self.params = params or []    # lista de (typ, is_array)
        self.return_type = return_type
        self.lines = [lineno]

# Stack de scopes: lista de diccionarios (uno por scope)
scope_stack = [{}]   # scope 0 (global)
scopes_done = []     # lista de todos los scopes que existieron

def st_enter_scope():
    scope_stack.append({})

def st_exit_scope():
    finished = scope_stack.pop()
    scopes_done.insert(0, copy.deepcopy(finished))  # insert al inicio para que el global quede como Scope 0

def st_insert(name, **kwargs):
    entry = SymbolEntry(name=name, **kwargs)
    current_scope = scope_stack[-1]            # tope de pila
    if name in current_scope:                  # redefinición local
        current_scope[name].lines.append(kwargs["lineno"])
    else:
        current_scope[name] = entry

def current_scope():
    return scope_stack[-1] 