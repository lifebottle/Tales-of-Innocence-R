# Tales of Innocence R

An attempt to create an English patch for Tales of Innocence R.

![ToIR](https://raw.githubusercontent.com/pnvnd/Tales-of-Innocence-R/main/toir.png)

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


## Hacker Note 2

1. Compile `psvita-l7ctool.exe` from the taikotools submodule and run this command: `psvita-l7ctool.exe x toidata_release.l7c`
2. You'll get a message `This archive type is unsupported and most likely won't unpack properly.`
3. Files get extracted anyway, not sure if extracted correctly though: `_Data/Battle/Effect/00.pck`

## Hacker Note 3

1. Skip Hacker Note 2
2. Get Kuriimu2 from https://github.com/FanTranslatorsInternational/Kuriimu2/releases/tag/1.2.0
3. Install .NET Core 3.1 Runtime
4. Open `Kuriimu2.exe` and go to File > Open with Plugin
5. Select `toidata_release.l7c` (decrypted from Hacker Note 1)
6. Right-click `_Data` and extract all.
7. View files in `UTF-8` to get readable Japanese
