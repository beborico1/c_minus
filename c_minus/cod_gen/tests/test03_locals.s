# C- Compilation to MIPS
# File: test_programs/test03_locals.s
.data
newline: .asciiz "\n"

.text
.globl main

# -> Function: main
main:
    addi $sp, $sp, -8
# -> compound
# -> assign
# -> Const
    li $a0, 7
# <- Const
    sw $a0, -4($sp)
# <- assign
# -> assign
# -> Const
    li $a0, 8
# <- Const
    sw $a0, -8($sp)
# <- assign
# -> Call: output
# -> Op
# -> Id
    lw $a0, -4($sp)
# <- Id
    move $t0, $a0
# -> Id
    lw $a0, -8($sp)
# <- Id
    add $a0, $t0, $a0
# <- Op
    li $v0, 1
    syscall
    li $v0, 4
    la $a0, newline
    syscall
# <- Call: output
# <- compound
    li $v0, 10
    syscall
# <- Function: main
