# C- Compilation to MIPS
# File: prueba.s
.data
newline: .asciiz "\n"
var_x: .word 0
var_result: .word 0

.text
.globl main
__start:
    jal main
    li $v0, 10
    syscall
# -> Function: factorial
factorial:
    addi $sp, $sp, -8
    sw $fp, 4($sp)
    sw $ra, 0($sp)
    move $fp, $sp
# -> compound
# -> if
# -> Op
# -> Id
# <- Id
    move $t0, $v0
# -> Const
    li $v0, 1
# <- Const
    move $t1, $v0
    slt $v0, $t1, $t0
    xori $v0, $v0, 1
# <- Op
    beq $v0, $zero, L14
# -> compound
# -> return
# -> Const
    li $v0, 1
# <- Const
    jr $ra
# <- return
# <- compound
    j L17
L15:
# -> compound
# -> return
# -> Op
# -> Id
# <- Id
    move $t0, $v0
# -> Call: factorial
    addi $sp, $sp, -4
    sw $ra, 0($sp)
# -> Op
# -> Id
# <- Id
    move $t0, $v0
# -> Const
    li $v0, 1
# <- Const
    move $t1, $v0
    sub $v0, $t0, $t1
# <- Op
    move $a0, $v0
    jal factorial
    lw $ra, 0($sp)
    addi $sp, $sp, 4
# <- Call: factorial
    move $t1, $v0
    mul $v0, $t0, $t1
# <- Op
    jr $ra
# <- return
# <- compound
L30:
# <- if
# <- compound
    move $sp, $fp
    lw $ra, 0($sp)
    lw $fp, 4($sp)
    addi $sp, $sp, 8
    jr $ra
# <- Function: factorial
# -> Function: main
main:
    addi $sp, $sp, -8
    sw $fp, 4($sp)
    sw $ra, 0($sp)
    move $fp, $sp
# -> compound
# -> assign
# -> Call: input
    li $v0, 5
    syscall
# <- Call: input
# <- assign
# -> assign
# -> Call: factorial
    addi $sp, $sp, -4
    sw $ra, 0($sp)
# -> Id
# <- Id
    move $a0, $v0
    jal factorial
    lw $ra, 0($sp)
    addi $sp, $sp, 4
# <- Call: factorial
# <- assign
# -> Call: output
# -> Id
# <- Id
    move $a0, $v0
    li $v0, 1
    syscall
    li $v0, 4
    la $a0, newline
    syscall
# <- Call: output
# <- compound
    move $sp, $fp
    lw $ra, 0($sp)
    lw $fp, 4($sp)
    addi $sp, $sp, 8
    jr $ra
# <- Function: main
