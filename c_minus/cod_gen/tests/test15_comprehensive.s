# C- Compilation to MIPS
# File: test_programs/test15_comprehensive.s
.data
newline: .asciiz "\n"
var_globalResult: .word 0

.text
.globl main

# -> Function: calculateComplex
func_calculateComplex:
    addi $sp, $sp, -12
    sw $ra, 8($sp)
    sw $a0, 0($sp)
    sw $a1, 4($sp)
# -> compound
# -> assign
# -> Op
# -> Id
    lw $a0, 0($sp)
# <- Id
    move $t0, $a0
# -> Const
    li $a0, 2
# <- Const
    mul $a0, $t0, $a0
# <- Op
    sw $a0, -4($sp)
# <- assign
# -> return
# -> Op
# -> Op
# -> Id
    lw $a0, -4($sp)
# <- Id
    move $t0, $a0
# -> Id
    lw $a0, 4($sp)
# <- Id
    add $a0, $t0, $a0
# <- Op
    move $t0, $a0
# -> Const
    li $a0, 1
# <- Const
    sub $a0, $t0, $a0
# <- Op
    lw $ra, 8($sp)
    addi $sp, $sp, 12
    jr $ra
# <- return
# <- compound
# <- Function: calculateComplex
# -> Function: simpleAdd
func_simpleAdd:
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
# <- Function: simpleAdd
# -> Function: main
main:
    addi $sp, $sp, -4
# -> compound
# -> assign
# -> Const
    li $a0, 5
# <- Const
    sw $a0, var_globalResult
# <- assign
# -> assign
# -> Const
    li $a0, 7
# <- Const
    sw $a0, -4($sp)
# <- assign
# -> assign
# -> Call: simpleAdd
# -> Id
    lw $a0, var_globalResult
# <- Id
    move $t0, $a0
# -> Id
    lw $a0, -4($sp)
# <- Id
    move $a1, $a0
    move $a0, $t0
    jal func_simpleAdd
# <- Call: simpleAdd
    sw $a0, var_globalResult
# <- assign
# -> assign
# -> Call: calculateComplex
# -> Const
    li $a0, 3
# <- Const
    move $t0, $a0
# -> Const
    li $a0, 4
# <- Const
    move $a1, $a0
    move $a0, $t0
    jal func_calculateComplex
# <- Call: calculateComplex
    sw $a0, -4($sp)
# <- assign
# -> Call: output
# -> Id
    lw $a0, var_globalResult
# <- Id
    li $v0, 1
    syscall
    li $v0, 4
    la $a0, newline
    syscall
# <- Call: output
# -> Call: output
# -> Id
    lw $a0, -4($sp)
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
