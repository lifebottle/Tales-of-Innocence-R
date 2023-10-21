# Tales of Innocence R

An attempt to create an English patch for Tales of Innocence R.

![ToIR](tools/assets/toir.png)

Discord: https://discord.gg/tmDgBDNPpE  

Spreadsheet (Current): https://docs.google.com/spreadsheets/d/1hfZIQXpGyQw6dQtG_oVKI7bkO0teIUG9bXN9kKrANBw/edit?usp=sharing  
Spreadsheet (Outdated): https://docs.google.com/spreadsheets/d/1X_-WfAYM5J2JL2uDAK0JPA9P8zGQHe2G3otozGymd1I/edit?usp=sharing  


## Hacker Note 1

![ToIR](tools/assets/decrypt_toir.gif)  

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

![L7CA_header](tools/assets/L7CA_decrypted.png)


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
1. Change the `eboot.bin` (the one with the 0x1000 SCE header) as follows: offset `0x7B5E` (should contain `01 23`) to `00 23` to fix monospace problem
2. Also, change the `eboot.bin` as follows: offset `0x8630` (should contain `80 18`) to `40 18`
3. If `recompile.py` doesn't work, install python package "sortedcontainers", "click", and "pypng": `pip install sortedcontainers`, `pip install click`, `pip install pypng`
4. Get `Kuriiku2.exe` (CMD version) to batch replace patched files: `Kuriimu2.exe extensions batch-inject orig-dir patch-dir`
```
orig-dir
 data_release.l7c (as a file)

patch-dir
 data_release.l7c (as a directory)
  _data
   announcement
    announcement.anm
 (followed by any number of files in the correct directory relative to the L7c)
```

## Hacker Note #5
![movie_subs](tools/assets/moviecaptions.png)  
1. Movie subs can be saved to .SRT format

## Hacker Note #6
![kuriimu2](tools/assets/kuriimu2_settings.png)  
1. Batch inject settings to create patch  

## Credits
Thanks to Ethanol for basically everything  
Thanks to LT for for basically everything  
Thansk to OnePieceFreak for basically everything  
`Mine` for Translation Script: https://docs.google.com/document/d/12hoLXugMHRRiQ7YrqrB5nvLvxlpH9tIc7yisB_ZI_Y4/edit  
`kkhdigifantasy13` for Translation Guide: https://drive.google.com/file/d/1sbCzce3OMSNVEKuTcYGWufS-NWkJq4Th/view?usp=sharing  
`AppleKratue` for Gameplay Guide: https://psnprofiles.com/guide/6120-tales-of-innocence-r-faq (https://twitter.com/talesofkratue)  

## Tools
https://gbatemp.net/threads/release-decrypt-and-launch-psn-store-vita-games-without-plugins.548878/
https://github.com/FanTranslatorsInternational/Kuriimu2  
https://github.com/onepiecefreak3/taikotools  
https://github.com/mariodon/taikotools  
