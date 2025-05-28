# cgen.py
from globalTypes import *
from symtab import *
import sys

# MIPS registers
zero = "$zero"  # Always 0
v0 = "$v0"      # Return values
v1 = "$v1"
a0 = "$a0"      # Arguments
a1 = "$a1"
a2 = "$a2"
a3 = "$a3"
t0 = "$t0"      # Temporaries
t1 = "$t1"
t2 = "$t2"
t3 = "$t3"
t4 = "$t4"
t5 = "$t5"
t6 = "$t6"
t7 = "$t7"
t8 = "$t8"
t9 = "$t9"
s0 = "$s0"      # Saved
s1 = "$s1"
s2 = "$s2"
s3 = "$s3"
s4 = "$s4"
s5 = "$s5"
s6 = "$s6"
s7 = "$s7"
sp = "$sp"      # Stack pointer
fp = "$fp"      # Frame pointer
ra = "$ra"      # Return address
gp = "$gp"      # Global pointer

# Code generation state
emitLoc = 0
highEmitLoc = 0
tmpOffset = 0
mainLoc = 0
globalOffset = 0
localOffset = 0
paramOffset = 0
labelCount = 0

# Output file
code_file = None

# Trace code generation
TraceCode = True

# Track current function and local variables
current_function = None
local_vars = {}  # Maps variable names to their offsets

def emitComment(comment):
    """Emit a comment in the assembly code"""
    if TraceCode and code_file:
        code_file.write(f"# {comment}\n")

def emit(instruction):
    """Emit a MIPS instruction"""
    global emitLoc, highEmitLoc
    if code_file:
        code_file.write(f"    {instruction}\n")
    emitLoc += 1
    if highEmitLoc < emitLoc:
        highEmitLoc = emitLoc

def emitLabel(label):
    """Emit a label"""
    if code_file:
        code_file.write(f"{label}:\n")

def getLabel():
    """Generate a unique label"""
    global labelCount
    labelCount += 1
    return f"L{labelCount}"

def emitSkip(howMany):
    """Skip locations for later backpatch"""
    global emitLoc, highEmitLoc
    i = emitLoc
    emitLoc += howMany
    if highEmitLoc < emitLoc:
        highEmitLoc = emitLoc
    return i

def emitBackup(loc):
    """Back up to previously skipped location"""
    global emitLoc
    emitLoc = loc

def emitRestore():
    """Restore to highest emitted location"""
    global emitLoc, highEmitLoc
    emitLoc = highEmitLoc

def cGen(tree):
    """Recursively generate code by tree traversal"""
    if tree is not None:
        if tree.nodekind == NodeKind.StmtK:
            genStmt(tree)
        elif tree.nodekind == NodeKind.ExpK:
            genExp(tree)
        elif tree.nodekind == NodeKind.DeclK:
            genDecl(tree)
        
        # Generate code for siblings
        cGen(tree.sibling)

def genStmt(tree):
    """Generate code for statement nodes"""
    global tmpOffset
    
    if tree.stmt == StmtKind.IfK:
        emitComment("-> if")
        # Generate test expression
        cGen(tree.child[0])
        # Get labels
        false_label = getLabel()
        end_label = getLabel()
        # Branch if false
        emit(f"beq {v0}, {zero}, {false_label}")
        # Generate then part
        cGen(tree.child[1])
        if tree.child[2] is not None:
            # Jump over else part
            emit(f"j {end_label}")
            emitLabel(false_label)
            # Generate else part
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
        # Generate test expression
        cGen(tree.child[0])
        # Branch if false (exit loop)
        emit(f"beq {v0}, {zero}, {end_label}")
        # Generate body
        cGen(tree.child[1])
        # Jump back to start
        emit(f"j {loop_label}")
        emitLabel(end_label)
        emitComment("<- while")
        
    elif tree.stmt == StmtKind.AssignK:
        emitComment("-> assign")
        # Generate RHS expression
        cGen(tree.child[1])
        # Store result
        if tree.child[0].exp == ExpKind.SubscriptK:
            # Array element assignment
            emit(f"move {t0}, {v0}")  # Save RHS value
            cGen(tree.child[0].child[0])  # Generate index
            emit(f"sll {v0}, {v0}, 2")  # Multiply by 4
            # Check if local or global
            if tree.child[0].name in local_vars:
                offset = local_vars[tree.child[0].name]
                emit(f"addi {t1}, {fp}, {offset}")
            else:
                emit(f"la {t1}, var_{tree.child[0].name}")
            emit(f"add {t1}, {t1}, {v0}")
            emit(f"sw {t0}, 0({t1})")
        else:
            # Simple variable assignment
            var_name = tree.child[0].name
            if var_name in local_vars:
                # Local variable
                offset = local_vars[var_name]
                emit(f"sw {v0}, {offset}({fp})")
            else:
                # Global variable
                emit(f"sw {v0}, var_{var_name}")
        emitComment("<- assign")
        
    elif tree.stmt == StmtKind.ReturnK:
        emitComment("-> return")
        if tree.child[0] is not None:
            cGen(tree.child[0])
        emit(f"jr {ra}")
        emitComment("<- return")
        
    elif tree.stmt == StmtKind.CompoundK:
        emitComment("-> compound")
        cGen(tree.child[0])  # Local declarations
        cGen(tree.child[1])  # Statement list
        emitComment("<- compound")

