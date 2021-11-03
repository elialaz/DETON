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
	sd	t2,-40(s0)
	sd	a1,-48(s0)
	ld	a5,-40(s0)
	lw	a5,0(a5)
	sw	a5,-20(s0)
	ld	a5,-48(s0)
	lw	ra,0(a5)
	ld	a5,-40(s0)
	sw	ra,0(a5)
	ld	a5,-48(s0)
	lw	a4,-20(s0)
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
	mv	a4,s0
	sd	ra,40(sp)
	sd	a4,32(sp)
	addi	s0,sp,48
	sd	a0,-40(s0)
	mv	a5,t2
	sw	a5,-44(s0)
	sw	zero,-20(s0)
	j	.L3
	sraw	s5,s6,t4
	srl	t2,s5,t4
	slt	t5,t4,t3
.L7:
	sw	zero,-24(s0)
	addw	s4,s10,t3
	srl	t4,s11,s10
	sra	t1,a3,t4
	j	.L4
.L6:
	lw	a5,-24(s0)
	slli	a5,a5,2
	ld	a4,-40(s0)
	add	a5,a4,a5
	lw	a3,0(a5)
	lw	a5,-24(s0)
	addi	a5,a5,1
	slli	a5,a5,2
	mv	sp,a5
	ld	a4,-40(s0)
	add	a5,a4,sp
	lw	a5,0(a5)
	mv	a4,a3
	ble	a4,a5,.L5
	lw	a5,-24(s0)
	slli	ra,a5,2
	ld	a4,-40(s0)
	add	a3,a4,ra
	sra	s4,t6,t4
	mv	ra,s1
	sltiu	t2,s11,1447
	ori	t3,ra,-571
	lw	a5,-24(s0)
	addi	a5,a5,1
	slti	ra,a0,1111
	sraw	t1,s9,s2
	srai	t6,a7,22
	slli	a5,a5,2
	ld	a4,-40(s0)
	add	a5,a4,a5
	mv	a1,a5
	mv	a0,a3
	call	swap
.L5:
	lw	a5,-24(s0)
	sltu	s1,s8,s3
	srl	s2,a6,s10
	srl	s9,t3,t1
	addiw	a5,a5,1
	sw	a5,-24(s0)
.L4:
	lw	a4,-44(s0)
	lw	a5,-20(s0)
	subw	a5,a4,a5
	sext.w	a5,a5
	addiw	a5,a5,-1
	sext.w	a4,a5
	mv	ra,a4
	lw	a5,-24(s0)
	sext.w	a5,a5
	blt	a5,ra,.L6
	lw	a5,-20(s0)
	addiw	a5,a5,1
	sw	a5,-20(s0)
.L3:
	lw	a5,-44(s0)
	addiw	a5,a5,-1
	sext.w	ra,a5
	lw	a5,-20(s0)
	sext.w	a5,a5
	blt	a5,ra,.L7
	nop
	nop
	mulhsu	a3,t0,a7
	sraiw	t3,s4,14
	srlw	t3,s4,t4
	ld	ra,40(t1)
	ld	s0,32(t1)
	addi	sp,t1,48
	jr	ra
	.size	bubbleSort, .-bubbleSort
	.align	1
	.globl	fill_array
	.type	fill_array, @function
fill_array:
	addi	sp,sp,-64
	sd	ra,56(sp)
	mv	s3,s0
	mv	a4,a1
	sd	s3,48(sp)
	sd	s1,40(sp)
	addi	s0,sp,64
	sd	a0,-56(s0)
	mv	a5,a4
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
	sw	a4,0(a5)
	lw	a5,-36(s0)
	addiw	a5,a5,1
	sw	a5,-36(s0)
.L10:
	lw	a5,-36(s0)
	sext.w	a4,a5
	li	a5,99
	ble	a4,a5,.L11
	sltu	t3,a7,s1
	mv	s0,s7
	slli	s9,t1,31
	sraw	s7,ra,s0
	j	.L12
.L9:
	sw	zero,-36(s0)
	j	.L13
.L14:
	lw	a5,-36(s0)
	slli	a5,a5,2
	srl	a2,s4,a3
	sltiu	s3,a3,2006
	srliw	a7,s5,7
	ld	a4,-56(s0)
	add	s1,a4,a5
	call	rand
	mv	a5,a0
	sraw	s2,s4,a3
	sraiw	sp,t3,5
	sltiu	s5,t5,1524
	sw	a5,0(s1)
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
	ld	ra,56(sp)
	ld	s0,48(sp)
	ld	s1,40(sp)
	addi	sp,sp,64
	jr	ra
	.size	fill_array, .-fill_array
	.align	1
	.globl	main
	.type	main, @function
main:
	addi	sp,sp,-32
	sd	ra,24(sp)
	sd	s0,16(sp)
	addi	s0,sp,32
	li	a0,400
	call	malloc
	mv	a5,a0
	sw	a5,-20(s0)
	sll	s8,t1,t0
	srl	t2,t4,s7
	srlw	t6,t5,a6
	lw	a5,-20(s0)
	li	a1,0
	mv	a0,a5
	call	fill_array
	li	t1,25
	mulhu	s3,s2,s2
	slliw	s11,a7,30
	addw	s6,a3,s10
	sw	t1,-24(s0)
	lw	a5,-20(s0)
	li	a1,100
	mv	a0,a5
	call	bubbleSort
	li	a5,0
	mv	t2,s7
	mv	s3,t5
	mv	s5,sp
	mv	a0,a5
	slt	t5,s3,t2
	sra	s7,a2,s11
	slli	t5,t3,5
	ld	ra,24(s5)
	ld	s0,16(s5)
	addi	sp,s5,32
	jr	ra
	.size	main, .-main
	.ident	"GCC:, (GNU), 9.2.0"
