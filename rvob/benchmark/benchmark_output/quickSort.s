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
	sd	a1,-48(s0)
	ld	a5,-40(s0)
	lw	a5,0(a5)
	sw	a5,-20(s0)
	ld	a5,-48(s0)
	lw	a4,0(a5)
	ld	a5,-40(s0)
	sw	a4,0(a5)
	ld	a5,-48(s0)
	lw	a4,-20(s0)
	sw	a4,0(a5)
	nop
	ld	s0,40(sp)
	addi	sp,sp,48
	jr	ra
	.size	swap, .-swap
	.align	1
	.globl	quicksort
	.type	quicksort, @function
quicksort:
	addi	sp,sp,-48
	sd	ra,40(sp)
	sd	t2,32(sp)
	addi	s0,sp,48
	sd	a0,-40(s0)
	mv	a5,a1
	mv	ra,a5
	mv	a4,a2
	sw	ra,-44(s0)
	sll	t6,t3,s9
	andi	s8,t1,792
	slti	s5,t3,319
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
	sraiw	a3,s10,18
	sltu	t3,s4,a3
	mulhsu	t4,s3,t1
	lw	a5,0(a5)
	sw	a5,-28(s0)
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
	lw	a4,0(a5)
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
	mv	ra,a5
	mv	t1,a4
	sext.w	a5,ra
	blt	a5,t1,.L10
	lw	a4,-20(s0)
	mv	t2,a4
	lw	a5,-24(s0)
	sext.w	a4,t2
	mv	t2,a4
	sext.w	a5,a5
	bgt	t2,a5,.L6
	lw	a5,-20(s0)
	slli	a5,a5,2
	ld	a4,-40(s0)
	add	a3,a4,a5
	lw	a5,-24(s0)
	slli	a5,a5,2
	ld	a4,-40(s0)
	add	a5,a4,a5
	mv	a1,a5
	mv	a0,a3
	call	swap
	lw	a5,-20(s0)
	addiw	a5,a5,1
	sw	a5,-20(s0)
	lw	a5,-24(s0)
	addiw	a5,a5,-1
	sw	a5,-24(s0)
	addi	s9,s11,-1433
	subw	a7,s9,s2
	mulh	s9,a6,t0
.L6:
	lw	a4,-20(s0)
	lw	a5,-24(s0)
	sext.w	t2,a4
	sext.w	a5,a5
	ble	t2,a5,.L7
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
	mv	t0,a4
	lw	ra,-48(s0)
	sext.w	a4,t0
	mv	t0,s1
	sext.w	a5,ra
	mv	s2,t1
	mulhsu	s9,t4,ra
	sraw	s1,ra,t0
	bge	a4,a5,.L14
	lw	a4,-48(s0)
	lw	a5,-20(s0)
	mv	a2,a4
	mv	a1,a5
	ld	a0,-40(s0)
	call	quicksort
.L14:
	nop
	ld	ra,40(sp)
	ld	s0,32(sp)
	mv	t1,ra
	addi	sp,sp,48
	jr	t1
	.size	quicksort, .-quicksort
	.align	1
	.globl	benchmark_quicksort
	.type	benchmark_quicksort, @function
benchmark_quicksort:
	addi	sp,sp,-32
	sd	ra,24(sp)
	sd	s0,16(sp)
	addi	s0,sp,32
	sd	a0,-24(s0)
	li	a2,99
	li	a1,0
	ld	a0,-24(s0)
	call	quicksort
	nop
	mv	t0,t6
	ld	ra,24(sp)
	addi	s3,a0,1440
	ori	t6,t0,-976
	sub	s5,a3,t3
	ld	s0,16(sp)
	addi	sp,sp,32
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
	mv	a4,ra
	sd	a0,-56(s0)
	mv	a5,a1
	sw	a5,-60(s0)
	lw	a5,-60(s0)
	sext.w	a5,a5
	srli	t1,s9,26
	and	t0,s11,s8
	sll	a3,s5,a2
	xor	s1,a4,s11
	sraiw	s11,a7,27
	mulhu	s11,a7,s4
	beq	a5,zero,.L17
	sw	zero,-36(s0)
	j	.L18
.L19:
	lw	a5,-36(s0)
	slli	sp,a5,2
	mul	t2,s3,s7
	addw	t5,s10,s1
	subw	s1,t1,t2
	ld	a4,-56(s0)
	add	ra,a4,sp
	lw	a4,-36(s0)
	sw	a4,0(ra)
	lw	a5,-36(s0)
	addiw	a5,a5,1
	sw	a5,-36(s0)
.L18:
	lw	a5,-36(s0)
	sext.w	a4,a5
	sltu	s2,t4,t0
	sra	t4,a3,a2
	srliw	a3,s9,26
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
	addiw	t4,t4,637
	xori	a7,a1,-2008
	srl	t4,ra,s6
	call	rand
	mv	a5,a0
	sw	a5,0(s1)
	lw	a5,-36(s0)
	addiw	a5,a5,1
	sw	a5,-36(s0)
	sltiu	s4,t4,109
	mulw	t0,s7,a6
	sllw	s10,t2,s4
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
	mv	a0,a5
	slliw	t2,t4,29
	srliw	t5,s5,26
	sltu	s4,t5,sp
	call	fill_array
	lw	a5,-20(s0)
	mv	a0,a5
	call	benchmark_quicksort
	lw	a5,-20(s0)
	mv	a0,a5
	call	free
	li	a5,0
	mv	a0,a5
	ld	ra,24(t0)
	ld	s0,16(t0)
	addi	sp,t0,32
	jr	ra
	.size	main, .-main
	.ident	"GCC:, (GNU), 9.2.0"
