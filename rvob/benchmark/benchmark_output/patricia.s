	.file	"patricia.c"
	.option	nopic
	.attribute	arch, "rv64i2p0_m2p0_a2p0_f2p0_d2p0_c2p0"
	.attribute	unaligned_access, 0
	.attribute	stack_align, 16
	.text	
	.align	1
	.type	bit, @function
bit:
	addi	sp,sp,-32
	sltiu	a4,t4,-2007
	sub	a7,s8,t4
	addw	a4,s2,s7
	mulh	a7,a1,s2
	slli	s2,s1,20
	sra	s2,t3,a5
	mv	ra,a7
	sraw	a5,s3,s9
	mv	t6,t3
	mulhsu	t1,s7,sp
	addiw	s2,ra,1173
	mulhu	ra,t4,s5
	slliw	sp,s9,4
	mulhu	a5,s3,ra
	sd	s0,24(sp)
	addi	s0,sp,32
	mv	a5,a0
	sd	a1,-32(s0)
	slliw	t1,t5,31
	addw	s2,sp,s0
	slti	a7,s0,1937
	mulhsu	s6,ra,sp
	slli	ra,s3,31
	mv	s6,a2
	andi	a4,t4,-977
	mulhu	a7,t5,s2
	sltiu	s2,s0,-955
	sraw	a4,s8,s5
	addi	a4,a0,-874
	andi	s2,s5,1347
	mulh	t0,s2,t2
	sllw	a4,s3,sp
	and	t1,a6,ra
	mulhu	t1,t6,a5
	srliw	s6,t5,20
	sltu	t0,a1,sp
	sll	s6,s11,t6
	sltiu	t1,ra,-1614
	xori	t0,t4,-167
	mv	s6,t4
	srlw	s2,s5,t6
	sll	t6,s2,s8
	srliw	s2,a3,12
	sraiw	s2,s10,14
	sw	a5,-20(s0)
	lw	a5,-20(s0)
	li	a4,-2147483648
	srlw	a5,a4,a5
	sext.w	a5,a5
	sext.w	a5,a5
	mv	a4,a5
	ori	s9,s9,-1183
	sltiu	s6,a0,-1251
	and	t1,s1,s4
	sltiu	t6,ra,439
	addw	t0,a2,t1
	sraw	s2,t3,s10
	and	a7,s10,s1
	sltu	t0,a2,s5
	mv	sp,t0
	mv	ra,a7
	sub	t6,sp,sp
	add	sp,t4,s7
	andi	a7,ra,1705
	mv	a7,sp
	xori	s2,a7,-1847
	ld	a5,-32(s0)
	and	a5,a4,a5
	mv	a0,a5
	andi	t1,a5,939
	sltu	a7,a2,t2
	mulw	s6,a7,t3
	sltiu	s2,t3,967
	xori	t6,s3,1762
	addi	s7,a7,1188
	mv	s10,t6
	addiw	s9,a5,-1169
	srai	t1,s0,25
	mv	ra,t1
	mv	t2,ra
	subw	t2,s5,a4
	sll	ra,a4,a5
	slti	s9,t6,-250
	srai	t2,sp,6
	add	t0,t3,ra
	slt	a7,ra,ra
	sllw	t0,ra,s10
	addi	t6,t6,636
	addw	t6,a4,s10
	sraw	t0,s2,s4
	sra	s9,t4,a3
	xor	a7,a6,a6
	slliw	s9,a6,23
	srlw	s2,s10,a1
	mulw	s10,t4,ra
	sll	s1,ra,s10
	srl	s7,s3,s11
	mulhu	s1,t2,s0
	xor	s6,a6,s11
	mulw	t1,s4,s10
	sub	t0,s0,s3
	subw	a3,s0,s4
	sltu	a3,s8,t4
	sra	t6,t5,t3
	sub	s9,a4,a3
	mulh	s6,ra,t5
	mv	t1,s9
	mv	sp,t2
	slti	t0,t1,1529
	mulw	s1,t1,s1
	addw	t0,a6,s2
	mv	t1,s6
	mv	ra,s1
	slti	t6,t1,-570
	sllw	s10,s3,ra
	srli	t6,s8,27
	slli	s10,t4,29
	mulhsu	s6,sp,s11
	addiw	s7,sp,762
	addi	s7,a7,-1224
	mv	sp,t0
	xori	t6,t1,-1443
	sllw	a3,a3,s0
	mv	s9,s8
	srli	s6,s3,3
	sraw	s6,t4,s7
	add	a2,t5,s6
	sraw	a2,a7,ra
	xor	s7,a7,sp
	addw	t6,t1,a7
	mul	s1,s0,ra
	slt	a2,ra,t3
	mv	ra,a2
	addiw	s10,a7,-1176
	srl	t6,sp,s1
	slli	a7,t6,5
	mulh	t6,ra,a6
	srlw	t6,s11,s0
	srli	t0,a5,16
	slti	s9,ra,-511
	sraiw	s6,ra,15
	slt	s6,s5,t1
	mv	s9,s4
	addi	t0,s2,1402
	srlw	s11,s0,s0
	mulhsu	sp,t5,t4
	subw	s11,s8,a4
	slli	s11,a6,23
	srli	s2,s5,13
	mulh	s9,s1,s3
	srliw	s1,s4,1
	sra	t4,ra,s11
	mul	a7,t5,s2
	srliw	t5,s5,13
	ld	s0,24(sp)
	and	ra,s3,s8
	slti	s10,s1,509
	sub	t3,ra,t3
	sraw	s3,sp,ra
	srliw	t2,a4,19
	slti	s5,a1,-521
	or	s3,sp,sp
	slliw	a6,sp,28
	mulhsu	a2,a4,sp
	mv	s10,s2
	srliw	s3,a5,19
	srliw	s1,a5,29
	mul	s2,a0,sp
	addw	a7,s0,t1
	srl	s9,a2,t2
	subw	a3,s1,a5
	sub	t1,a4,s2
	and	s9,ra,t6
	subw	s7,s8,t1
	mulh	s1,a4,a6
	sllw	t4,s6,a0
	addiw	t6,s7,-423
	mulw	a7,t1,a0
	sll	a3,s8,t6
	andi	s8,ra,-443
	andi	t3,s4,-170
	addi	sp,sp,32
	jr	ra
	.size	bit, .-bit
	.align	1
	.type	pat_count, @function
