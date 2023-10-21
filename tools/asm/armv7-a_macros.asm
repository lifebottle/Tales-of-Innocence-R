; ###############################################################
;    ARMv7-A Thumb-2 macros for ARMIPS | encodings taken from:
;
;  ARM® Architecture Reference Manual ARMv7-A and ARMv7-R edition
;   https://developer.arm.com/documentation/ddi0406/cd/?lang=en
; ###############################################################

; Also check "Appendix D8 Legacy Instruction Mnemonics"
; for UAL related changes


;################################
;
;       Some misc functions
;
;################################

.expfunc getbyte(value, n), ((value >> (8 * (n - 1))) & 0xff)
.expfunc getoff(src_addr, dst_addr), ((dst_addr & (~1)) - (src_addr & (~1)) - 4)
.expfunc swaphw(w), (w >> 16 | w << 16)
.expfunc clz(x), x == 0 ? 32 : clz_1(x, 0xFFFF0000, 32)

.expfunc clz_1(x, val, k),\
    (k == 0) ? \ 
        0 \
    : \
        ((x & val) == 0) ? (\
            (k >> 1) + clz_1((x << (k >> 1)), (val << (k >> 2)), (k >> 1)) \
        )\
        : (\
            0 + clz_1(x, (val << (k >> 2)), (k >> 1))\
        )

.expfunc ctz(x), x == 0 ? 32 : ctz_1(x, 0x0000FFFF, 32)

.expfunc ctz_1(x, val, k), \
    (k == 0) ? (\ 
        0 \
    )\
    : (\
        ((x & val) == 0) ? (\
            (k >> 1) + ctz_1((x >> (k >> 1)), (val >> (k >> 2)), (k >> 1)) \
        )\
        : (\
            0 + ctz_1(x, (val >> (k >> 2)), (k >> 1))\
        )\
    )


;################################
;
;       Labels
;
;################################

; For less akward macro writing I
; globally define labels with the
; same names as the register
; (which apparently is valid?)
; so we can refer to them the same
; was as a normal instruction
; No such thing for # and [] because
; there's no token level parsing
; only text replacements and some
; string manipulation

.definelabel r0, 0
.definelabel r1, 1
.definelabel r2, 2
.definelabel r3, 3
.definelabel r4, 4
.definelabel r5, 5
.definelabel r6, 6
.definelabel r7, 7
.definelabel r8, 8
.definelabel r9, 9
.definelabel r10, 10
.definelabel r11, 11
.definelabel r12, 12

.definelabel r13, 13
.definelabel r14, 14
.definelabel r15, 15

.definelabel sp, 13
.definelabel lr, 14
.definelabel pc, 15 

;################################
;
;         B instructions
;   Check A8.8.18 in the manual
;
;################################

; encoding T3
.macro b.w,dst_addr
    ; Not on Thumb mode, bail out!
    .if isthumb() != 1
        .error "b.w T4 encoding error: Not on thumb mode!"
    .endif

    ; This is the T4 encoding of this instruction, 
    ; so jumps are limited to –16777216 to 16777214 even jumps
    .if getoff(., dst_addr) > 16777214 || getoff(., dst_addr) < -16777216
        .error "b.w T4 encoding error: label out of range"
    .endif

    ; the half words are swapped because it's in Thumb mode
    ; also, not having variables makes this a clusterfuck
    .word swaphw(\
            /* Top bits */ (0b11110 << 27) | \
            /* Sign */ ((getoff(., dst_addr) < 0 ? 1 : 0) << 26) | \
            /* Imm10 */ (((getoff(., dst_addr) >> 12) & 0b1111111111) << 16) | \
            /* 1 */ (1 << 15) | \
            /* J1 */ ((((~(((getoff(., dst_addr) & (1 << 23)) ? 1 : 0) & 1) ^ (getoff(., dst_addr) < 0)) & 1)) << 13) |\
            /* 1 */ (1 << 12) | \
            /* J2 */ ((((~((getoff(., dst_addr) & (1 << 22) ? 1 : 0) & 1) ^ (getoff(., dst_addr) < 0)) & 1)) << 11) | \
            /* Imm11 */ (((getoff(., dst_addr) >> 1) & 0b11111111111))\
           )
.endmacro

