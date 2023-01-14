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

.expfunc getoff(src_addr, dst_addr), ((dst_addr & (~1)) - (src_addr & (~1)) - 4)
.expfunc swaphw(w), (w >> 16 | w << 16)


;################################
;
;         B instructions
;   Check A8.8.18 in the manual
;
;################################

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

;################################
;
;         MOV instructions
;   Check A8.8.103 in the manual
;
;################################

; mov T2 encoding, encodes a <const>
; ranges defined by A6.3.2 section of the manual
.macro mov.w,rd,val
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
            /* i */ (((val >> 11) & 0b00001) << 26) | \
            /* st1 */ (0b100100 << 20) | \
            /* Imm4 */ (((val >> 12) & 0b1111) << 15) |\
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


;################################
;
;         STR instructions
;    Check A8.8.204 in the manual
;
;################################

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