pat_count:
	addi	sp,sp,-48
	sd	ra,40(sp)
	sd	s0,32(sp)
	addi	s0,sp,48
	sd	a0,-40(s0)
	mv	a5,a1
	sw	a5,-44(s0)
	ld	a5,-40(s0)
	lbu	a5,17(a5)
	sext.w	a4,a5
	lw	a5,-44(s0)
	sext.w	a5,a5
	blt	a5,a4,.L4
	li	a5,0
	j	.L5
.L4:
	ld	a5,-40(s0)
	lbu	a5,16(a5)
	sw	a5,-20(s0)
	ld	a5,-40(s0)
	ld	a4,24(a5)
	ld	a5,-40(s0)
	lbu	a5,17(a5)
	sext.w	a5,a5
	mv	a1,a5
	mv	a0,a4
	call	pat_count
	mv	a5,a0
	mv	a4,a5
	lw	a5,-20(s0)
	addw	a5,a5,a4
	sw	a5,-20(s0)
	ld	a5,-40(s0)
	ld	a4,32(a5)
	ld	a5,-40(s0)
	lbu	a5,17(a5)
	sext.w	a5,a5
	mv	a1,a5
	mv	a0,a4
	call	pat_count
	mv	a5,a0
	mv	a4,a5
	lw	a5,-20(s0)
	addw	a5,a5,a4
	sw	a5,-20(s0)
	lw	a5,-20(s0)