; encoding T3
.macro bne.w,dst_addr
    ; Not on Thumb mode, bail out!
    .if isthumb() != 1
        .error "bne.w T3 encoding error: Not on thumb mode!"
    .endif

    ; This is the T3 encoding of this instruction, 
    ; so jumps are limited to -1048576 to 1048574 even jumps
    .if getoff(., dst_addr) > 1048574 || getoff(., dst_addr) < -1048576
        .error "bne.w T3 encoding error: label out of range"
    .endif

    ; the half words are swapped because it's in Thumb mode
    ; also, not having variables makes this a clusterfuck
    .word swaphw(\
            /* Top bits */ (0b11110 << 27) | \
            /* Sign */ ((getoff(., dst_addr) < 0 ? 1 : 0) << 26) | \
            /* cond */ (0b0001 << 22)|\ /* NE */
            /* Imm6 */ (((getoff(., dst_addr) >> 12) & 0b111111) << 16) | \
            /* 1 */ (1 << 15) | \
            /* J1 */ ((((~(((getoff(., dst_addr) & (1 << 23)) ? 1 : 0) & 1) ^ (getoff(., dst_addr) < 0)) & 1)) << 13) |\
            /* 1 */ (0 << 12) | \ /* T3 encoding */
            /* J2 */ ((((~((getoff(., dst_addr) & (1 << 22) ? 1 : 0) & 1) ^ (getoff(., dst_addr) < 0)) & 1)) << 11) | \
            /* Imm11 */ (((getoff(., dst_addr) >> 1) & 0b11111111111))\
           )
.endmacro

;################################
;
;         MOV instructions
;   Check A8.8.103 in the manual
;
;################################

; add T1 encoding, encodes an <Imm8>
.macro movs,rd,val
    ; According to D8.1 this should be the same
    ; as mov rd,val in ARMv6k (3DS) and ARMv4T (GBA)
    ; so just pop that in
    mov rd,val
.endmacro

; mov T2 encoding, encodes a <const>
; ranges defined by A6.3.2 section of the manual
.macro mov.w,rd,val
    .ifndef r3
        .error "!"
    .endif
    ; Not on Thumb mode, bail out!
    .if isthumb() != 1
        .error "mov.w T2 encoding error: Not on thumb mode!"
    .endif

    ; As per the manual, can only address the first 13 GPR
    ; not that you could write "SP" or "LR" in a macro...
    .if rd < 0 || rd > 13
        .warning "movw T2 encoding warning: Invalid target register, bahavior is UNPREDICTABLE"
    .endif

    ; I won't even bother with rotated values if I can help it
    .if val > 0xFF
        .error "mov.w T2 encoding error: Currently only 0-255 values are supported"
    .endif

    ; the half words are swapped because it's in Thumb mode
    ; Top bits are just saying "Yep, this is a thumb instruction"
    ; i = 0, we only encode 0xFF bytes
    ; S = 0, this is mov.w not movs.w
    ; Imm3 = 0, we only encode 0xFF bytes
    .word swaphw(\
            /* Top bits */ (0b11110 << 27) | \
            /* i */ (0 << 26) | \
            /* st1 */ (0b00010 << 21) | \
            /* S */ (0 << 20) | \
            /* st2 */ (0b11110 << 15) |\
            /* Imm3 */ (0b000 << 12) | \
            /* Rd */ ((rd & 0xF) << 8) | \
            /* Imm8 */ (val & 0b11111111)\
           )
.endmacro


