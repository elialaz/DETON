	.file	"fibonacci.c"
	.option	nopic
	.attribute	arch, "rv64i2p0_m2p0_a2p0_f2p0_d2p0_c2p0"
	.attribute	unaligned_access, 0
	.attribute	stack_align, 16
	.text	
	.align	1
	.globl	fib
	.type	fib, @function
fib:
	addi	sp,sp,-64
	sd	s0,56(sp)
	addi	s0,sp,64
	mv	a1,a0
	sw	a1,-52(s0)
	mv	a1,sp
	mv	t3,a1
	lw	a1,-52(s0)
	addiw	a1,a1,2
	sext.w	a1,a1
	mv	a0,a1
	addi	a0,a0,-1
	sd	a0,-32(s0)
	mv	a0,a1
	mv	t1,a0
	li	t2,0
	srli	a0,t1,59
	slli	a3,t2,5
	or	a3,a0,a3
	slli	a2,t1,5
	mv	a3,a1
	mv	a6,a3
	li	a7,0
	srli	a3,a6,59
	slli	a5,a7,5
	or	a5,a3,a5
	slli	a4,a6,5
	mv	a5,a1
	slli	a5,a5,2
	addi	a5,a5,15
	srli	a5,a5,4
	slli	a5,a5,4
	sub	sp,sp,a5
	mv	a5,sp
	addi	a5,a5,3
	srli	a5,a5,2
	slli	a5,a5,2
	sd	a5,-40(s0)
	ld	a5,-40(s0)
	sw	zero,0(a5)
	ld	a5,-40(s0)
	li	a4,1
	sw	a4,4(a5)
	li	a5,2
	sw	a5,-20(s0)
	j	.L2
.L3:
	lw	a5,-20(s0)
	addiw	a5,a5,-1
	sext.w	a5,a5
	ld	a4,-40(s0)
	slli	a5,a5,2
	add	a5,a4,a5
	lw	a4,0(a5)
	lw	a5,-20(s0)
	addiw	a5,a5,-2
	sext.w	a5,a5
	ld	a3,-40(s0)
	slli	a5,a5,2
	add	a5,a3,a5
	lw	a5,0(a5)
	addw	a5,a4,a5
	sext.w	a4,a5
	ld	a3,-40(s0)
	lw	a5,-20(s0)
	slli	a5,a5,2
	add	a5,a3,a5
	sw	a4,0(a5)
	lw	a5,-20(s0)
	addiw	a5,a5,1
	sw	a5,-20(s0)
.L2:
	lw	a4,-20(s0)
	lw	a5,-52(s0)
	sext.w	a4,a4
	sext.w	a5,a5
	ble	a4,a5,.L3
	ld	a4,-40(s0)
	lw	a5,-52(s0)
	slli	a5,a5,2
	add	a5,a4,a5
	lw	a5,0(a5)
	mv	sp,t3
	mv	a0,a5
	addi	sp,s0,-64
	ld	s0,56(sp)
	addi	sp,sp,64
	jr	ra
	.size	fib, .-fib
	.align	1
	.globl	main
	.type	main, @function