.L5:
	mv	a0,a5
	ld	ra,40(sp)
	ld	s0,32(sp)
	addi	sp,sp,48
	jr	ra
	.size	pat_count, .-pat_count
	.align	1
	.type	insertR, @function
insertR:
	addi	sp,sp,-48
	sd	ra,40(sp)
	sd	s0,32(sp)
	addi	s0,sp,48
	sd	a0,-24(s0)
	sd	a1,-32(s0)
	mv	a5,a2
	sd	a3,-48(s0)
	sw	a5,-36(s0)
	ld	a5,-24(s0)
	lbu	a5,17(a5)
	sext.w	a4,a5
	lw	a5,-36(s0)
	sext.w	a5,a5
	ble	a5,a4,.L7
	ld	a5,-24(s0)
	lbu	a4,17(a5)
	ld	a5,-48(s0)
	lbu	a5,17(a5)
	bgtu	a4,a5,.L8
.L7:
	lw	a5,-36(s0)
	andi	a4,a5,255
	ld	a5,-32(s0)
	sb	a4,17(a5)
	ld	a5,-32(s0)
	ld	a4,0(a5)
	lw	a5,-36(s0)
	mv	a1,a4
	mv	a0,a5
	call	bit
	mv	a5,a0
	beq	a5,zero,.L9
	ld	a5,-24(s0)
	j	.L10
.L9:
	ld	a5,-32(s0)
.L10:
	ld	a4,-32(s0)
	sd	a5,24(a4)
	ld	a5,-32(s0)
	ld	a4,0(a5)
	lw	a5,-36(s0)
	mv	a1,a4
	mv	a0,a5
	call	bit
	mv	a5,a0
	beq	a5,zero,.L11
	ld	a5,-32(s0)
	j	.L12
.L11:
	ld	a5,-24(s0)
.L12:
	ld	a4,-32(s0)
	sd	a5,32(a4)
	ld	a5,-32(s0)
	j	.L13
.L8:
	ld	a5,-24(s0)
	lbu	a5,17(a5)
	sext.w	a4,a5
	ld	a5,-32(s0)
	ld	a5,0(a5)
	mv	a1,a5
	mv	a0,a4
	call	bit
	mv	a5,a0
	beq	a5,zero,.L14
	ld	a5,-24(s0)
	ld	a5,32(a5)
	lw	a4,-36(s0)
	ld	a3,-24(s0)
	mv	a2,a4
	ld	a1,-32(s0)
	mv	a0,a5
	call	insertR
	mv	a4,a0
	ld	a5,-24(s0)
	sd	a4,32(a5)
	j	.L15
.L14:
	ld	a5,-24(s0)
	ld	a5,24(a5)
	lw	a4,-36(s0)
	ld	a3,-24(s0)
	mv	a2,a4
	ld	a1,-32(s0)
	mv	a0,a5
	call	insertR
	mv	a4,a0
	ld	a5,-24(s0)
	sd	a4,24(a5)
.L15:
	ld	a5,-24(s0)
.L13:
	mv	a0,a5
	ld	ra,40(sp)
	ld	s0,32(sp)
	addi	sp,sp,48
	jr	ra
	.size	insertR, .-insertR
	.align	1
	.globl	pat_insert
	.type	pat_insert, @function
pat_insert:
	addi	sp,sp,-80
	sd	ra,72(sp)
	sd	s0,64(sp)
	sd	s1,56(sp)
	addi	s0,sp,80
	sd	a0,-72(s0)
	sd	a1,-80(s0)
	ld	a5,-80(s0)
	beq	a5,zero,.L17
	ld	a5,-72(s0)
	beq	a5,zero,.L17
	ld	a5,-72(s0)
	ld	a5,8(a5)
	bne	a5,zero,.L18
.L17:
	li	a5,0
	j	.L19