def genExp(tree):
    """Generate code for expression nodes"""
    global tmpOffset, labelCount
    
    if tree.exp == ExpKind.ConstK:
        emitComment("-> Const")
        emit(f"li {v0}, {tree.val}")
        emitComment("<- Const")
        
    elif tree.exp == ExpKind.IdK:
        emitComment("-> Id")
        var_name = tree.name
        if var_name in local_vars:
            # Local variable or parameter
            offset = local_vars[var_name]
            emit(f"lw {v0}, {offset}({fp})")
        else:
            # Global variable
            emit(f"lw {v0}, var_{var_name}")
        emitComment("<- Id")
        
    elif tree.exp == ExpKind.SubscriptK:
        emitComment("-> Array access")
        cGen(tree.child[0])  # Generate index
        emit(f"sll {v0}, {v0}, 2")  # Multiply by 4
        if tree.name in local_vars:
            offset = local_vars[tree.name]
            emit(f"addi {t0}, {fp}, {offset}")
        else:
            emit(f"la {t0}, var_{tree.name}")
        emit(f"add {t0}, {t0}, {v0}")
        emit(f"lw {v0}, 0({t0})")
        emitComment("<- Array access")
        
    elif tree.exp == ExpKind.CallK:
        emitComment(f"-> Call: {tree.name}")
        # Handle built-in functions
        if tree.name == "input":
            emit(f"li {v0}, 5")  # Read integer syscall
            emit("syscall")
        elif tree.name == "output":
            # Generate argument
            if tree.child[0] is not None:
                cGen(tree.child[0])
                emit(f"move {a0}, {v0}")
                emit(f"li {v0}, 1")  # Print integer syscall
                emit("syscall")
                # Print newline
                emit(f"li {v0}, 4")
                emit(f"la {a0}, newline")
                emit("syscall")
        else:
            # User-defined function call
            # Push arguments on stack in reverse order
            arg_list = []
            arg = tree.child[0]
            while arg is not None:
                arg_list.append(arg)
                arg = arg.sibling
            
            # Generate arguments in reverse order
            for i in range(len(arg_list) - 1, -1, -1):
                cGen(arg_list[i])
                emit(f"addi {sp}, {sp}, -4")
                emit(f"sw {v0}, 0({sp})")
            
            # Call function
            emit(f"jal {tree.name}")
            
            # Pop arguments
            if len(arg_list) > 0:
                emit(f"addi {sp}, {sp}, {4 * len(arg_list)}")
        emitComment(f"<- Call: {tree.name}")
        
    elif tree.exp == ExpKind.OpK:
        emitComment("-> Op")
        # Generate left operand
        cGen(tree.child[0])
        # Push left operand on stack
        emit(f"addi {sp}, {sp}, -4")
        emit(f"sw {v0}, 0({sp})")
        
        # Generate right operand
        cGen(tree.child[1])
        emit(f"move {t1}, {v0}")
        
        # Pop left operand from stack
        emit(f"lw {t0}, 0({sp})")
        emit(f"addi {sp}, {sp}, 4")
        
        # Perform operation
        if tree.op == TokenType.PLUS:
            emit(f"add {v0}, {t0}, {t1}")
        elif tree.op == TokenType.MINUS:
            emit(f"sub {v0}, {t0}, {t1}")
        elif tree.op == TokenType.TIMES:
            emit(f"mult {t0}, {t1}")
            emit(f"mflo {v0}")
        elif tree.op == TokenType.DIVIDE:
            emit(f"div {t0}, {t1}")
            emit(f"mflo {v0}")
        elif tree.op == TokenType.LT:
            emit(f"slt {v0}, {t0}, {t1}")
        elif tree.op == TokenType.LTE:
            emit(f"slt {v0}, {t1}, {t0}")
            emit(f"xori {v0}, {v0}, 1")
        elif tree.op == TokenType.GT:
            emit(f"slt {v0}, {t1}, {t0}")
        elif tree.op == TokenType.GTE:
            emit(f"slt {v0}, {t0}, {t1}")
            emit(f"xori {v0}, {v0}, 1")
        elif tree.op == TokenType.EQ:
            # Implement seq using basic instructions
            emit(f"beq {t0}, {t1}, L{labelCount+1}")
            emit(f"li {v0}, 0")
            emit(f"j L{labelCount+2}")
            emitLabel(f"L{labelCount+1}")
            emit(f"li {v0}, 1")
            emitLabel(f"L{labelCount+2}")
            labelCount += 2
        elif tree.op == TokenType.NEQ:
            # Implement sne using basic instructions
            emit(f"bne {t0}, {t1}, L{labelCount+1}")
            emit(f"li {v0}, 0")
            emit(f"j L{labelCount+2}")
            emitLabel(f"L{labelCount+1}")
            emit(f"li {v0}, 1")
            emitLabel(f"L{labelCount+2}")
            labelCount += 2
        emitComment("<- Op")

