# C- Compilation to MIPS
# File: prueba.s
.data
newline: .asciiz "\n"

.text
.globl main

# -> Function: factorial
factorial:
    addi $sp, $sp, -8
    sw $ra, 4($sp)
    sw $a0, 0($sp)
# -> compound
# -> if
# -> Op
# -> Id
    lw $v0, 0($sp)
# <- Id
    move $t0, $v0
# -> Const
    li $v0, 1
# <- Const
    move $t1, $v0
    ble $t0, $t1, L1
    li $v0, 0
    j L2
L1:
    li $v0, 1
L2:
# <- Op
    beqz $v0, L3
# -> compound
# -> return
# -> Const
    li $v0, 1
# <- Const
    lw $ra, 4($sp)
    addi $sp, $sp, 8
    jr $ra
# <- return
# <- compound
    j L4
L3:
# -> compound
# -> return
# -> Op
# -> Id
    lw $v0, 0($sp)
# <- Id
    move $t0, $v0
# -> Call: factorial
    addi $sp, $sp, -4
    sw $ra, 0($sp)
# -> Op
# -> Id
    lw $v0, 0($sp)
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
    lw $ra, 4($sp)
    addi $sp, $sp, 8
    jr $ra
# <- return
# <- compound
L4:
# <- if
# <- compound
# <- Function: factorial
# -> Function: main
main:
    addi $sp, $sp, -8
# -> compound
# -> assign
# -> Call: input
    li $v0, 5
    syscall
# <- Call: input
    sw $v0, -4($sp)
# <- assign
# -> assign
# -> Call: factorial
    addi $sp, $sp, -4
    sw $ra, 0($sp)
# -> Id
    lw $v0, -4($sp)
# <- Id
    move $a0, $v0
    jal factorial
    lw $ra, 0($sp)
    addi $sp, $sp, 4
# <- Call: factorial
    sw $v0, -8($sp)
# <- assign
# -> Call: output
# -> Id
    lw $v0, -8($sp)
# <- Id
    move $a0, $v0
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
