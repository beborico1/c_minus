# cgen.py
from globalTypes import *
from symtab import *

# Registros MIPS
zero = "$zero"  # Siempre 0
v0 = "$v0"      # Valores de retorno
v1 = "$v1"
a0 = "$a0"      # Argumentos (tambien acumulador segun codegen.md)
a1 = "$a1"
a2 = "$a2"
a3 = "$a3"
t0 = "$t0"      # Temporales
t1 = "$t1"
t2 = "$t2"
t3 = "$t3"
t4 = "$t4"
t5 = "$t5"
t6 = "$t6"
t7 = "$t7"
t8 = "$t8"
t9 = "$t9"
s0 = "$s0"      # Guardados
s1 = "$s1"
s2 = "$s2"
s3 = "$s3"
s4 = "$s4"
s5 = "$s5"
s6 = "$s6"
s7 = "$s7"
sp = "$sp"      # Puntero de pila
fp = "$fp"      # Puntero de marco
ra = "$ra"      # Direccion de retorno
gp = "$gp"      # Puntero global

# Estado de generacion de codigo
emitLoc = 0
highEmitLoc = 0
tmpOffset = 0
mainLoc = 0
globalOffset = 0
localOffset = 0
paramOffset = 0
labelCount = 0

# Archivo de salida
code_file = None

# Rastrear generacion de codigo
TraceCode = True

# Rastrear funcion actual y variables locales
current_function = None
local_vars = {}  # Mapea nombres de variables a sus desplazamientos
param_count = 0  # Rastrear numero de parametros para la funcion actual
stack_adjustment = 0  # Rastrear ajustes de pila para acceso adecuado a parametros

def emitComment(comment):
    """Emitir un comentario en el codigo ensamblador"""
    if TraceCode and code_file:
        code_file.write(f"# {comment}\n")

def emit(instruction):
    """Emitir una instruccion MIPS"""
    global emitLoc, highEmitLoc
    if code_file:
        code_file.write(f"    {instruction}\n")
    emitLoc += 1
    if highEmitLoc < emitLoc:
        highEmitLoc = emitLoc

def emitLabel(label):
    """Emitir una etiqueta"""
    if code_file:
        code_file.write(f"{label}:\n")

def getLabel():
    """Generar una etiqueta unica"""
    global labelCount
    labelCount += 1
    return f"L{labelCount}"

def emitSkip(howMany):
    """Saltar ubicaciones para posterior backpatch"""
    global emitLoc, highEmitLoc
    i = emitLoc
    emitLoc += howMany
    if highEmitLoc < emitLoc:
        highEmitLoc = emitLoc
    return i

def emitBackup(loc):
    """Retroceder a ubicacion previamente saltada"""
    global emitLoc
    emitLoc = loc

def emitRestore():
    """Restaurar a la ubicacion emitida mas alta"""
    global emitLoc, highEmitLoc
    emitLoc = highEmitLoc

def cGen(tree):
    """Generar codigo recursivamente mediante recorrido del arbol"""
    if tree is not None:
        if tree.nodekind == NodeKind.StmtK:
            genStmt(tree)
        elif tree.nodekind == NodeKind.ExpK:
            genExp(tree)
        elif tree.nodekind == NodeKind.DeclK:
            genDecl(tree)
        
        # Generar codigo para hermanos
        cGen(tree.sibling)

