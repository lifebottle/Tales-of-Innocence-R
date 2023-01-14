.open "../../3_patched/eboot.bin",0x80FFE000
.arm.little
.thumb
.include "armv7-a_macros.asm"

; Registers are numbered (r)0-12
; then special names follow
; SP -> 13
; LR -> 14
; PC -> 15

.org 0x8102ABBE
cmp        r3,#0x40
bne        skip
b.w        tag_case

skip:
b.w        space_case
nop :: nop

else_case:

.org 0x8102ABF2
default:

.org 0x8115F798
space_case:
cmp        r3,#0x20
bne        go_back
push       { r3 }
mov.w      /*r*/3,0xE
str.w      /*r*/3,/*[r*/6,0x0/*]*/
pop        { r3 }
;That was the code fucking up the letters the first few attempts at fixing the button on Innocence
;adds       /*r*/6,0x3c
;add.w      /*r*/7,/*lr*/14,0x2
b.w        default
go_back:
b.w        else_case

tag_case:
adds       r6,#0x3c
add.w      /*r*/7,/*lr*/14,0x4
add.w      /*r*/8,/*r*/2,0x2
b.w        default


; Cooking Lv text overlaps the number
; so let's move that to the left, 0x164 to 0x154
.org 0x8112F332
movw       /*r*/2,0x154

; Replace the 'a' special char with '|'
.org 0x8115D138
.asciiz "|"


; The width of a button is derived from
; the width of a space, which is half the width
; from the japanese one, so let's use 2
.org 0x8115CF70
.asciiz "  "

; Remove the monospacing 0x01 is on, 0x00 is off
.orga 0x7B5E
.byte 0x00

; Change the width of the whitespace to half from 0x80 to 0x40
.orga 0x8630
.byte 0x40

.close
