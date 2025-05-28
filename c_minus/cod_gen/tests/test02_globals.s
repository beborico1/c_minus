# C- Compilation to MIPS
# File: test_programs/test02_globals.s
.data
newline: .asciiz "\n"
var_x: .word 0
var_y: .word 0

.text
.globl main

# -> Function: main
main:
# -> compound
# -> assign
# -> Const
    li $a0, 15
# <- Const
    sw $a0, var_x
# <- assign
# -> assign
# -> Op
# -> Id
    lw $a0, var_x
# <- Id
    move $t0, $a0
# -> Const
    li $a0, 10
# <- Const
    add $a0, $t0, $a0
# <- Op
    sw $a0, var_y
# <- assign
# -> assign
# -> Op
# -> Id
    lw $a0, var_y
# <- Id
    move $t0, $a0
# -> Const
    li $a0, 5
# <- Const
    sub $a0, $t0, $a0
# <- Op
    sw $a0, var_x
# <- assign
# -> Call: output
# -> Id
    lw $a0, var_x
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
