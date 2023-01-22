.open "../../3_patched/eboot.bin",0x80FFE000
.arm.little
.thumb
.include "armv7-a_macros.asm"

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
mov.w      r3,0xE
str.w      r3, /*[*/ r6,0x0 /*]*/
pop        { r3 }
;adds       /*r*/6,0x3c
;add.w      /*r*/7,/*lr*/14,0x2
b.w        default
go_back:
b.w        else_case

tag_case:
adds       r6,#0x3c
add.w      r7,lr,0x4
add.w      r8,r2,0x2
b.w        default


; Cooking Lv text overlaps the number
; so let's move that to the left
.org 0x8112F332
movw       r2,0x154


; Remove the monospacing 0x01 is on, 0x00 is off
.orga 0x7B5E
.byte 0x00

; Change the width of the whitespace to half from 0x80 to 0x40
.orga 0x8630
.byte 0x40


; Replace the 'a' special char with '|'
.org 0x8115D138
.asciiz "|"


; The width of a button is derived from
; the width of a space, which is half the width
; from the japanese one, so let's use 2
.org 0x8115CF70
.asciiz "  "

.close
