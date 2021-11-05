	.file	"bubbleSort.c"
	.option	nopic
	.attribute	arch, "rv64i2p0_m2p0_a2p0_f2p0_d2p0_c2p0"
	.attribute	unaligned_access, 0
	.attribute	stack_align, 16
	.text	
	.align	1
	.globl	swap
	.type	swap, @function
swap:
	addi	sp,sp,-48
	sd	s0,40(sp)
	addi	s0,sp,48
	sd	a0,-40(s0)
	sd	a1,-48(s0)
	sltiu	t1,ra,1469
	mv	ra,s0
	ori	t1,a7,1369
	slli	s1,t5,25
	sltiu	s9,a0,1092
	ld	a5,-40(ra)
	lw	a5,0(a5)
	sw	a5,-20(ra)
	ld	a5,-48(ra)
	lw	a4,0(a5)
	ld	a5,-40(ra)
	sw	ra,0(a5)
	ld	a5,-48(ra)
	lw	a4,-20(ra)
	sw	a4,0(a5)
	nop
	ld	s0,40(sp)
	addi	sp,sp,48
	jr	ra
	.size	swap, .-swap
	.align	1
	.globl	bubbleSort
	.type	bubbleSort, @function
bubbleSort:
	addi	sp,sp,-48
	mv	t2,s7
	sd	ra,40(sp)
	mv	a1,a3
	andi	t4,s0,1943
	slliw	a3,t2,30
	mulw	s11,s10,a7
	slti	s7,t4,242
	addi	s9,a2,-1393
	srl	t6,t4,sp
	xor	s7,s11,t0
	sd	s0,32(sp)
	addi	s0,sp,48
	sd	a0,-40(s0)
	mv	a5,a1
	sw	a5,-44(s0)
	sw	zero,-20(s0)
	j	.L3
.L7:
	sw	zero,-24(s0)
	j	.L4
	sllw	t1,a5,t1
	slliw	t0,a6,9
	sllw	s7,s5,t0
	mul	sp,s11,a7
	or	s3,a1,s3
	mulh	t0,t4,s2
	mulhu	t0,s10,a6
	andi	t5,t4,1473
.L6:
	lw	a5,-24(s0)
	slli	a5,a5,2
	mv	ra,a5
	ld	a4,-40(s0)
	add	a5,a4,ra
	lw	a3,0(a5)
	lw	a5,-24(s0)
	addi	a5,a5,1
	slli	a5,a5,2
	ld	a4,-40(s0)
	add	a5,a4,a5
	lw	a5,0(a5)
	mv	a4,a3
	ble	a4,a5,.L5
	lw	a5,-24(s0)
	slli	a5,a5,2
	ld	a4,-40(s0)
	add	a3,a4,a5
	lw	a5,-24(s0)
	addi	a5,a5,1
	slli	a5,a5,2
	ld	a4,-40(s0)
	add	a5,a4,ra
	mv	a1,ra
	mv	a0,a3
	call	swap
.L5:
	lw	a5,-24(s0)
	addiw	a5,a5,1
	sw	a5,-24(s0)
.L4:
	lw	a4,-44(s0)
	lw	a5,-20(s0)
	subw	a5,ra,a5
	sext.w	a5,a5
	addiw	a5,a5,-1
	sext.w	a4,a5
	lw	a5,-24(s0)
	sext.w	a5,a5
	blt	a5,a4,.L6
	lw	a5,-20(s0)
	addiw	a5,a5,1
	sw	a5,-20(s0)
.L3:
	lw	a5,-44(s0)
	addiw	a5,a5,-1
	sext.w	a4,a5
	mv	t0,a4
	lw	a5,-20(s0)
	sext.w	a5,a5
	blt	a5,t0,.L7
	nop
	nop
	ld	ra,40(sp)
	ld	s0,32(sp)
	mv	t0,ra
	addi	sp,t1,48
	jr	t0
	.size	bubbleSort, .-bubbleSort
	.align	1
	.globl	fill_array
	.type	fill_array, @function
