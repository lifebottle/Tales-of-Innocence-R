.open "../../3_patched/eboot.bin",0x80FFE000
.arm.little
.thumb
.include "armv7-a_macros.asm"

; fonts from app folder (broken)
;.org 0x810059d2
;movs r1,0x0
;bl   0x81005340


;################################
;       100 save slots hack
;################################

; The save class has an array with
; every slot it's goin to use (among other stuff)
; at 0x20 bytes per slot it's 25 x 0x20 = 0x320
; then at 100 slots we'd need 100 x 0x20 = 0xC80
; So we just tack that at the end of the allocator
; original size + the extra data is:
; 0x6CC + 0xC80 = 0x134C
.org 0x8100bdd6
movw       r0, 0x134C

; Move the slot array pointer to the end of the
; allocated space (new space)
.org 0x8101d950
addw       r5,r4,0x6cc ; for save screen
.org 0x8101d874
addw       r5,r4,0x6cc ; for load screen

; Update saveSlots array allocation, just memset
; the extra memory :)
.org 0x8101d95a
movs.w     r2,0xC80 ; for save screen
.org 0x8101d87e
movs.w     r2,0x640 ; for load screen


; Update saveSlots array init
; For save screen
.org 0x8101d9c2 :: str.w      r2,/*[*/r3,0x6cc/*]*/
.org 0x8101d9c8 :: str.w      r1,/*[*/r3,0x6d8/*]*/
.org 0x8101d9ce :: cmp        r2, 100
; Same but for load screen
.org 0x8101d8e6 :: str.w      r0,/*[*/r2,0x6cc/*]*/
.org 0x8101d8ee :: cmp        r0, 100

; Update array size field
.org 0x8101d8f8 :: movs.w     lr, 100
.org 0x8101d9d8 :: movs.w     lr, 100

;################################
;     Button alignment fix
;################################

.org 0x8102ABBE
cmp        r3,0x40
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

; Change sceCommonDialogSetConfigParam function caller
; to use the system language in the save screen
.org 0x8100bdd0
movs       r1,0x1


; Cooking Lv text overlaps the number
; so let's move that to the left
.org 0x8112F332
movw       r2,0x154


; Remove the monospacing 0x01 is on, 0x00 is off
.org 0x81005b5e
movs r3,0x0

; Change the width of the whitespace to half from 0x80 to 0x40
.org 0x81006630
; .org 0x8100662E :: add.w      r8,r8,r0, lsl #0x6

.byte 0x40


; Replace the 'a' special char with '|'
.org 0x8115D138
.asciiz "|"


; The width of a button is derived from
; the width of a space, which is half the width
; from the japanese one, so let's use 2
.org 0x8115CF70
.asciiz "  "

;;This breaks the inn gald line
;; ProcField setIsMonospace = false
;.org 0x810C502E
;movs r1,/*#*/0x00

; ProcBattle setIsMonospace = false
.org 0x8103F356
movs r1,/*#*/0x00
.org 0x8103F364
movs r1,/*#*/0x00

; font raster thing (breaks the cooking and newgame plus notice but make the letter spacing tighter on cooking menu)
;.org 0x810063E0
;.byte 0xb1, 0xf8, 0x66, 0x10 ;ldrh.w     r1,[r1,#0x66]
;
;.org 0x8100664E
;movs r1,/*#*/0x00 ; og .byte 0xf1, 0x69 ldr        r1,[r6,#0x1c]



; Style screen setIsMonospace = false
.org 0x8111E99E
movs r1,/*#*/0x00

.org 0x8111E9C2
movw r1,/*#*/0x00 ; movw r1,/*#*/0x209

.close