; mov T2 encoding, encodes a <const>
; ranges defined by A6.3.2?? section of the manual
.macro movs.w,rd,val
    ; Not on Thumb mode, bail out!
    .if isthumb() != 1
        .error "movs.w T2 encoding error: Not on thumb mode!"
    .endif

    ; As per the manual, can only address the first 13 GPR
    ; not that you could write "SP" or "LR" in a macro...
    .if rd < 0 || rd == 13 || rd == 15
        .warning "movs.w T2 encoding warning: Invalid target register, bahavior is UNPREDICTABLE"
    .endif

    .if val <= 0xFF || val == 0
        ; the half words are swapped because it's in Thumb mode
        ; Top bits are just saying "Yep, this is a thumb instruction"
        ; i = 0, we only encode 0xFF bytes
        ; S = 1, this is movs.w not mov.w
        ; Imm3 = 0, we only encode 0xFF bytes
        .word swaphw(\
            /* Top bits */ (0b11110 << 27) | \
            /* i */ (0 << 26) | \
            /* st1 */ (0b00010 << 21) | \
            /* S */ (1 << 20) | \
            /* st2 */ (0b11110 << 15) |\
            /* Imm3 */ (0b000 << 12) | \
            /* Rd */ ((rd & 0xF) << 8) | \
            /* Imm8 */ (val & 0b11111111)\
        )
    .elseif val == (((val & 0xFF) << 16) | (val & 0xFF))
        .word swaphw(\
            /* Top bits */ (0b11110 << 27) | \
            /* i */ (0 << 26) | \
            /* st1 */ (0b00010 << 21) | \
            /* S */ (1 << 20) | \
            /* st2 */ (0b11110 << 15) |\
            /* Imm3 */ (0b001 << 12) | \
            /* Rd */ ((rd & 0xF) << 8) | \
            /* Imm8 */ (val & 0b11111111)\
        )
    .elseif val == (((val & 0xFF) << 24) | ((val & 0xFF) << 8))
        .word swaphw(\
            /* Top bits */ (0b11110 << 27) | \
            /* i */ (0 << 26) | \
            /* st1 */ (0b00010 << 21) | \
            /* S */ (1 << 20) | \
            /* st2 */ (0b11110 << 15) |\
            /* Imm3 */ (0b010 << 12) | \
            /* Rd */ ((rd & 0xF) << 8) | \
            /* Imm8 */ (val & 0b11111111)\
        )
    .elseif val == (((val & 0xFF) << 24) | ((val & 0xFF) << 16) | ((val & 0xFF) << 8) | (val & 0xff))
        .word swaphw(\
            /* Top bits */ (0b11110 << 27) | \
            /* i */ (0 << 26) | \
            /* st1 */ (0b00010 << 21) | \
            /* S */ (1 << 20) | \
            /* st2 */ (0b11110 << 15) |\
            /* Imm3 */ (0b011 << 12) | \
            /* Rd */ ((rd & 0xF) << 8) | \
            /* Imm8 */ (val & 0b11111111)\
        )
    .elseif (32 - abs(clz(val) + ctz(val))) <= 8
        .word swaphw(\
            /* Top bits */ (0b11110 << 27) | \
            /* i */ (((clz(val) >> 4) & 0b1) << 26) | \
            /* st1 */ (0b00010 << 21) | \
            /* S */ (1 << 20) | \
            /* st2 */ (0b11110 << 15) |\
            /* Imm3 */ (((0b100 + (clz(val) >> 1)) & 0b111) << 12) | \
            /* Rd */ ((rd & 0xF) << 8) | \
            /* A */ (((clz(val) % 2) & 0b1) << 7) | \
            /* Imm8 */ (((val >> ctz(val)) << (8 - (32 - abs(clz(val) + ctz(val))))) & 0b1111111)\
        )
    .else
        .error "Can't encode constant for movs.w"
    .endif

    
.endmacro

; movw T3 encoding, encodes an <Imm16>
.macro movw,rd,val
    ; Not on Thumb mode, bail out!
    .if isthumb() != 1
        .error "movw T3 encoding error: Not on thumb mode!"
    .endif

    ; As per the manual, can only address the first 13 GPR
    ; not that you could write "SP" or "AL" in a macro...
    .if rd < 0 || rd > 13
        .warning "movw T3 encoding warning: Invalid target register, bahavior is UNPREDICTABLE"
    .endif

    ; the half words are swapped because it's in Thumb mode
    ; the Imm16 is encoded as | Imm4 : i : Imm3 : Imm8 |
    .word swaphw(\
            /* Top bits */ (0b11110 << 27) | \
            /* i */ (((val >> 11) & 0b1) << 26) | \
            /* st1 */ (0b100100 << 20) | \
            /* Imm4 */ (((val >> 12) & 0b1111) << 16) |\
            /* st2 */ (0b0 << 15) |\
            /* Imm3 */ (((val >> 8) & 0b111) << 12) | \
            /* Rd */ ((rd & 0xF) << 8) | \
            /* Imm8 */ (val & 0xFF)\
           )
.endmacro

;################################
;
;         ADD instructions
;    Check A8.8.4 in the manual
;
;################################

; add T2 encoding, encodes an <Imm8>
.macro adds,rd,val
    ; According to D8.1 this should be the same
    ; as add rd,val in ARMv6k (3DS) and ARMv4T (GBA)
    ; so just pop that in
    add rd,val
.endmacro

