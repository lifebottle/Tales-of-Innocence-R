# Tales of Innocence R

An attempt to create an English patch for Tales of Innocence R.

![ToIR](https://raw.githubusercontent.com/pnvnd/Tales-of-Innocence-R/main/toir.png)

Discord: https://discord.gg/tmDgBDNPpE  

Spreadsheet: https://docs.google.com/spreadsheets/d/1hfZIQXpGyQw6dQtG_oVKI7bkO0teIUG9bXN9kKrANBw/edit?usp=sharing  


## Hacker Note 1

1. Get `pkg2zip` https://github.com/mmozeiko/pkg2zip 
2. Also, get `psvpfstools` https://github.com/motoharu-gosuto/psvpfstools
3. With `pkg2zip`, extract the `pkg` `pkg2zip.exe` `innocenceR.pkg`
4. It should produce this zip file `テイルズ オブ イノセンス R [PCSG00009] [JPN].zip`. Extract it.
5. It should extract a folder named app, cut the folder PCSG00009 from it and paste it in the same folder as `psvpfstools`
6. Then run `psvpfsparser.exe -i PCSG00009 -o PCSG00009_dec -z <zRif> -f http://cma.henkaku.xyz`
7. Get `zRif` from somewhere.
8. If everything's correct it will decrypt everything into the `PCSG00009_dec`
9. You still need a Vita to decrypt the `EBOOT.BIN` as it is an FSELF and it's encrypted
10. Download `FAGDec.vpk` https://github.com/CelesteBlue-dev/PSVita-RE-tools/raw/master/FAGDec/build/FAGDec.vpk
11. Install `FAGDec.vpk` from Vita Shell.  A new bubble should be on the home screen.
12. Select the `EBOOT.BIN` file to decrypt and choose `START DECRYPT(ELF)`

![L7CA_header](https://raw.githubusercontent.com/pnvnd/Tales-of-Innocence-R/main/L7CA_decrypted.png)


## Hacker Note 2 (Outdated)

1. Compile `psvita-l7ctool.exe` from the taikotools submodule and run this command: `psvita-l7ctool.exe x toidata_release.l7c`
2. You'll get a message `This archive type is unsupported and most likely won't unpack properly.`
3. Files get extracted anyway, not sure if extracted correctly though: `_Data/Battle/Effect/00.pck`

## Hacker Note 3

1. Skip Hacker Note 2
2. Get `Kuriimu2` from https://github.com/FanTranslatorsInternational/Kuriimu2/releases/tag/1.2.0
3. Install .NET Core 3.1 Runtime
4. Open `Kuriimu2.exe` and go to File > Open with Plugin > plugin_bandai_namco.dll > L7C > OK
5. Select `toidata_release.l7c` (decrypted from Hacker Note 1)
6. Right-click `_Data` and extract all.
7. View files in `UTF-8` to get readable Japanese

## Hacker Note 4
1. ItemDataPack.dat = item name and description
2. ArtsDataPack.dat - Magic
3. EnemyParam = artes names, enemy names
4. BattleBookDataPack.dat seems to be tutorial ( and also end of battle pop ups ?)
5. these DAT files are easy enough that you could just write a simple Python script that extracts/inserts the text, Python can decode/encode UTF-8 natively
6. first a 32-bit word that represents the number of "sub sections" or whatever you want to call them. then, starting from offset 0x10, there is a list of offset/size pairs that describes the sub sections. each sub section then contains a sequence of records. the records contain the text (besides others).
7. the size of a record is always the same within a sub section, but can be different between different sub sections
8. get from virtual address to offset in the file you'd need to subtract `0x80FFF000`
9. you only substract the offset to the text section from the base virtual address
10. `abcde`: if it uses 32-bit math you could try `7F001000` (positive)
11. `0x175AEC` at this offset there's a pointer to some text
12. the pointers where the lower 16 and upper 16 bits are a few instructions apart, because they're embedded into the code, and you need to extract the values from the instruction encoding (which abcde probably can't do)
13. new line `0A`

## Hacker Note #4
Change the `eboot.bin` (the one with the 0x1000 SCE header) as follows: offset `0x7B5E` (should contain `01 23`) to `00 23` to fix monospace problem

## Credits
Thanks to Ethanol for basically everything  
Thanks to LT for for basically everything  
Thansk to OnePieceFreak for basically everything

## Tools
https://gbatemp.net/threads/release-decrypt-and-launch-psn-store-vita-games-without-plugins.548878/
https://github.com/FanTranslatorsInternational/Kuriimu2  
https://github.com/onepiecefreak3/taikotools  
https://github.com/mariodon/taikotools  