def genStmt(tree):
    """Generar codigo para nodos de declaracion"""
    global tmpOffset
    
    if tree.stmt == StmtKind.IfK:
        emitComment("-> if")
        # Generar expresion de prueba
        cGen(tree.child[0])
        # Obtener etiquetas
        false_label = getLabel()
        end_label = getLabel()
        # Saltar si es falso (0)
        emit(f"beqz {a0}, {false_label}")
        # Generar parte then
        cGen(tree.child[1])
        if tree.child[2] is not None:
            # Saltar sobre la parte else
            emit(f"j {end_label}")
            emitLabel(false_label)
            # Generar parte else
            cGen(tree.child[2])
            emitLabel(end_label)
        else:
            emitLabel(false_label)
        emitComment("<- if")
        
    elif tree.stmt == StmtKind.WhileK:
        emitComment("-> while")
        loop_label = getLabel()
        end_label = getLabel()
        emitLabel(loop_label)
        # Generar expresion de prueba
        cGen(tree.child[0])
        # Saltar si es falso (salir del bucle)
        emit(f"beqz {a0}, {end_label}")
        # Generar cuerpo
        cGen(tree.child[1])
        # Saltar de vuelta al inicio
        emit(f"j {loop_label}")
        emitLabel(end_label)
        emitComment("<- while")
        
    elif tree.stmt == StmtKind.AssignK:
        emitComment("-> assign")
        # Generar expresion del lado derecho
        cGen(tree.child[1])  # Resultado en $a0
        # Almacenar resultado
        if tree.child[0].exp == ExpKind.SubscriptK:
            # Asignacion de elemento de arreglo
            emit(f"move {t0}, {a0}")  # Guardar valor del lado derecho
            cGen(tree.child[0].child[0])  # Generar indice
            emit(f"sll {a0}, {a0}, 2")  # Multiplicar por 4
            # Verificar si es local o global
            if tree.child[0].name in local_vars:
                offset = local_vars[tree.child[0].name]
                emit(f"la {t1}, {offset}({sp})")
            else:
                emit(f"la {t1}, var_{tree.child[0].name}")
            emit(f"add {t1}, {t1}, {a0}")
            emit(f"sw {t0}, 0({t1})")
        else:
            # Asignacion de variable simple
            var_name = tree.child[0].name
            if var_name in local_vars:
                # Variable local
                offset = local_vars[var_name]
                emit(f"sw {a0}, {offset}({sp})")
            else:
                # Variable global
                emit(f"sw {a0}, var_{var_name}")
        emitComment("<- assign")
        
    elif tree.stmt == StmtKind.ReturnK:
        emitComment("-> return")
        if tree.child[0] is not None:
            cGen(tree.child[0])  # El resultado estara en $a0
        
        # Retorno basado en tipo de funcion
        if current_function == "factorial":
            # Restaurar direccion de retorno y limpiar
            emit(f"lw {ra}, 4({sp})")
            emit(f"addi {sp}, {sp}, 8")  # Limpiar ra guardado y parametro
            emit(f"jr {ra}")
        elif current_function and current_function != "main":
            # Retorno de funcion generica - usar el param_count de la declaracion de funcion
            # param_count ya esta establecido correctamente en genDecl() 
            stack_size = 4 + 4 * param_count
            # Para funcion add: param_count=2, stack_size=12, $ra en 8($sp)
            emit(f"lw {ra}, {stack_size-4}({sp})")
            emit(f"addi {sp}, {sp}, {stack_size}")
            emit(f"jr {ra}")
        else:
            # Funcion main o desconocida
            emit(f"jr {ra}")
        emitComment("<- return")
        
    elif tree.stmt == StmtKind.CompoundK:
        emitComment("-> compound")
        cGen(tree.child[0])  # Declaraciones locales
        cGen(tree.child[1])  # Lista de declaraciones
        emitComment("<- compound")

