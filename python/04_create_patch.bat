xdelta.exe -f -e -s "PCSG00009_dec\eboot.bin" "patched\eboot.bin" "eboot.xdelta"
xdelta.exe -f -e -s "eboot.bin.elf" "patched\eboot.bin" "fagdec_eboot.xdelta"
xdelta.exe -f -e -s "PCSG00009_dec\toidata_release.l7c" "orig-dir\toidata_release.l7c" "toidata_release.xdelta"
tar.exe -acf toir_patch.zip eboot.xdelta fagdec_eboot.xdelta toidata_release.xdelta toir_readme.txt
pause