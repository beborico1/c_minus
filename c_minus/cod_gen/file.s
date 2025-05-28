# C- Compilation to MIPS
# File: file.s
.data
newline: .asciiz "\n"
var_x: .word 0

.text
.globl main

# -> Function: add
func_add:
    addi $sp, $sp, -12
    sw $ra, 8($sp)
    sw $a0, 0($sp)
    sw $a1, 4($sp)
# -> compound
# -> return
# -> Op
# -> Id
    lw $a0, 0($sp)
# <- Id
    move $t0, $a0
# -> Id
    lw $a0, 4($sp)
# <- Id
    add $a0, $t0, $a0
# <- Op
    lw $ra, 8($sp)
    addi $sp, $sp, 12
    jr $ra
# <- return
# <- compound
# <- Function: add
# -> Function: main
main:
    addi $sp, $sp, -4
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
# -> Call: add
# -> Id
    lw $a0, var_x
# <- Id
    move $t0, $a0
# -> Id
    lw $a0, -4($sp)
# <- Id
    move $a1, $a0
    move $a0, $t0
    jal func_add
# <- Call: add
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