def genDecl(tree):
    """Generate code for declaration nodes"""
    global current_function, local_vars, localOffset, paramOffset
    
    if tree.decl == DeclKind.VarK:
        # Local variable declarations are handled by tracking offsets
        if current_function is not None:
            # Inside a function - allocate space on stack
            localOffset -= 4
            local_vars[tree.name] = localOffset
            if tree.is_array and tree.array_size:
                # Allocate space for array
                localOffset -= 4 * (tree.array_size - 1)
    
    elif tree.decl == DeclKind.FunK:
        emitComment(f"-> Function: {tree.name}")
        current_function = tree.name
        local_vars.clear()
        localOffset = -8  # Start after saved fp and ra
        paramOffset = 8   # Parameters start at fp+8 (skip saved fp and return address)
        
        # Process parameters to record their offsets
        # Parameters are pushed in reverse order, so the first parameter is at fp+8
        for i, param in enumerate(tree.params):
            if hasattr(param, 'name') and param.name:
                # Calculate offset for each parameter
                # First param at fp+8, second at fp+12, etc.
                local_vars[param.name] = paramOffset + i * 4
        
        # First pass: count local variables to allocate space
        saved_localOffset = localOffset
        countLocalVars(tree.child[0])
        space_needed = -8 - localOffset
        localOffset = saved_localOffset  # Reset for actual code generation
        
        emitLabel(tree.name)
        
        # Function prologue
        emit(f"addi {sp}, {sp}, -8")
        emit(f"sw {fp}, 4({sp})")
        emit(f"sw {ra}, 0({sp})")
        emit(f"move {fp}, {sp}")
        
        # Allocate space for local variables
        if space_needed > 0:
            emit(f"addi {sp}, {sp}, -{space_needed}")
        
        # Generate function body
        if tree.child[0] is not None:
            cGen(tree.child[0])
        
        # If this is main, add exit syscall
        if tree.name == "main":
            emit(f"li {v0}, 10")  # Exit syscall
            emit("syscall")
        
        # Function epilogue
        emit(f"move {sp}, {fp}")
        emit(f"lw {ra}, 0({sp})")
        emit(f"lw {fp}, 4({sp})")
        emit(f"addi {sp}, {sp}, 8")
        emit(f"jr {ra}")
        emitComment(f"<- Function: {tree.name}")
        
        current_function = None

def countLocalVars(tree):
    """Count local variables in a compound statement"""
    global localOffset
    
    if tree is None:
        return
    
    if tree.nodekind == NodeKind.DeclK and tree.decl == DeclKind.VarK:
        localOffset -= 4
        if tree.is_array and tree.array_size:
            localOffset -= 4 * (tree.array_size - 1)
    
    # Process children
    for i in range(MAXCHILDREN):
        if tree.child[i] is not None:
            countLocalVars(tree.child[i])
    
    # Process siblings
    if tree.sibling is not None:
        countLocalVars(tree.sibling)

def codeGen(syntaxTree, codefile):
    """Main function to generate code"""
    global code_file, TraceCode
    
    # Open output file
    code_file = open(codefile, 'w')
    
    emitComment("C- Compilation to MIPS")
    emitComment(f"File: {codefile}")
    
    # Data section
    code_file.write(".data\n")
    code_file.write("newline: .asciiz \"\\n\"\n")
    
    # Generate space for global variables
    generateGlobals(syntaxTree)
    
    # Text section
    code_file.write("\n.text\n")
    code_file.write(".globl main\n")
    
    # Generate code for program
    cGen(syntaxTree)
    
    # Close file
    code_file.close()

def generateGlobals(tree):
    """Generate .data section for global variables"""
    if tree is not None:
        if tree.nodekind == NodeKind.DeclK and tree.decl == DeclKind.VarK:
            # Only generate globals for variables declared outside functions
            sym = st_lookup(tree.name)
            if sym and sym.scope_level == 0:  # Global scope
                if tree.is_array and tree.array_size:
                    # Array variable
                    code_file.write(f"var_{tree.name}: .space {tree.array_size * 4}\n")
                else:
                    # Simple variable
                    code_file.write(f"var_{tree.name}: .word 0\n")
        
        # Check children
        for i in range(MAXCHILDREN):
            if tree.child[i] is not None:
                generateGlobals(tree.child[i])
        
        # Check siblings
        generateGlobals(tree.sibling)

# Additional helper functions for code generation
def globales(prog, pos, long):
    """Function to receive global variables"""
    # This is handled by the parser
    from Parser import recibeParser
    recibeParser(prog, pos, long)