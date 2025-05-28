# C- Compilation to MIPS
# File: test_programs/test14_chain_calls.s
.data
newline: .asciiz "\n"

.text
.globl main

# -> Function: addOne
func_addOne:
    addi $sp, $sp, -8
    sw $ra, 4($sp)
    sw $a0, 0($sp)
# -> compound
# -> return
# -> Op
# -> Id
    lw $a0, 0($sp)
# <- Id
    move $t0, $a0
# -> Const
    li $a0, 1
# <- Const
    add $a0, $t0, $a0
# <- Op
    lw $ra, 4($sp)
    addi $sp, $sp, 8
    jr $ra
# <- return
# <- compound
# <- Function: addOne
# -> Function: addTwo
func_addTwo:
    addi $sp, $sp, -8
    sw $ra, 4($sp)
    sw $a0, 0($sp)
# -> compound
# -> return
# -> Op
# -> Id
    lw $a0, 0($sp)
# <- Id
    move $t0, $a0
# -> Const
    li $a0, 2
# <- Const
    add $a0, $t0, $a0
# <- Op
    lw $ra, 4($sp)
    addi $sp, $sp, 8
    jr $ra
# <- return
# <- compound
# <- Function: addTwo
# -> Function: addThree
func_addThree:
    addi $sp, $sp, -8
    sw $ra, 4($sp)
    sw $a0, 0($sp)
# -> compound
# -> return
# -> Op
# -> Id
    lw $a0, 0($sp)
# <- Id
    move $t0, $a0
# -> Const
    li $a0, 3
# <- Const
    add $a0, $t0, $a0
# <- Op
    lw $ra, 4($sp)
    addi $sp, $sp, 8
    jr $ra
# <- return
# <- compound
# <- Function: addThree
# -> Function: main
main:
# -> compound
# -> Call: output
# -> Call: addThree
# -> Call: addTwo
# -> Call: addOne
# -> Const
    li $a0, 10
# <- Const
    jal func_addOne
# <- Call: addOne
    jal func_addTwo
# <- Call: addTwo
    jal func_addThree
# <- Call: addThree
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