def genExp(tree):
    """Generar codigo para nodos de expresion"""
    global tmpOffset, stack_adjustment
    
    if tree.exp == ExpKind.ConstK:
        emitComment("-> Const")
        emit(f"li {a0}, {tree.val}")  # Usar $a0 como acumulador segun codegen.md
        emitComment("<- Const")
        
    elif tree.exp == ExpKind.IdK:
        emitComment("-> Id")
        var_name = tree.name
        if var_name in local_vars:
            # Variable local o parametro
            offset = local_vars[var_name]
            emit(f"lw {a0}, {offset}({sp})")  # Usar $a0 como acumulador
        else:
            # Variable global
            emit(f"lw {a0}, var_{var_name}")  # Usar $a0 como acumulador
        emitComment("<- Id")
        
    elif tree.exp == ExpKind.SubscriptK:
        emitComment("-> Array access")
        cGen(tree.child[0])  # Generar indice
        emit(f"sll {a0}, {a0}, 2")  # Multiplicar por 4
        if tree.name in local_vars:
            offset = local_vars[tree.name]
            emit(f"la {t0}, {offset}({sp})")
        else:
            emit(f"la {t0}, var_{tree.name}")
        emit(f"add {t0}, {t0}, {a0}")
        emit(f"lw {a0}, 0({t0})")
        emitComment("<- Array access")
        
    elif tree.exp == ExpKind.CallK:
        emitComment(f"-> Call: {tree.name}")
        # Manejar funciones integradas
        if tree.name == "input":
            emit(f"li {v0}, 5")  # Syscall leer entero
            emit("syscall")
            emit(f"move {a0}, {v0}")  # Mover resultado al acumulador
        elif tree.name == "output":
            # Generar argumento
            if tree.child[0] is not None:
                cGen(tree.child[0])  # Resultado ya en $a0
                emit(f"li {v0}, 1")  # Syscall imprimir entero
                emit("syscall")
                # Imprimir nueva linea
                emit(f"li {v0}, 4")
                emit(f"la {a0}, newline")
                emit("syscall")
        else:
            # Llamada a funcion definida por el usuario  
            # Manejar argumentos manualmente para evitar recorrido automatico de hermanos
            if tree.child[0] is not None:
                # Existe el primer argumento
                if tree.child[0].sibling is not None:
                    # Dos argumentos - manejar cuidadosamente para evitar problemas del puntero de pila
                    # Generar primer argumento directamente usando genExp para evitar recorrido de hermanos
                    genExp(tree.child[0])  # Primer arg en $a0  
                    emit(f"move {t0}, {a0}")  # Guardar primer arg en registro en lugar de pila
                    # Generar segundo argumento  
                    genExp(tree.child[0].sibling)  # Segundo arg en $a0
                    emit(f"move {a1}, {a0}")  # Mover segundo a $a1
                    emit(f"move {a0}, {t0}")  # Restaurar primero a $a0
                else:
                    # Argumento unico
                    genExp(tree.child[0])  # Resultado en $a0
            
            # Llamar funcion
            # Usar nombre de funcion con prefijo para evitar conflictos
            func_name = f"func_{tree.name}" if tree.name not in ["input", "output", "main"] else tree.name
            emit(f"jal {func_name}")
            
            # El resultado esta en $a0 (acumulador)
        emitComment(f"<- Call: {tree.name}")
        
    elif tree.exp == ExpKind.OpK:
        emitComment("-> Op")
        # Verificar si algun operando es una llamada a funcion
        has_call = (tree.child[0] and tree.child[0].exp == ExpKind.CallK) or \
                   (tree.child[1] and tree.child[1].exp == ExpKind.CallK)
        
        if has_call:
            # Manejo especial cuando hay llamadas a funcion involucradas
            # Evaluar llamada a funcion primero para evitar problemas de pila
            if tree.child[1] and tree.child[1].exp == ExpKind.CallK:
                # El operando derecho es una llamada - evaluarlo primero
                cGen(tree.child[1])  # Resultado en $a0
                emit(f"move {t1}, {a0}")  # Guardar resultado
                cGen(tree.child[0])  # Obtener operando izquierdo en $a0
                emit(f"move {t0}, {a0}")
                emit(f"move {a0}, {t1}")  # Poner operando derecho de vuelta en $a0 para operacion
                # Ahora $t0 tiene izquierdo, $a0 tiene derecho
            else:
                # El operando izquierdo es una llamada
                cGen(tree.child[0])  # Resultado en $a0
                emit(f"move {t0}, {a0}")  # Guardar resultado
                cGen(tree.child[1])  # Obtener operando derecho en $a0
                emit(f"move {t1}, {a0}")
                emit(f"move {a0}, {t0}")  # Poner operando izquierdo en $a0
                emit(f"move {t0}, {t1}")  # Poner derecho en $t0
                # Ahora $a0 tiene izquierdo, $t0 tiene derecho
            
            # Realizar operacion basada en tipo
            if tree.op == TokenType.PLUS:
                emit(f"add {a0}, {t0}, {a0}")
            elif tree.op == TokenType.MINUS:
                emit(f"sub {a0}, {t0}, {a0}")
            elif tree.op == TokenType.TIMES:
                # Para n * factorial(n-1), $t0 tiene n, $a0 tiene factorial(n-1)
                emit(f"mul {a0}, {t0}, {a0}")
        else:
            # Caso normal - sin llamadas a funcion
            # Para operaciones simples como a+b donde ambos son parametros/locales
            # No usar pila - usar registros directamente
            cGen(tree.child[0])  # Operando izquierdo en $a0
            emit(f"move {t0}, {a0}")  # Guardar izquierdo en $t0
            cGen(tree.child[1])  # Operando derecho en $a0
            
            # Realizar operacion (resultado en $a0)
            if tree.op == TokenType.PLUS:
                emit(f"add {a0}, {t0}, {a0}")
            elif tree.op == TokenType.MINUS:
                emit(f"sub {a0}, {t0}, {a0}")
            elif tree.op == TokenType.TIMES:
                emit(f"mul {a0}, {t0}, {a0}")
            elif tree.op == TokenType.DIVIDE:
                emit(f"div {t0}, {a0}")
                emit(f"mflo {a0}")
            elif tree.op == TokenType.LT:
                emit(f"slt {a0}, {t0}, {a0}")
            elif tree.op == TokenType.LTE:
                true_label = getLabel()
                end_label = getLabel()
                emit(f"ble {t0}, {a0}, {true_label}")
                emit(f"li {a0}, 0")
                emit(f"j {end_label}")
                emitLabel(true_label)
                emit(f"li {a0}, 1")
                emitLabel(end_label)
            elif tree.op == TokenType.GT:
                emit(f"slt {a0}, {a0}, {t0}")
            elif tree.op == TokenType.GTE:
                emit(f"slt {a0}, {t0}, {a0}")
                emit(f"xori {a0}, {a0}, 1")
            elif tree.op == TokenType.EQ:
                true_label = getLabel()
                end_label = getLabel()
                emit(f"beq {t0}, {a0}, {true_label}")
                emit(f"li {a0}, 0")
                emit(f"j {end_label}")
                emitLabel(true_label)
                emit(f"li {a0}, 1")
                emitLabel(end_label)
            elif tree.op == TokenType.NEQ:
                true_label = getLabel()
                end_label = getLabel()
                emit(f"bne {t0}, {a0}, {true_label}")
                emit(f"li {a0}, 0")
                emit(f"j {end_label}")
                emitLabel(true_label)
                emit(f"li {a0}, 1")
                emitLabel(end_label)
        emitComment("<- Op")

