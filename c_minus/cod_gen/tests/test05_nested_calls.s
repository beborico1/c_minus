# C- Compilation to MIPS
# File: test_programs/test05_nested_calls.s
.data
newline: .asciiz "\n"

.text
.globl main

# -> Function: doubleVal
func_doubleVal:
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
    mul $a0, $t0, $a0
# <- Op
    lw $ra, 4($sp)
    addi $sp, $sp, 8
    jr $ra
# <- return
# <- compound
# <- Function: doubleVal
# -> Function: tripleVal
func_tripleVal:
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
    mul $a0, $t0, $a0
# <- Op
    lw $ra, 4($sp)
    addi $sp, $sp, 8
    jr $ra
# <- return
# <- compound
# <- Function: tripleVal
# -> Function: main
main:
# -> compound
# -> Call: output
# -> Call: doubleVal
# -> Call: tripleVal
# -> Const
    li $a0, 4
# <- Const
    jal func_tripleVal
# <- Call: tripleVal
    jal func_doubleVal
# <- Call: doubleVal
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
