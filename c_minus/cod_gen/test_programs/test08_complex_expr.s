# C- Compilation to MIPS
# File: test_programs/test08_complex_expr.s
.data
newline: .asciiz "\n"

.text
.globl main

# -> Function: main
main:
    addi $sp, $sp, -16
# -> compound
# -> assign
# -> Const
    li $a0, 5
# <- Const
    sw $a0, -4($sp)
# <- assign
# -> assign
# -> Const
    li $a0, 3
# <- Const
    sw $a0, -8($sp)
# <- assign
# -> assign
# -> Op
# -> Id
    lw $a0, -4($sp)
# <- Id
    move $t0, $a0
# -> Id
    lw $a0, -8($sp)
# <- Id
    mul $a0, $t0, $a0
# <- Op
    sw $a0, -12($sp)
# <- assign
# -> assign
# -> Op
# -> Id
    lw $a0, -12($sp)
# <- Id
    move $t0, $a0
# -> Const
    li $a0, 2
# <- Const
    add $a0, $t0, $a0
# <- Op
    sw $a0, -16($sp)
# <- assign
# -> assign
# -> Op
# -> Id
    lw $a0, -16($sp)
# <- Id
    move $t0, $a0
# -> Const
    li $a0, 1
# <- Const
    sub $a0, $t0, $a0
# <- Op
    sw $a0, -16($sp)
# <- assign
# -> Call: output
# -> Id
    lw $a0, -16($sp)
# <- Id
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