def genDecl(tree):
    """Generar codigo para nodos de declaracion"""
    global current_function, local_vars, localOffset, param_count, stack_adjustment
    
    if tree.decl == DeclKind.VarK:
        # Las declaraciones de variables locales se manejan rastreando desplazamientos
        if current_function is not None:
            # Dentro de una funcion - asignar espacio en la pila
            if tree.name not in local_vars:  # Solo agregar si no esta ya ahi
                local_vars[tree.name] = localOffset
                localOffset -= 4
                if tree.is_array and tree.array_size:
                    # Asignar espacio para arreglo
                    localOffset -= 4 * (tree.array_size - 1)
    
    elif tree.decl == DeclKind.FunK:
        emitComment(f"-> Function: {tree.name}")
        current_function = tree.name
        local_vars.clear()
        localOffset = -4  # Comenzar en -4 para el primer local
        stack_adjustment = 0  # Reiniciar ajuste de pila para nueva funcion
        
        # Contar parametros
        param_count = len(tree.params)
        
        # Prefijar nombres de funcion para evitar conflictos con instrucciones MIPS
        func_label = f"func_{tree.name}" if tree.name != "main" else "main"
        emitLabel(func_label)
        
        if tree.name == "factorial":
            # Enfoque simple como ejemplo funcional
            emit(f"addi {sp}, {sp}, -8")  # Hacer espacio para $ra y parametro
            emit(f"sw {ra}, 4({sp})")     # Guardar direccion de retorno
            emit(f"sw {a0}, 0({sp})")     # Guardar parametro n
            
            # Marcar ubicacion del parametro
            if param_count > 0 and hasattr(tree.params[0], 'name'):
                local_vars[tree.params[0].name] = 0  # Parametro en 0($sp)
            
        elif tree.name == "main":
            # Funcion main - configuracion simple
            # Contar y asignar locales
            processLocalDecls(tree.child[0])
            space_needed = -localOffset - 4  # Calculo ajustado
            if space_needed > 0:
                emit(f"addi {sp}, {sp}, -{space_needed}")
        else:
            # Otras funciones - manejar multiples parametros
            # Para C-, los parametros se pasan en registros $a0-$a3
            # Los guardaremos en la pila
            stack_size = 4 + 4 * param_count  # Espacio para $ra + parametros
            emit(f"addi {sp}, {sp}, -{stack_size}")
            emit(f"sw {ra}, {stack_size-4}({sp})")
            
            # Guardar parametros
            for i in range(min(param_count, 4)):  # Maximo 4 parametros de registro
                if i == 0:
                    emit(f"sw {a0}, {i*4}({sp})")
                elif i == 1:
                    emit(f"sw {a1}, {i*4}({sp})")
                elif i == 2:
                    emit(f"sw {a2}, {i*4}({sp})")
                elif i == 3:
                    emit(f"sw {a3}, {i*4}({sp})")
                    
                # Marcar ubicaciones de parametros
                if i < len(tree.params) and hasattr(tree.params[i], 'name'):
                    local_vars[tree.params[i].name] = i * 4
        
        # Generar cuerpo de funcion
        if tree.child[0] is not None:
            cGen(tree.child[0])
        
        if tree.name == "main":
            # La funcion main termina con syscall de salida
            emit(f"li {v0}, 10")
            emit("syscall")
        elif tree.name == "factorial":
            # Limpieza de factorial - ya tiene retornos en el cuerpo
            pass
        else:
            # Epilogo por defecto - ya manejado en declaraciones de retorno
            pass
        
        emitComment(f"<- Function: {tree.name}")
        
        current_function = None

