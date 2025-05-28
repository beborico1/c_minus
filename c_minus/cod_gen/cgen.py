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

# Output file
code_file = None

# Trace code generation
TraceCode = True

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
        # Branch if false
        emit(f"beq {v0}, {zero}, L{emitLoc+2}")
        # Generate then part
        cGen(tree.child[1])
        if tree.child[2] is not None:
            # Jump over else part
            emit(f"j L{emitLoc+2}")
            emitLabel(f"L{emitLoc-1}")
            # Generate else part
            cGen(tree.child[2])
        emitLabel(f"L{emitLoc}")
        emitComment("<- if")
        
    elif tree.stmt == StmtKind.WhileK:
        emitComment("-> while")
        loop_start = emitLoc
        emitLabel(f"L{loop_start}")
        # Generate test expression
        cGen(tree.child[0])
        # Branch if false (exit loop)
        emit(f"beq {v0}, {zero}, L{emitLoc+2}")
        # Generate body
        cGen(tree.child[1])
        # Jump back to start
        emit(f"j L{loop_start}")
        emitLabel(f"L{emitLoc-1}")
        emitComment("<- while")
        
    elif tree.stmt == StmtKind.AssignK:
        emitComment("-> assign")
        # Generate RHS expression
        cGen(tree.child[1])
        # Store result
        if tree.child[0].exp == ExpKind.SubscriptK:  # Changed from ArrayK to SubscriptK
            # Array element assignment
            emit(f"move {t0}, {v0}")  # Save RHS value
            cGen(tree.child[0].child[0])  # Generate index
            emit(f"sll {v0}, {v0}, 2")  # Multiply by 4
            loc = st_lookup(tree.child[0].name)
            if loc:  # Changed from loc >= 0
                emit(f"la {t1}, var_{tree.child[0].name}")
                emit(f"add {t1}, {t1}, {v0}")
                emit(f"sw {t0}, 0({t1})")
        else:
            # Simple variable assignment
            loc = st_lookup(tree.child[0].name)
            if loc:  # Changed from loc >= 0
                emit(f"sw {v0}, var_{tree.child[0].name}")
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
    global tmpOffset
    
    if tree.exp == ExpKind.ConstK:
        emitComment("-> Const")
        emit(f"li {v0}, {tree.val}")
        emitComment("<- Const")
        
    elif tree.exp == ExpKind.IdK:
        emitComment("-> Id")
        loc = st_lookup(tree.name)
        if loc:  # Changed from loc >= 0
            emit(f"lw {v0}, var_{tree.name}")
        emitComment("<- Id")
        
    elif tree.exp == ExpKind.SubscriptK:  # Changed from ArrayK to SubscriptK
        emitComment("-> Array access")
        cGen(tree.child[0])  # Generate index
        emit(f"sll {v0}, {v0}, 2")  # Multiply by 4
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
            # Save registers
            emit(f"addi {sp}, {sp}, -4")
            emit(f"sw {ra}, 0({sp})")
            
            # Generate arguments (simplified - only handles first few args)
            arg = tree.child[0]
            arg_count = 0
            while arg is not None and arg_count < 4:
                cGen(arg)
                if arg_count == 0:
                    emit(f"move {a0}, {v0}")
                elif arg_count == 1:
                    emit(f"move {a1}, {v0}")
                elif arg_count == 2:
                    emit(f"move {a2}, {v0}")
                elif arg_count == 3:
                    emit(f"move {a3}, {v0}")
                arg = arg.sibling
                arg_count += 1
            
            # Call function
            emit(f"jal {tree.name}")
            
            # Restore registers
            emit(f"lw {ra}, 0({sp})")
            emit(f"addi {sp}, {sp}, 4")
        emitComment(f"<- Call: {tree.name}")
        
    elif tree.exp == ExpKind.OpK:
        emitComment("-> Op")
        # Generate left operand
        cGen(tree.child[0])
        emit(f"move {t0}, {v0}")
        
        # Generate right operand
        cGen(tree.child[1])
        emit(f"move {t1}, {v0}")
        
        # Perform operation
        if tree.op == TokenType.PLUS:
            emit(f"add {v0}, {t0}, {t1}")
        elif tree.op == TokenType.MINUS:
            emit(f"sub {v0}, {t0}, {t1}")
        elif tree.op == TokenType.TIMES:
            emit(f"mul {v0}, {t0}, {t1}")
        elif tree.op == TokenType.DIVIDE:  # Changed from OVER
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
            emit(f"seq {v0}, {t0}, {t1}")
        elif tree.op == TokenType.NEQ:
            emit(f"sne {v0}, {t0}, {t1}")
        emitComment("<- Op")

def genDecl(tree):
    """Generate code for declaration nodes"""
    if tree.decl == DeclKind.VarK:
        # Variable declarations are handled in data section
        pass
    elif tree.decl == DeclKind.FunK:
        emitComment(f"-> Function: {tree.name}")
        emitLabel(tree.name)
        
        # Function prologue
        emit(f"addi {sp}, {sp}, -8")
        emit(f"sw {fp}, 4({sp})")
        emit(f"sw {ra}, 0({sp})")
        emit(f"move {fp}, {sp}")
        
        # Generate function body
        if tree.child[0] is not None:
            cGen(tree.child[0])
        
        # Function epilogue
        emit(f"move {sp}, {fp}")
        emit(f"lw {ra}, 0({sp})")
        emit(f"lw {fp}, 4({sp})")
        emit(f"addi {sp}, {sp}, 8")
        emit(f"jr {ra}")
        emitComment(f"<- Function: {tree.name}")

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
    
    # Standard startup: jump to main
    emitLabel("__start")
    emit(f"jal main")
    emit(f"li {v0}, 10")  # Exit syscall
    emit("syscall")
    
    # Generate code for program
    cGen(syntaxTree)
    
    # Close file
    code_file.close()

def generateGlobals(tree):
    """Generate .data section for global variables"""
    if tree is not None:
        if tree.nodekind == NodeKind.DeclK and tree.decl == DeclKind.VarK:
            if tree.array_size is not None:
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