.L18:
	ld	a5,-72(s0)
	ld	a4,0(a5)
	ld	a5,-72(s0)
	ld	a5,8(a5)
	ld	a5,0(a5)
	and	a4,a4,a5
	ld	a5,-72(s0)
	sd	a4,0(a5)
	ld	a5,-80(s0)
	sd	a5,-40(s0)
.L22:
	ld	a5,-40(s0)
	lbu	a5,17(a5)
	sw	a5,-52(s0)
	ld	a5,-40(s0)
	lbu	a5,17(a5)
	sext.w	a4,a5
	ld	a5,-72(s0)
	ld	a5,0(a5)
	mv	a1,a5
	mv	a0,a4
	call	bit
	mv	a5,a0
	beq	a5,zero,.L20
	ld	a5,-40(s0)
	ld	a5,32(a5)
	j	.L21
.L20:
	ld	a5,-40(s0)
	ld	a5,24(a5)
.L21:
	sd	a5,-40(s0)
	ld	a5,-40(s0)
	lbu	a5,17(a5)
	sext.w	a4,a5
	lw	a5,-52(s0)
	sext.w	a5,a5
	blt	a5,a4,.L22
	ld	a5,-72(s0)
	ld	a4,0(a5)
	ld	a5,-40(s0)
	ld	a5,0(a5)
	bne	a4,a5,.L23
	sw	zero,-52(s0)
	j	.L24
.L26:
	ld	a5,-72(s0)
	ld	a5,8(a5)
	ld	a4,0(a5)
	ld	a5,-40(s0)
	ld	a3,8(a5)
	lw	a5,-52(s0)
	slli	a5,a5,4
	add	a5,a3,a5
	ld	a5,0(a5)
	bne	a4,a5,.L25
	ld	a5,-72(s0)
	ld	a4,8(a5)
	ld	a5,-40(s0)
	ld	a3,8(a5)
	lw	a5,-52(s0)
	slli	a5,a5,4
	add	a5,a3,a5
	ld	a4,8(a4)
	sd	a4,8(a5)
	ld	a5,-72(s0)
	ld	a5,8(a5)
	mv	a0,a5
	call	free
	ld	a0,-72(s0)
	call	free
	sd	zero,-72(s0)
	ld	a5,-40(s0)
	j	.L19
.L25:
	lw	a5,-52(s0)
	addiw	a5,a5,1
	sw	a5,-52(s0)
.L24:
	ld	a5,-40(s0)
	lbu	a5,16(a5)
	sext.w	a4,a5
	lw	a5,-52(s0)
	sext.w	a5,a5
	blt	a5,a4,.L26
	ld	a5,-40(s0)
	lbu	a5,16(a5)
	sext.w	a5,a5
	addiw	a5,a5,1
	sext.w	a5,a5
	slli	a5,a5,4
	mv	a0,a5
	call	malloc
	mv	a5,a0
	sd	a5,-64(s0)
	sw	zero,-56(s0)
	sw	zero,-52(s0)
	ld	a5,-64(s0)
	sd	a5,-48(s0)
	j	.L27
.L30:
	ld	a5,-72(s0)
	ld	a5,8(a5)
	ld	a4,0(a5)
	ld	a5,-40(s0)
	ld	a3,8(a5)
	lw	a5,-52(s0)
	slli	a5,a5,4
	add	a5,a3,a5
	ld	a5,0(a5)
	bleu	a4,a5,.L28
	ld	a5,-40(s0)
	ld	a4,8(a5)
	lw	a5,-52(s0)
	slli	a5,a5,4
	add	a5,a4,a5
	li	a2,16
	mv	a1,a5
	ld	a0,-48(s0)
	call	memmove
	lw	a5,-52(s0)
	addiw	a5,a5,1
	sw	a5,-52(s0)
	j	.L29
