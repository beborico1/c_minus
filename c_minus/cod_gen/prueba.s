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
    lw $a0, 0($sp)
# <- Id
    sw $a0, 0($sp)
    addi $sp, $sp, -4
# -> Const
    li $a0, 1
# <- Const
    lw $t1, 4($sp)
    addi $sp, $sp, 4
    ble $t1, $a0, L1
    li $a0, 0
    j L2
L1:
    li $a0, 1
L2:
# <- Op
    beqz $a0, L3
# -> compound
# -> return
# -> Const
    li $a0, 1
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
# -> Call: factorial
# -> Op
# -> Id
    lw $a0, 0($sp)
# <- Id
    sw $a0, 0($sp)
    addi $sp, $sp, -4
# -> Const
    li $a0, 1
# <- Const
    lw $t1, 4($sp)
    addi $sp, $sp, 4
    sub $a0, $t1, $a0
# <- Op
    jal factorial
# <- Call: factorial
    move $t1, $a0
# -> Id
    lw $a0, 0($sp)
# <- Id
    move $t0, $a0
    move $a0, $t1
    mul $a0, $t0, $a0
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
    move $a0, $v0
# <- Call: input
    sw $a0, -4($sp)
# <- assign
# -> assign
# -> Call: factorial
# -> Id
    lw $a0, -4($sp)
# <- Id
    jal factorial
# <- Call: factorial
    sw $a0, -8($sp)
# <- assign
# -> Call: output
# -> Id
    lw $a0, -8($sp)
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
