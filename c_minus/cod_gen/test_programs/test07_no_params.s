# C- Compilation to MIPS
# File: test_programs/test07_no_params.s
.data
newline: .asciiz "\n"

.text
.globl main

# -> Function: getValue
func_getValue:
    addi $sp, $sp, -4
    sw $ra, 0($sp)
# -> compound
# -> return
# -> Const
    li $a0, 42
# <- Const
    lw $ra, 0($sp)
    addi $sp, $sp, 4
    jr $ra
# <- return
# <- compound
# <- Function: getValue
# -> Function: main
main:
    addi $sp, $sp, -4
# -> compound
# -> assign
# -> Call: getValue
    jal func_getValue
# <- Call: getValue
    sw $a0, -4($sp)
# <- assign
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
