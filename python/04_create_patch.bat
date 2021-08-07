xdelta.exe -f -e -s "PCSG00009_dec\eboot.bin" "patched\eboot.bin" "eboot.xdelta"
xdelta.exe -f -e -s "eboot.bin.elf" "patched\eboot.bin" "fagdec_eboot_fagdec.xdelta"
xdelta.exe -f -e -s "PCSG00009_dec\toidata_release.l7c" "orig-dir\toidata_release.l7c" "toidata_release.xdelta"
pause