.L28:
	ld	a5,-72(s0)
	ld	a5,8(a5)
	li	a2,16
	mv	a1,a5
	ld	a0,-48(s0)
	call	memmove
	ld	a5,-72(s0)
	ld	a5,8(a5)
	li	a4,-1
	srli	a4,a4,32
	sd	a4,0(a5)
	li	a5,1
	sw	a5,-56(s0)
.L29:
	ld	a5,-48(s0)
	addi	a5,a5,16
	sd	a5,-48(s0)
.L27:
	ld	a5,-40(s0)
	lbu	a5,16(a5)
	sext.w	a4,a5
	lw	a5,-52(s0)
	sext.w	a5,a5
	blt	a5,a4,.L30
	lw	a5,-56(s0)
	sext.w	a5,a5
	bne	a5,zero,.L31
	ld	a5,-72(s0)
	ld	a5,8(a5)
	li	a2,16
	mv	a1,a5
	ld	a0,-48(s0)
	call	memmove
.L31:
	ld	a5,-72(s0)
	ld	a5,8(a5)
	mv	a0,a5
	call	free
	ld	a0,-72(s0)
	call	free
	sd	zero,-72(s0)
	ld	a5,-40(s0)
	lbu	a5,16(a5)
	addiw	a5,a5,1
	andi	a4,a5,255
	ld	a5,-40(s0)
	sb	a4,16(a5)
	ld	a5,-40(s0)
	ld	a5,8(a5)
	mv	a0,a5
	call	free
	ld	a5,-40(s0)
	ld	a4,-64(s0)
	sd	a4,8(a5)
	ld	a5,-40(s0)
	j	.L19
.L23:
	li	a5,1
	sw	a5,-52(s0)
	j	.L32
.L34:
	lw	a5,-52(s0)
	addiw	a5,a5,1
	sw	a5,-52(s0)
.L32:
	lw	a5,-52(s0)
	sext.w	a4,a5
	li	a5,31
	bgt	a4,a5,.L33
	ld	a5,-72(s0)
	ld	a4,0(a5)
	lw	a5,-52(s0)
	mv	a1,a4
	mv	a0,a5
	call	bit
	mv	s1,a0
	ld	a5,-40(s0)
	ld	a4,0(a5)
	lw	a5,-52(s0)
	mv	a1,a4
	mv	a0,a5
	call	bit
	mv	a5,a0
	beq	s1,a5,.L34
.L33:
	ld	a5,-80(s0)
	lbu	a5,17(a5)
	sext.w	a4,a5
	ld	a5,-72(s0)
	ld	a5,0(a5)
	mv	a1,a5
	mv	a0,a4
	call	bit
	mv	a5,a0
	beq	a5,zero,.L35
	ld	a5,-80(s0)
	ld	a5,32(a5)
	lw	a4,-52(s0)
	ld	a3,-80(s0)
	mv	a2,a4
	ld	a1,-72(s0)
	mv	a0,a5
	call	insertR
	mv	a4,a0
	ld	a5,-80(s0)
	sd	a4,32(a5)
	j	.L36
.L35:
	ld	a5,-80(s0)
	ld	a5,24(a5)
	lw	a4,-52(s0)
	ld	a3,-80(s0)
	mv	a2,a4
	ld	a1,-72(s0)
	mv	a0,a5
	call	insertR
	mv	a4,a0
	ld	a5,-80(s0)
	sd	a4,24(a5)
.L36:
	ld	a5,-72(s0)
.L19:
	mv	a0,a5
	ld	ra,72(sp)
	ld	s0,64(sp)
	ld	s1,56(sp)
	addi	sp,sp,80
	jr	ra
	.size	pat_insert, .-pat_insert
	.align	1
	.globl	pat_remove
	.type	pat_remove, @function