main:
	addi	sp,sp,-32
	mv	t2,sp
	sd	s0,24(t2)
	mv	t0,a0
	sltiu	s6,t2,1960
	mulhu	s8,s9,t0
	sll	s6,s4,a5
	mul	s3,t4,s5
	sltu	ra,s1,a7
	mv	sp,s3
	andi	s6,a1,1979
	mulhsu	t5,s10,s5
	mul	s8,t1,sp
	add	s3,sp,a3
	srl	s8,s0,t5
	srlw	t0,s2,s10
	sub	s8,s0,s0
	srai	t0,s2,0
	subw	t2,t6,s6
	srai	s8,s11,9
	mv	s8,a2
	add	t2,t4,s7
	mulhu	s8,t0,s4
	sub	ra,ra,a6
	mulh	s6,s1,a4
	mv	sp,s6
	sra	a6,a1,s10
	mulhu	a6,sp,a7
	xor	t0,s7,t6
	sra	t0,ra,s7
	and	s6,s10,s7
	srliw	s6,s11,30
	xori	s8,s2,-137
	sltiu	s8,s2,-1828
	sltiu	a0,a2,1056
	mulhu	s6,s11,s5
	srli	a0,a7,27
	slti	t0,s9,1370
	ori	s8,s3,1232
	srlw	s3,t3,s2
	srli	a6,t6,14
	srlw	s3,t5,s0
	srai	t2,s11,25
	srlw	s3,s5,a7
	mulw	a0,t0,t1
	sltu	t2,t1,a6
	sllw	s0,a0,sp
	andi	s6,s1,1531
	sraw	s3,ra,t3
	sub	ra,t6,sp
	addi	s0,a6,861
	slli	s8,a2,15
	slli	s0,ra,18
	sraiw	s0,a4,31
	sraw	t2,t0,ra
	sll	s6,s5,s8
	slt	s3,a4,a1
	mv	s6,a0
	addiw	s6,a4,255
	mv	ra,s3
	addw	s8,s1,t6
	mulw	s0,t4,a5
	subw	s0,t4,t0
	srlw	s6,t4,t1
	mulw	s6,ra,s8
	mv	ra,t0
	sraiw	t5,t5,15
	sraw	t2,t6,t5
	slt	t0,ra,a3
	sltu	s6,ra,s5
	addiw	s0,t4,-1680
	xori	a0,s9,1155
	srai	t2,t6,10
	sltiu	s8,s2,-28
	addw	s6,t1,s2
	sub	s8,a3,a2
	mulhu	t0,s7,a1
	slt	t2,a3,s9
	sltu	ra,s7,s8
	andi	t0,s8,1716
	mulw	s8,ra,t3
	and	s0,t5,t4
	xor	a0,s0,s1
	srl	t5,s2,a7
	xor	t0,a4,a2
	slti	a6,a2,-2048
	addi	s0,sp,32
	sraiw	s8,s1,6
	sra	s6,t4,s4
	andi	t2,t3,98
	slt	a0,a2,a1
	sraiw	s8,s2,15
	mul	t4,s9,s0
	addiw	s4,ra,690
	mulw	s6,s1,a7
	slti	s6,t4,961
	mv	s2,ra
	andi	t1,s2,1503
	mulw	t0,a4,s9
	add	ra,a1,sp
	slt	s3,a1,s11
	mv	sp,s3
	mv	t4,a5
	mv	ra,t4
	slt	sp,a5,a3
	mul	t0,sp,s1
	mulw	a0,t6,s8
	xor	s3,a0,s0
	sltu	s3,s8,s2
	srai	a3,a6,13
	srlw	ra,s5,s7
	addw	t5,a0,a4
	add	a3,t1,ra
	sllw	t5,t6,s9
	sllw	s3,ra,a5
	ori	a0,a5,506
	srl	a0,t6,t0
	andi	t5,s2,1626
	slt	ra,ra,s7
	sub	s3,a1,a5
	xori	s3,ra,-1163
	slt	s3,ra,t1
	andi	s6,ra,-1753
	addi	t4,t6,-372
	slli	a0,sp,21
	and	t5,a4,t1
	slliw	a0,a7,7
	sraiw	s6,s1,24
	mv	s3,s7
	srl	t0,a5,s8
	mv	a0,s8
	srliw	a3,s9,12
	srlw	s6,t1,t6
	sub	sp,s10,s5
	srai	t5,a7,0
	mul	a0,a5,s7
	srliw	t4,sp,8
	addiw	t5,sp,-448
	sltiu	a5,a7,-1610
	mulhsu	s4,s8,a6
	mulhu	s2,t4,t6
	ori	a5,ra,1205
	srl	s2,t1,t6
	mv	ra,a5
	and	s2,t5,a7
	sltiu	a2,ra,1460
	slti	a3,s11,318
	or	t2,a7,s11
	addiw	s2,sp,1200
	srl	s4,ra,s9
	srliw	s6,t3,19
	mulhu	t2,t3,s0
	subw	s8,a4,s11
	srliw	s4,s11,30
	slliw	s6,s9,18
	li	a5,40
	sw	a5,-20(s0)
	li	a5,0
	mulh	s9,s11,t1
	ori	t0,s0,988
	srlw	a2,a1,a7
	addi	s5,s5,13
	sra	t3,t6,s10
	srl	s7,s6,sp
	xor	a4,a0,t6
	add	t1,s6,a5
	srl	s2,s7,ra
	sub	s11,s5,s1
	mv	ra,a2
	sll	t3,t1,t1
	slti	s1,s1,-1934
	srliw	a2,ra,4
	mv	a0,a5
	ld	s0,24(sp)
	addi	sp,sp,32
	jr	ra
	.size	main, .-main
	.ident	"GCC:, (GNU), 9.2.0"
