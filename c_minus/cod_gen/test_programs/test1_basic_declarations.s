# C- Compilation to MIPS
# File: test_programs/test1_basic_declarations.s
.data
newline: .asciiz "\n"
var_x: .word 0
var_y: .space 40

.text
.globl main

# -> Function: main
main:
    addi $sp, $sp, -24
# -> compound
# -> assign
# -> Const
    li $a0, 10
# <- Const
    sw $a0, var_x
# <- assign
# -> assign
# -> Const
    li $a0, 20
# <- Const
    sw $a0, -4($sp)
# <- assign
# -> assign
# -> Const
    li $a0, 30
# <- Const
    move $t0, $a0
# -> Const
    li $a0, 0
# <- Const
    sll $a0, $a0, 2
    la $t1, var_y
    add $t1, $t1, $a0
    sw $t0, 0($t1)
# <- assign
# -> assign
# -> Const
    li $a0, 40
# <- Const
    move $t0, $a0
# -> Const
    li $a0, 2
# <- Const
    sll $a0, $a0, 2
    la $t1, -8($sp)
    add $t1, $t1, $a0
    sw $t0, 0($t1)
# <- assign
# -> Call: output
# -> Array access
# -> Const
    li $a0, 0
# <- Const
    sll $a0, $a0, 2
    la $t0, var_y
    add $t0, $t0, $a0
    lw $a0, 0($t0)
# <- Array access
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