pat_remove:
	addi	sp,sp,-96
	sd	ra,88(sp)
	sd	s0,80(sp)
	addi	s0,sp,96
	sd	a0,-88(s0)
	sd	a1,-96(s0)
	ld	a5,-88(s0)
	beq	a5,zero,.L38
	ld	a5,-88(s0)
	ld	a5,8(a5)
	beq	a5,zero,.L38
	ld	a5,-40(s0)
	bne	a5,zero,.L39
.L38:
	li	a5,0
	j	.L40
.L39:
	ld	a5,-96(s0)
	sd	a5,-40(s0)
	ld	a5,-40(s0)
	sd	a5,-24(s0)
	ld	a5,-24(s0)
	sd	a5,-64(s0)
.L43:
	ld	a5,-40(s0)
	lbu	a5,17(a5)
	sw	a5,-52(s0)
	ld	a5,-24(s0)
	sd	a5,-64(s0)
	ld	a5,-40(s0)
	sd	a5,-24(s0)
	ld	a5,-40(s0)
	lbu	a5,17(a5)
	sext.w	a4,a5
	ld	a5,-88(s0)
	ld	a5,0(a5)
	mv	a1,a5
	mv	a0,a4
	call	bit
	mv	a5,a0
	beq	a5,zero,.L41
	ld	a5,-40(s0)
	ld	a5,32(a5)
	j	.L42
.L41:
	ld	a5,-40(s0)
	ld	a5,24(a5)
.L42:
	sd	a5,-40(s0)
	ld	a5,-40(s0)
	lbu	a5,17(a5)
	sext.w	a4,a5
	lw	a5,-52(s0)
	sext.w	a5,a5
	blt	a5,a4,.L43
	ld	a5,-40(s0)
	ld	a4,0(a5)
	ld	a5,-88(s0)
	ld	a5,0(a5)
	beq	a4,a5,.L44
	li	a5,0
	j	.L40
.L44:
	ld	a5,-40(s0)
	lbu	a5,16(a5)
	mv	a4,a5
	li	a5,1
	bne	a4,a5,.L45
	ld	a5,-40(s0)
	lbu	a5,17(a5)
	bne	a5,zero,.L46
	li	a5,0
	j	.L40
.L46:
	ld	a5,-40(s0)
	ld	a5,8(a5)
	ld	a4,0(a5)
	ld	a5,-88(s0)
	ld	a5,8(a5)
	ld	a5,0(a5)
	beq	a4,a5,.L47
	li	a5,0
	j	.L40
.L47:
	ld	a5,-24(s0)
	sd	a5,-32(s0)
	ld	a5,-32(s0)
	sd	a5,-80(s0)
.L50:
	ld	a5,-32(s0)
	lbu	a5,17(a5)
	sw	a5,-52(s0)
	ld	a5,-32(s0)
	sd	a5,-80(s0)
	ld	a5,-32(s0)
	lbu	a5,17(a5)
	sext.w	a4,a5
	ld	a5,-24(s0)
	ld	a5,0(a5)
	mv	a1,a5
	mv	a0,a4
	call	bit
	mv	a5,a0
	beq	a5,zero,.L48
	ld	a5,-32(s0)
	ld	a5,32(a5)
	j	.L49
.L48:
	ld	a5,-32(s0)
	ld	a5,24(a5)
.L49:
	sd	a5,-32(s0)
	ld	a5,-32(s0)
	lbu	a5,17(a5)
	sext.w	a4,a5
	lw	a5,-52(s0)
	sext.w	a5,a5
	blt	a5,a4,.L50
	ld	a5,-80(s0)
	lbu	a5,17(a5)
	sext.w	a4,a5
	ld	a5,-24(s0)
	ld	a5,0(a5)
	mv	a1,a5
	mv	a0,a4
	call	bit
	mv	a5,a0
	beq	a5,zero,.L51
	ld	a5,-80(s0)
	ld	a4,-40(s0)
	sd	a4,32(a5)
	j	.L52
.L51:
	ld	a5,-80(s0)
	ld	a4,-40(s0)
	sd	a4,24(a5)
