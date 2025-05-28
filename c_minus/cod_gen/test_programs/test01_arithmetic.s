# C- Compilation to MIPS
# File: test_programs/test01_arithmetic.s
.data
newline: .asciiz "\n"
var_result: .word 0

.text
.globl main

# -> Function: calculate
func_calculate:
    addi $sp, $sp, -12
    sw $ra, 8($sp)
    sw $a0, 0($sp)
    sw $a1, 4($sp)
# -> compound
# -> return
# -> Op
# -> Op
# -> Id
    lw $a0, 0($sp)
# <- Id
    move $t0, $a0
# -> Op
# -> Id
    lw $a0, 4($sp)
# <- Id
    move $t0, $a0
# -> Const
    li $a0, 2
# <- Const
    mul $a0, $t0, $a0
# <- Op
    add $a0, $t0, $a0
# <- Op
    move $t0, $a0
# -> Const
    li $a0, 5
# <- Const
    sub $a0, $t0, $a0
# <- Op
    lw $ra, 8($sp)
    addi $sp, $sp, 12
    jr $ra
# <- return
# <- compound
# <- Function: calculate
# -> Function: main
main:
# -> compound
# -> assign
# -> Call: calculate
# -> Const
    li $a0, 10
# <- Const
    move $t0, $a0
# -> Const
    li $a0, 3
# <- Const
    move $a1, $a0
    move $a0, $t0
    jal func_calculate
# <- Call: calculate
    sw $a0, var_result
# <- assign
# -> Call: output
# -> Id
    lw $a0, var_result
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
