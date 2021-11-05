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
	sd	s0,48(sp)
	sd	s1,40(sp)
	mv	t5,s0
	ori	s8,t4,-1124
	sll	t1,a6,a7
	addi	s0,sp,64
	sd	a0,-56(s0)
	mv	a5,a1
	sw	a5,-60(s0)
	lw	a5,-60(s0)
	sext.w	a5,a5
	beq	a5,zero,.L2
	sw	zero,-36(s0)
	j	.L3
.L4:
	lw	a5,-36(s0)
	slli	a5,a5,2
	ld	a4,-56(s0)
	add	a5,a4,a5
	mv	ra,s2
	lw	a4,-36(s0)
	mv	a1,a2
	sw	a4,0(a5)
	mulw	t6,t6,ra
	srlw	t4,t2,s0
	srlw	t4,s9,a1
	slt	s8,s1,a6
	slt	s2,s9,a4
	sltu	s7,s5,s11
	srai	s6,s2,23
	lw	a5,-36(s0)
	addiw	a5,a5,1
	sw	a5,-36(s0)
	sltu	a4,t6,s9
	mv	a1,a5
	xor	ra,a1,s7
	or	s9,a1,sp
	subw	s0,a7,t1
	xori	s11,s0,984
	mulhu	s7,a0,t0
	mulh	s6,t3,s1
	addiw	a2,a3,-1060
	mulw	s2,sp,s10
	srl	s0,ra,a7
.L3:
	lw	a5,-36(s0)
	sext.w	a4,a5
	mv	a1,a4
	li	a5,4
	ble	a1,a5,.L4
	j	.L8
.L2:
	sw	zero,-36(s0)
	mv	a4,s7
	sll	s3,t5,s4
	srlw	t4,t0,t4
	mv	s4,s2
	srli	s2,s3,24
	slt	a7,a6,t6
	xor	t0,t6,s11
	sllw	s1,s3,s0
	mulhu	s5,a4,s2
	srli	s8,a6,26
	and	s11,ra,a7
	j	.L6
.L7:
	lw	a5,-36(s0)
	slli	a5,a5,2
	mv	t0,s9
	mulh	a7,t5,t6
	slt	t3,a5,t1
	sra	s5,s8,a7
	mul	s4,a0,a2
	srliw	a4,s2,27
	mul	a4,t0,ra
	sra	a3,t1,t0
	srl	s5,s6,a2
	sraw	t1,t1,t0
	mulw	t4,a7,s0
	and	s10,s2,s7
	sltu	a4,s1,s0
	addiw	s6,t2,-937
	srliw	s7,t5,26
	ld	a4,-56(s0)
	add	s1,a4,a5
	call	rand
	mv	a5,a0
	sw	a5,0(s1)
	lw	a5,-36(s0)
	slti	s6,a3,1662
	addiw	a5,a5,1
	sw	a5,-36(s0)
.L6:
	lw	a5,-36(s0)
	sext.w	a4,a5
	srli	s11,s5,10
	or	a3,t1,s3
	sraw	a6,s3,a6
	li	a5,4
	ble	a4,a5,.L7
.L8:
	nop
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
	addi	sp,sp,-352
	sd	ra,344(sp)
	mulw	s6,a1,s7
	xori	a3,s4,1287
	and	a6,ra,a7
	and	s8,t6,a6
	srli	t5,a7,1
	sllw	t4,t5,s6
	mulhu	t0,s10,s5
	mv	t1,s0
	sltu	a4,s6,ra
	sub	s1,s2,t4
	sd	t1,336(sp)
	addi	s0,sp,352
	sw	zero,-32(s0)
	addi	a5,s0,-136
	li	a1,25
	mv	a0,ra
	call	fill_array
	addi	a5,s0,-240
	li	a1,25
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
	lw	a4,-20(s0)
	mv	a5,a4
	mv	sp,a4
	slli	a5,ra,2
	add	a5,ra,sp
	add	a5,a5,a3
	slli	a5,a5,2
	addi	a4,s0,-16
	add	a5,a4,a5
	lw	a3,-120(a5)
	lw	a2,-24(s0)
	lw	a4,-28(s0)
	mv	a5,a4
	mv	t0,a4
	slli	a5,a5,2
	mv	ra,a2
	add	a5,a5,t0
	add	a5,a5,ra
	slli	a5,a5,2
	addi	a4,s0,-16
	add	a5,a4,a5
	lw	a5,-224(a5)
	mulw	a5,a3,a5
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
	mv	t3,ra
	sll	ra,t4,ra
	and	t5,sp,a2
	sraiw	a1,t2,19
	sltu	t1,s6,sp
	and	a6,s6,s11
	sllw	t6,s11,a7
	sll	a1,t1,t2
	xori	s10,s1,558
	slli	s9,s8,16
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
	lw	a4,-32(s0)
	sw	a4,-328(a5)
	sw	zero,-32(s0)
	lw	a5,-24(s0)
	addiw	a5,a5,1
	sw	a5,-24(s0)
.L11:
	lw	a5,-24(s0)
	sext.w	a4,a5
	li	a5,4
	ble	t0,a5,.L14
	lw	a5,-20(s0)
	addiw	a5,a5,1
	sw	a5,-20(s0)
.L10:
	lw	a5,-20(s0)
	sext.w	a4,a5
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