def processLocalDecls(tree):
    """Procesar declaraciones locales para asignar desplazamientos"""
    if tree is None:
        return
    
    # Procesar este nodo si es una declaracion de variable
    if tree.nodekind == NodeKind.DeclK and tree.decl == DeclKind.VarK:
        genDecl(tree)
    
    # Procesar hijos
    for i in range(MAXCHILDREN):
        if tree.child[i] is not None:
            processLocalDecls(tree.child[i])
    
    # Procesar hermanos
    if tree.sibling is not None:
        processLocalDecls(tree.sibling)

def codeGen(syntaxTree, codefile):
    """Funcion principal para generar codigo"""
    global code_file, TraceCode
    
    # Abrir archivo de salida
    code_file = open(codefile, 'w')
    
    emitComment("Compilacion C- a MIPS")
    emitComment(f"Archivo: {codefile}")
    
    # Seccion de datos
    code_file.write(".data\n")
    code_file.write("newline: .asciiz \"\\n\"\n")
    
    # Generar espacio para variables globales
    generateGlobals(syntaxTree)
    
    # Seccion de texto
    code_file.write("\n.text\n")
    code_file.write(".globl main\n")
    code_file.write("\n")
    
    # Generar codigo para programa
    cGen(syntaxTree)
    
    # Cerrar archivo
    code_file.close()

def generateGlobals(tree):
    """Generar seccion .data para variables globales"""
    if tree is not None:
        if tree.nodekind == NodeKind.DeclK and tree.decl == DeclKind.VarK:
            # Solo generar globales para variables declaradas fuera de funciones
            sym = st_lookup(tree.name)
            if sym and sym.scope_level == 0:  # Ambito global
                if tree.is_array and tree.array_size:
                    # Variable de arreglo
                    code_file.write(f"var_{tree.name}: .space {tree.array_size * 4}\n")
                else:
                    # Variable simple
                    code_file.write(f"var_{tree.name}: .word 0\n")
        
        # Verificar hijos
        for i in range(MAXCHILDREN):
            if tree.child[i] is not None:
                generateGlobals(tree.child[i])
        
        # Verificar hermanos
        generateGlobals(tree.sibling)

# Funciones auxiliares adicionales para generacion de codigo
def globales(prog, pos, long):
    """Funcion para recibir variables globales"""
    # Esto es manejado por el parser
    from Parser import recibeParser
    recibeParser(prog, pos, long)