.L52:
	ld	a5,-64(s0)
	lbu	a5,17(a5)
	sext.w	a4,a5
	ld	a5,-88(s0)
	ld	a5,0(a5)
	mv	a1,a5
	mv	a0,a4
	call	bit
	mv	a5,a0
	beq	a5,zero,.L53
	ld	a5,-24(s0)
	lbu	a5,17(a5)
	sext.w	a4,a5
	ld	a5,-88(s0)
	ld	a5,0(a5)
	mv	a1,a5
	mv	a0,a4
	call	bit
	mv	a5,a0
	beq	a5,zero,.L54
	ld	a5,-24(s0)
	ld	a5,24(a5)
	j	.L55
.L54:
	ld	a5,-24(s0)
	ld	a5,32(a5)
.L55:
	ld	a4,-64(s0)
	sd	a5,32(a4)
	j	.L56
.L53:
	ld	a5,-24(s0)
	lbu	a5,17(a5)
	sext.w	a4,a5
	ld	a5,-88(s0)
	ld	a5,0(a5)
	mv	a1,a5
	mv	a0,a4
	call	bit
	mv	a5,a0
	beq	a5,zero,.L57
	ld	a5,-24(s0)
	ld	a5,24(a5)
	j	.L58
.L57:
	ld	a5,-24(s0)
	ld	a5,32(a5)
.L58:
	ld	a4,-64(s0)
	sd	a5,24(a4)
.L56:
	ld	a5,-40(s0)
	ld	a5,8(a5)
	ld	a5,8(a5)
	beq	a5,zero,.L59
	ld	a5,-40(s0)
	ld	a5,8(a5)
	ld	a5,8(a5)
	mv	a0,a5
	call	free
.L59:
	ld	a5,-40(s0)
	ld	a5,8(a5)
	mv	a0,a5
	call	free
	ld	a4,-40(s0)
	ld	a5,-24(s0)
	beq	a4,a5,.L60
	ld	a5,-24(s0)
	ld	a4,0(a5)
	ld	a5,-40(s0)
	sd	a4,0(a5)
	ld	a5,-24(s0)
	ld	a4,8(a5)
	ld	a5,-40(s0)
	sd	a4,8(a5)
	ld	a5,-24(s0)
	lbu	a4,16(a5)
	ld	a5,-40(s0)
	sb	a4,16(a5)
.L60:
	ld	a0,-24(s0)
	call	free
	li	a5,1
	j	.L40
.L45:
	sw	zero,-52(s0)
	j	.L61
.L64:
	ld	a5,-88(s0)
	ld	a5,8(a5)
	ld	a4,0(a5)
	ld	a5,-40(s0)
	ld	a3,8(a5)
	lw	a5,-52(s0)
	slli	a5,a5,4
	add	a5,a3,a5
	ld	a5,0(a5)
	beq	a4,a5,.L69
	lw	a5,-52(s0)
	addiw	a5,a5,1
	sw	a5,-52(s0)
.L61:
	ld	a5,-40(s0)
	lbu	a5,16(a5)
	sext.w	a4,a5
	lw	a5,-52(s0)
	sext.w	a5,a5
	blt	a5,a4,.L64
	j	.L63
.L69:
	nop
.L63:
	ld	a5,-40(s0)
	lbu	a5,16(a5)
	sext.w	a4,a5
	lw	a5,-52(s0)
	sext.w	a5,a5
	blt	a5,a4,.L65
	li	a5,0
	j	.L40
.L65:
	ld	a5,-40(s0)
	lbu	a5,16(a5)
	sext.w	a5,a5
	addiw	a5,a5,-1
	sext.w	a5,a5
	slli	a5,a5,4
	mv	a0,a5
	call	malloc
	mv	a5,a0
	sd	a5,-72(s0)
	sw	zero,-52(s0)
	ld	a5,-72(s0)
	sd	a5,-48(s0)
	j	.L66