; add T3 encoding, encodes a <const>
; ranges defined by A6.3.2 section of the manual
.macro add.w,rd,rn,val
    ; Not on Thumb mode, bail out!
    .if isthumb() != 1
        .error "add.w T3 encoding error: Not on thumb mode!"
    .endif

    ; As per the manual, can only address the first 13 GPR
    ; not that you could write "SP" or "LR" in a macro...
    .if rd == 13 || rn == 15 || rd == 15
        .warning "add.w T3 encoding warning: Invalid source or target register, bahavior is UNPREDICTABLE"
    .endif

    ; I won't even bother with rotated values if I can help it
    .if val > 0xFF
        .error "add.w T3 encoding error: Currently only 0-255 values are supported"
    .endif

    ; the half words are swapped because it's in Thumb mode
    ; Top bits are just saying "Yep, this is a thumb instruction"
    ; i = 0, we only encode 0xFF bytes
    ; S = 0, this is add.w not adds.w
    ; Imm3 = 0, we only encode 0xFF bytes
    .word swaphw(\
            /* Top bits */ (0b11110 << 27) | \
            /* i */ (0 << 26) | \
            /* st1 */ (0b01000 << 21) | \
            /* S */ (0 << 20) | \
            /* Rn */ ((rn & 0xF) << 16) | \
            /* st2 */ (0b0 << 15) |\
            /* Imm3 */ (0b000 << 12) | \
            /* Rd */ ((rd & 0xF) << 8) | \
            /* Imm8 */ (val & 0b11111111)\
           )
.endmacro

; add T4 encoding, encodes an <Imm12>
; ranges defined by A8.8.4 section of the manual
.macro addw,rd,rn,val
    ; Not on Thumb mode, bail out!
    .if isthumb() != 1
        .error "add.w T4 encoding error: Not on thumb mode!"
    .endif

    ; As per the manual, can only address the first 13 GPR
    ; not that you could write "SP" or "LR" in a macro...
    .if rd == 13 || rn == 15 || rd == 15
        .warning "add.w T4 encoding warning: Invalid source or target register, bahavior is UNPREDICTABLE"
    .endif

    ; the half words are swapped because it's in Thumb mode
    ; Top bits are just saying "Yep, this is a thumb instruction"
    ; i = 0, we only encode 0xFF bytes
    ; S = 0, this is add.w not adds.w
    ; Imm3 = 0, we only encode 0xFF bytes
    .word swaphw(\
            /* Top bits */ (0b11110 << 27) | \
            /* i */ (((val >> 11) & 0b00001) << 26) | \
            /* st1 */ (0b10000 << 21) | \
            /* S */ (0 << 20) | \
            /* Rn */ ((rn & 0xF) << 16) | \
            /* st2 */ (0b0 << 15) |\
            /* Imm3 */ (((val >> 8) & 0b111) << 12) | \
            /* Rd */ ((rd & 0xF) << 8) | \
            /* Imm8 */ (val & 0b11111111)\
           )
.endmacro


;################################
;
;         STR instructions
;    Check A8.8 in the manual
;
;################################

; STR Check A8.8.204

; str T3 encoding, encodes an <Imm12>
.macro str.w,rt,rn,val
    ; Not on Thumb mode, bail out!
    .if isthumb() != 1
        .error "str.w T3 encoding error: Not on thumb mode!"
    .endif

    ; As per the manual, can only address the first 13 GPR
    ; not that you could write "SP" or "LR" in a macro...
    .if rt == 15
        .warning "str.w T3 encoding warning: Invalid target register, bahavior is UNPREDICTABLE"
    .endif

    ; the half words are swapped because it's in Thumb mode
    ; Top bits are just saying "Yep, this is a thumb instruction"
    ; i = 0, we only encode 0xFF bytes
    ; S = 0, this is add.w not adds.w
    ; Imm3 = 0, we only encode 0xFF bytes
    .word swaphw(\
            /* Top bits */ (0b11111 << 27) | \
            /* st1 */ (0b0001100 << 20) | \
            /* Rn */ ((rn & 0xF) << 16) | \
            /* Rt */ ((rt & 0xF) << 12) | \
            /* Imm12 */ (val & 0b111111111111) \
           )
.endmacro

; STRH Check A8.8.217

; str T3 encoding, encodes an <Imm12> BROKEN
.macro strh.w,rt,rn,val
    ; Not on Thumb mode, bail out!
    .if isthumb() != 1
        .error "str.w T3 encoding error: Not on thumb mode!"
    .endif

    .error "Not implemented"
.endmacro