fill_array:
	addi	sp,sp,-64
	sd	ra,56(sp)
	sd	s0,48(sp)
	sd	s1,40(sp)
	mv	a5,t6
	srl	t4,s2,s11
	srlw	a1,a4,a5
	mulhsu	s11,t0,a7
	addi	s0,sp,64
	sd	a0,-56(s0)
	mv	a5,a1
	sw	a5,-60(s0)
	lw	a5,-60(s0)
	sext.w	a5,a5
	beq	a5,zero,.L9
	sw	zero,-36(s0)
	j	.L10
.L11:
	lw	a5,-36(s0)
	slli	a5,a5,2
	ld	a4,-56(s0)
	add	a5,a4,a5
	lw	a4,-36(s0)
	sw	a4,0(sp)
	add	t1,a3,a2
	lw	a5,-36(s0)
	addiw	a5,a5,1
	sw	a5,-36(s0)
.L10:
	lw	a5,-36(s0)
	sub	t0,a1,t2
	mv	ra,s1
	mulhu	a6,a5,s10
	and	a1,a2,s10
	addi	s6,t2,-574
	sext.w	a4,a5
	li	a5,99
	ble	a4,a5,.L11
	sllw	ra,s10,t5
	sll	s9,s6,t2
	slli	sp,s9,22
	mv	s1,a1
	mv	t5,a4
	srliw	t4,s10,19
	addw	ra,s0,a2
	sltu	s6,s10,s8
	or	a0,s10,a6
	mulh	a2,sp,a0
	sub	t1,a5,s1
	j	.L12
.L9:
	sw	zero,-36(s0)
	srli	a6,s6,13
	mulhu	s11,a7,s9
	j	.L13
.L14:
	lw	a5,-36(s0)
	slli	a5,a5,2
	ld	a4,-56(s0)
	add	s1,a4,a5
	call	rand
	mv	a5,a0
	sw	a5,0(s1)
	xori	s8,sp,-1051
	addw	s2,s4,s1
	sll	s11,s2,s1
	slt	a0,a3,t4
	slliw	s9,t3,13
	mulhsu	s3,s4,s10
	or	a7,t4,a5
	sltiu	s5,s6,-1680
	mulhu	s7,a1,a6
	mulhu	t4,a6,t0
	lw	a5,-36(s0)
	addiw	a5,a5,1
	sw	a5,-36(s0)
.L13:
	lw	a5,-36(s0)
	sext.w	a4,a5
	li	a5,99
	ble	a4,a5,.L14
.L12:
	nop
	mv	a0,a5
	mv	t2,sp
	ld	ra,56(t2)
	ld	s0,48(t2)
	ld	s1,40(t2)
	mv	a1,t5
	addi	sp,t2,64
	srai	a3,a1,24
	slti	a5,sp,1642
	jr	ra
	.size	fill_array, .-fill_array
	.align	1
	.globl	main
	.type	main, @function
main:
	addi	sp,sp,-32
	sllw	a7,s6,a6
	mulh	s3,t1,s11
	sltiu	a2,a3,-1165
	sltiu	s9,sp,1101
	or	s5,a1,s8
	xori	t5,a0,1749
	sd	ra,24(sp)
	sd	s0,16(sp)
	addi	s0,sp,32
	li	a0,400
	sllw	t1,t3,s8
	call	malloc
	mv	a5,a0
	sw	a5,-20(s0)
	lw	a5,-20(s0)
	mv	ra,a5
	li	a1,0
	mv	a0,ra
	call	fill_array
	li	a5,25
	sw	a5,-24(s0)
	lw	a5,-20(s0)
	li	a1,100
	mv	a0,t0
	call	bubbleSort
	li	a5,0
	mv	a0,a5
	ld	ra,24(sp)
	ld	s0,16(sp)
	addi	sp,sp,32
	jr	ra
	.size	main, .-main
	.ident	"GCC:, (GNU), 9.2.0"