.L68:
	ld	a5,-88(s0)
	ld	a5,8(a5)
	ld	a4,0(a5)
	ld	a5,-40(s0)
	ld	a3,8(a5)
	lw	a5,-52(s0)
	slli	a5,a5,4
	add	a5,a3,a5
	ld	a5,0(a5)
	beq	a4,a5,.L67
	ld	a5,-40(s0)
	ld	a4,8(a5)
	lw	a5,-52(s0)
	slli	a5,a5,4
	add	a3,a4,a5
	ld	a5,-48(s0)
	addi	a4,a5,16
	sd	a4,-48(s0)
	li	a2,16
	mv	a1,a3
	mv	a0,a5
	call	memmove
.L67:
	lw	a5,-52(s0)
	addiw	a5,a5,1
	sw	a5,-52(s0)
.L66:
	ld	a5,-40(s0)
	lbu	a5,16(a5)
	sext.w	a4,a5
	lw	a5,-52(s0)
	sext.w	a5,a5
	blt	a5,a4,.L68
	ld	a5,-40(s0)
	lbu	a5,16(a5)
	addiw	a5,a5,-1
	andi	a4,a5,255
	ld	a5,-40(s0)
	sb	a4,16(a5)
	ld	a5,-40(s0)
	ld	a5,8(a5)
	mv	a0,a5
	call	free
	ld	a5,-40(s0)
	ld	a4,-72(s0)
	sd	a4,8(a5)
	li	a5,1
.L40:
	mv	a0,a5
	ld	ra,88(sp)
	ld	s0,80(sp)
	addi	sp,sp,96
	jr	ra
	.size	pat_remove, .-pat_remove
	.align	1
	.globl	pat_search
	.type	pat_search, @function
pat_search:
	addi	sp,sp,-64
	sd	ra,56(sp)
	sd	s0,48(sp)
	addi	s0,sp,64
	sd	a0,-56(s0)
	sd	a1,-64(s0)
	sd	zero,-24(s0)
	ld	a5,-64(s0)
	sd	a5,-32(s0)
	ld	a5,-32(s0)
	bne	a5,zero,.L71
	li	a5,0
	j	.L72
.L71:
	ld	a5,-32(s0)
	ld	a4,0(a5)
	ld	a5,-32(s0)
	ld	a5,8(a5)
	ld	a3,0(a5)
	ld	a5,-56(s0)
	and	a5,a3,a5
	bne	a4,a5,.L73
	ld	a5,-32(s0)
	sd	a5,-24(s0)
.L73:
	ld	a5,-32(s0)
	lbu	a5,17(a5)
	sw	a5,-36(s0)
	ld	a5,-32(s0)
	lbu	a5,17(a5)
	sext.w	a5,a5
	ld	a1,-56(s0)
	mv	a0,a5
	call	bit
	mv	a5,a0
	beq	a5,zero,.L74
	ld	a5,-32(s0)
	ld	a5,32(a5)
	j	.L75
.L74:
	ld	a5,-32(s0)
	ld	a5,24(a5)
.L75:
	sd	a5,-32(s0)
	ld	a5,-32(s0)
	lbu	a5,17(a5)
	sext.w	a4,a5
	lw	a5,-36(s0)
	sext.w	a5,a5
	blt	a5,a4,.L71
	ld	a5,-32(s0)
	ld	a4,0(a5)
	ld	a5,-32(s0)
	ld	a5,8(a5)
	ld	a3,0(a5)
	ld	a5,-56(s0)
	and	a5,a3,a5
	bne	a4,a5,.L76
	ld	a5,-32(s0)
	j	.L72
.L76:
	ld	a5,-24(s0)
.L72:
	mv	a0,a5
	ld	ra,56(sp)
	ld	s0,48(sp)
	addi	sp,sp,64
	jr	ra
	.size	pat_search, .-pat_search
	.ident	"GCC:, (GNU), 9.2.0"
