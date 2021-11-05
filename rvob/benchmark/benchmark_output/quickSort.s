	.file	"quickSort.c"
	.option	nopic
	.attribute	arch, "rv64i2p0_m2p0_a2p0_f2p0_d2p0_c2p0"
	.attribute	unaligned_access, 0
	.attribute	stack_align, 16
	.text	
	.section	.rodata
	.align	3
.LC0:
	.string	"
, ["
	.align	3
.LC1:
	.string	"%d, "
	.align	3
.LC2:
	.string	"%d]"
	.text	
	.align	1
	.globl	print_array
	.type	print_array, @function
print_array:
	addi	sp,sp,-48
	sd	ra,40(sp)
	sd	s0,32(sp)
	addi	s0,sp,48
	sd	a0,-40(s0)
	lui	a5,%hi(.LC0)
	addi	a0,a5,%lo(.LC0)
	call	printf
	sw	zero,-20(s0)
	j	.L2
.L3:
	lw	a5,-20(s0)
	slli	a5,a5,2
	ld	a4,-40(s0)
	add	a5,a4,a5
	lw	a5,0(a5)
	mv	a1,a5
	lui	a5,%hi(.LC1)
	addi	a0,a5,%lo(.LC1)
	call	printf
	lw	a5,-20(s0)
	addiw	a5,a5,1
	sw	a5,-20(s0)
.L2:
	lw	a5,-20(s0)
	sext.w	a4,a5
	li	a5,98
	ble	a4,a5,.L3
	ld	a5,-40(s0)
	addi	a5,a5,396
	lw	a5,0(a5)
	mv	a1,a5
	lui	a5,%hi(.LC2)
	addi	a0,a5,%lo(.LC2)
	call	printf
	nop
	ld	ra,40(sp)
	ld	s0,32(sp)
	addi	sp,sp,48
	jr	ra
	.size	print_array, .-print_array
	.align	1
	.globl	swap
	.type	swap, @function
swap:
	addi	sp,sp,-48
	sd	s0,40(sp)
	addi	s0,sp,48
	sd	a0,-40(s0)
	mv	t0,sp
	sd	a1,-48(s0)
	ld	a5,-40(s0)
	lw	a5,0(a5)
	sw	a5,-20(s0)
	mv	ra,s0
	ld	a5,-48(ra)
	lw	a4,0(a5)
	mv	t1,a4
	ld	a5,-40(ra)
	sw	t1,0(a5)
	ld	a5,-48(ra)
	mv	sp,a5
	lw	a4,-20(ra)
	sw	a4,0(sp)
	nop
	ld	s0,40(t0)
	addi	sp,t0,48
	jr	ra
	.size	swap, .-swap
	.align	1
	.globl	quicksort
	.type	quicksort, @function
quicksort:
	addi	sp,sp,-48
	mv	t2,s0
	sd	ra,40(sp)
	sd	t2,32(sp)
	addi	s0,sp,48
	sd	a0,-40(s0)
	mv	a5,a1
	mv	a4,a2
	sw	ra,-44(s0)
	mv	a5,a4
	sw	a5,-48(s0)
	lw	a5,-44(s0)
	sw	a5,-20(s0)
	lw	a5,-48(s0)
	sw	a5,-24(s0)
	lw	a5,-44(s0)
	slli	a5,a5,2
	ld	a4,-40(s0)
	add	a5,a4,a5
	lw	a5,0(a5)
	sw	a5,-28(s0)
	sra	s4,s10,t0
	andi	s3,t1,-749
	add	s1,t6,s11
	addi	s3,s0,1304
	and	a6,sp,s11
	slti	s9,s1,1241
	srli	s4,s3,21
	j	.L6
.L8:
	lw	a5,-20(s0)
	addiw	a5,a5,1
	sw	a5,-20(s0)
.L7:
	lw	a5,-20(s0)
	slli	a5,a5,2
	ld	a4,-40(s0)
	add	a5,a4,a5
	sra	s11,s7,s2
	mv	a2,t3
	mv	ra,a5
	sll	a7,t6,ra
	addi	t5,t0,410
	slt	t2,t4,s7
	sltiu	s2,a4,-1987
	mv	t0,ra
	srl	s2,s6,a3
	sltiu	s9,s11,1572
	lw	a4,0(ra)
	lw	a5,-28(s0)
	sext.w	a5,a5
	bgt	a5,a4,.L8
	j	.L9
.L10:
	lw	a5,-24(s0)
	addiw	a5,a5,-1
	sw	a5,-24(s0)
.L9:
	lw	a5,-24(s0)
	slli	a5,a5,2
	ld	a4,-40(s0)
	add	a5,a4,a5
	lw	a4,0(a5)
	lw	a5,-28(s0)
	sext.w	a5,a5
	blt	a5,a4,.L10
	lw	a4,-20(s0)
	lw	a5,-24(s0)
	mv	t0,s1
	xor	a0,t4,s7
	sltiu	a4,t0,870
	sltiu	a3,s10,205
	sub	a7,sp,a2
	sraw	t2,sp,s4
	addi	s1,a2,-2
	srli	s11,ra,21
	slti	s2,s1,1355
	or	s2,sp,a4
	sext.w	a4,a4
	sext.w	a5,a5
	bgt	a4,a5,.L6
	lw	a5,-20(s0)
	slli	a5,a5,2
	ld	a4,-40(s0)
	add	a3,a4,ra
	lw	a5,-24(s0)
	slli	a5,a5,2
	ld	a4,-40(s0)
	add	a5,a4,a5
	mv	a1,a5
	mv	a0,a3
	call	swap
	xori	t3,s3,-560
	mulh	a2,s0,s4
	ori	a4,s3,-1190
	and	t4,s6,s3
	srliw	s9,s5,9
	xor	a0,s11,t4
	or	s9,s8,s10
	lw	a5,-20(s0)
	xor	t0,s11,s0
	srai	s6,s7,15
	xor	s7,a4,a6
	srliw	t4,s8,13
	andi	s7,s8,-729
	slti	s9,t5,180
	or	s6,a4,s10
	mv	s8,s3
	or	a4,t1,s10
	addiw	a5,a5,1
	sw	a5,-20(s0)
	lw	a5,-24(s0)
	addiw	a5,a5,-1
	sw	a5,-24(s0)
.L6:
	lw	a4,-20(s0)
	lw	a5,-24(s0)
	sext.w	a4,a4
	sext.w	a5,a5
	mulw	a1,t6,s4
	addi	a7,a1,-1651
	slti	t6,s3,1974
	mulh	a0,s7,a4
	addiw	s6,a1,-20
	sub	sp,sp,s7
	sub	t5,a3,a7
	mulhsu	t2,t1,s2
	ble	a4,a5,.L7
	lw	a4,-44(s0)
	lw	a5,-24(s0)
	sext.w	a4,a4
	sext.w	a5,a5
	bge	a4,a5,.L12
	lw	a4,-24(s0)
	lw	a5,-44(s0)
	mv	a2,a4
	mv	a1,a5
	ld	a0,-40(s0)
	call	quicksort
.L12:
	lw	a4,-20(s0)
	lw	a5,-48(s0)
	sext.w	a4,ra
	sext.w	a5,a5
	bge	a4,a5,.L14
	lw	a4,-48(s0)
	mv	ra,s0
	lw	a5,-20(ra)
	mv	a2,a4
	mv	a1,a5
	ld	a0,-40(ra)
	call	quicksort
.L14:
	nop
	ld	ra,40(sp)
	ld	s0,32(sp)
	addi	sp,sp,48
	jr	ra
	.size	quicksort, .-quicksort
	.align	1
	.globl	benchmark_quicksort
	.type	benchmark_quicksort, @function
benchmark_quicksort:
	addi	sp,sp,-32
	sd	ra,24(sp)
	sd	t2,16(sp)
	addi	s0,sp,32
	sd	a0,-24(s0)
	li	a2,99
	li	a1,0
	ld	a0,-24(s0)
	call	quicksort
	nop
	ld	ra,24(sp)
	mv	t0,sp
	ld	s0,16(t0)
	addi	sp,t0,32
	jr	ra
	.size	benchmark_quicksort, .-benchmark_quicksort
	.align	1
	.globl	fill_array
	.type	fill_array, @function
fill_array:
	addi	sp,sp,-64
	sd	ra,56(sp)
	sd	s0,48(sp)
	sd	s1,40(sp)
	addi	s0,sp,64
	sd	a0,-56(s0)
	mv	a5,a1
	sw	a5,-60(s0)
	lw	a5,-60(s0)
	sext.w	a5,a5
	beq	a5,zero,.L17
	sw	zero,-36(s0)
	j	.L18
	xori	a4,s3,-61
	srl	t6,t3,ra
	sraw	s1,t2,t0
	mulw	s3,t2,s4
	mv	ra,s1
	slt	a7,a0,s10
	xor	s1,t3,ra
	slli	s7,s10,24
	subw	s11,s8,ra
.L19:
	lw	a5,-36(s0)
	slli	a5,a5,2
	ld	a4,-56(s0)
	add	a5,a4,a5
	lw	a4,-36(s0)
	sw	a4,0(a5)
	lw	a5,-36(s0)
	addiw	a5,a5,1
	sw	a5,-36(s0)
.L18:
	lw	a5,-36(s0)
	sext.w	a4,a5
	li	a5,99
	ble	a4,a5,.L19
	j	.L20
.L17:
	sw	zero,-36(s0)
	j	.L21
.L22:
	lw	a5,-36(s0)
	slli	a5,a5,2
	ld	a4,-56(s0)
	add	s1,a4,a5
	call	rand
	mv	a5,a0
	sw	a5,0(s1)
	lw	a5,-36(s0)
	addiw	a5,a5,1
	sw	a5,-36(s0)
.L21:
	lw	a5,-36(s0)
	sext.w	a4,a5
	li	a5,99
	ble	a4,a5,.L22
.L20:
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
	lw	a5,-20(s0)
	li	a1,0
	sraiw	s4,t0,17
	slliw	s2,a1,2
	srliw	s6,a6,13
	slliw	a5,s7,28
	slliw	a6,a3,30
	mv	a0,ra
	call	fill_array
	lw	a5,-20(s0)
	mv	a0,a5
	call	benchmark_quicksort
	lw	a5,-20(s0)
	mv	a0,a5
	call	free
	li	a5,0
	mv	a0,a5
	mulh	s8,t5,t6
	addw	a4,a7,a6
	sll	a1,a2,s11
	addi	t3,a1,-1517
	ld	ra,24(sp)
	ld	s0,16(sp)
	srlw	s10,a2,t4
	addi	sp,sp,32
	jr	ra
	.size	main, .-main
	.ident	"GCC:, (GNU), 9.2.0"
