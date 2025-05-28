# C- Compilation to MIPS
# File: test_programs/test13_mixed_vars.s
.data
newline: .asciiz "\n"
var_globalVar: .word 0

.text
.globl main

# -> Function: process
func_process:
    addi $sp, $sp, -8
    sw $ra, 4($sp)
    sw $a0, 0($sp)
# -> compound
# -> assign
# -> Op
# -> Id
    lw $a0, 0($sp)
# <- Id
    move $t0, $a0
# -> Id
    lw $a0, var_globalVar
# <- Id
    add $a0, $t0, $a0
# <- Op
    sw $a0, -4($sp)
# <- assign
# -> return
# -> Id
    lw $a0, -4($sp)
# <- Id
    lw $ra, 4($sp)
    addi $sp, $sp, 8
    jr $ra
# <- return
# <- compound
# <- Function: process
# -> Function: main
main:
# -> compound
# -> assign
# -> Const
    li $a0, 10
# <- Const
    sw $a0, var_globalVar
# <- assign
# -> Call: output
# -> Call: process
# -> Const
    li $a0, 25
# <- Const
    jal func_process
# <- Call: process
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
