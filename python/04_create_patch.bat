xdelta.exe -f -e -s "PCSG00009_dec\eboot.bin" "patched\eboot.bin" "dec_eboot.xdelta"
xdelta.exe -f -e -s "eboot.bin.elf" "patched\eboot.bin" "fagdec_eboot_elf.xdelta"
xdelta.exe -f -e -s "eboot.bin" "patched\eboot.bin" "fagdec_eboot.xdelta"
xdelta.exe -f -e -s "eboot_raw.bin" "patched\eboot.bin" "raw_eboot.xdelta"
xdelta.exe -f -e -s "PCSG00009_dec\toidata_release.l7c" "orig-dir\toidata_release.l7c" "toidata_release.xdelta"
xdelta.exe -f -e -s "C:\temp\ToIR\PCSG00009\toidata_release.l7c" "orig-dir\toidata_release.l7c" "raw_toidata_release.xdelta"
tar.exe -acf toir_patch.zip dec_eboot.xdelta fagdec_eboot_elf.xdelta fagdec_eboot.xdelta toidata_release.xdelta toir_readme.txt
pause
