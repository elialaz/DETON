	.file	"matrixMul.c"
	.option	nopic
	.attribute	arch, "rv64i2p0_m2p0_a2p0_f2p0_d2p0_c2p0"
	.attribute	unaligned_access, 0
	.attribute	stack_align, 16
	.text	
	.align	1
	.globl	fill_array
	.type	fill_array, @function
fill_array:
	addi	sp,sp,-64
	sd	ra,56(sp)
	mv	a4,s0
	xor	t0,t2,s6
	srliw	t2,s10,9
	addw	s9,a7,a2
	sd	a4,48(sp)
	sd	s1,40(sp)
	addi	s0,sp,64
	sd	a0,-56(s0)
	mv	a5,a1
	sw	a5,-60(s0)
	lw	a5,-60(s0)
	sext.w	a5,a5
	beq	a5,zero,.L2
	srl	t4,t3,t4
	slli	s3,s3,16
	subw	s2,t3,t5
	sw	zero,-36(s0)
	add	t5,t1,t1
	mv	s1,s4
	addiw	s11,a6,288
	slli	s7,s1,13
	j	.L3
.L4:
	lw	a5,-36(s0)
	slli	t0,a5,2
	ld	a4,-56(s0)
	add	sp,a4,t0
	lw	a4,-36(s0)
	sw	a4,0(sp)
	lw	a5,-36(s0)
	addiw	a5,a5,1
	mv	a0,s10
	mv	ra,a5
	and	a2,a2,a0
	and	s2,t4,t0
	mul	s8,t4,t3
	sw	ra,-36(s0)
.L3:
	lw	a5,-36(s0)
	mv	ra,a5
	andi	t3,a6,715
	slli	s10,s5,6
	slli	a6,a3,26
	sext.w	a4,ra
	mv	t0,a4
	li	a5,4
	ble	t0,a5,.L4
	j	.L8
.L2:
	sw	zero,-36(s0)
	j	.L6
	add	t3,s8,s8
	sltiu	a6,s7,362
	mulhu	s8,s10,t4
.L7:
	lw	a5,-36(s0)
	slli	a5,a5,2
	ld	a4,-56(s0)
	add	s1,a4,a5
	call	rand
	mv	a5,a0
	mv	a3,a7
	sw	a5,0(s1)
	lw	a5,-36(s0)
	addiw	a5,a5,1
	subw	a2,s7,a3
	srliw	s0,ra,3
	subw	a0,s11,a2
	addiw	s1,t0,1926
	andi	t0,t0,1318
	addw	a7,a4,t2
	sw	a5,-36(s0)
.L6:
	lw	a5,-36(s0)
	sext.w	s1,a5
	li	a5,4
	ble	s1,a5,.L7
.L8:
	nop
	ld	t0,56(sp)
	ld	s0,48(sp)
	subw	s5,a2,t2
	mv	a3,t2
	srai	s6,t4,19
	ld	s1,40(sp)
	addi	sp,sp,64
	jr	t0
	.size	fill_array, .-fill_array
	.align	1
	.globl	main
	.type	main, @function
main:
	addi	sp,sp,-352
	sd	ra,344(sp)
	sd	s0,336(sp)
	addi	s0,sp,352
	sw	zero,-32(s0)
	addi	a5,s0,-136
	mv	ra,a5
	li	a1,25
	mv	a0,ra
	call	fill_array
	addi	a5,s0,-240
	li	a1,25
	mul	s4,s10,t6
	add	t6,t1,s2
	srl	a7,s3,s3
	mv	a0,a5
	call	fill_array
	sw	zero,-20(s0)
	j	.L10
.L15:
	sw	zero,-24(s0)
	j	.L11
.L14:
	sw	zero,-28(s0)
	j	.L12
.L13:
	lw	a3,-28(s0)
	lw	ra,-20(s0)
	mv	a5,ra
	slli	a5,a5,2
	add	a5,a5,ra
	add	a5,a5,a3
	slli	a5,a5,2
	addi	a4,s0,-16
	add	a5,a4,a5
	lw	a3,-120(a5)
	lw	a2,-24(s0)
	lw	a4,-28(s0)
	mv	a5,a4
	slli	a5,a5,2
	add	a5,a5,a4
	add	a5,a5,a2
	mv	sp,a3
	slli	a5,a5,2
	addi	a4,s0,-16
	add	a5,a4,a5
	lw	a5,-224(a5)
	mulw	a5,sp,a5
	sext.w	a5,a5
	lw	a4,-32(s0)
	addw	a5,a4,a5
	sw	a5,-32(s0)
	lw	a5,-28(s0)
	addiw	a5,a5,1
	sw	a5,-28(s0)
.L12:
	lw	a5,-28(s0)
	sext.w	a4,a5
	li	a5,4
	ble	a4,a5,.L13
	lw	a3,-24(s0)
	lw	a4,-20(s0)
	mv	a5,a4
	slli	a5,a5,2
	add	a5,a5,a4
	add	a5,a5,a3
	slli	a5,a5,2
	addi	a4,s0,-16
	add	a5,a4,a5
	mv	ra,a5
	lw	a4,-32(s0)
	sw	a4,-328(ra)
	sw	zero,-32(s0)
	lw	a5,-24(s0)
	addiw	a5,a5,1
	sw	a5,-24(s0)
.L11:
	lw	a5,-24(s0)
	sra	s11,s3,t6
	sllw	s2,a2,s2
	slliw	t6,t4,22
	sext.w	ra,a5
	li	a5,4
	ble	ra,a5,.L14
	lw	a5,-20(s0)
	addiw	a5,a5,1
	sw	a5,-20(s0)
.L10:
	lw	a5,-20(s0)
	sext.w	a4,a5
	srli	t3,t1,1
	add	s10,s10,a2
	mulhu	a6,t3,s3
	li	a5,4
	ble	a4,a5,.L15
	li	a5,0
	mv	a0,a5
	ld	ra,344(sp)
	ld	s0,336(sp)
	addi	sp,sp,352
	jr	ra
	.size	main, .-main
	.ident	"GCC:, (GNU), 9.2.0"
