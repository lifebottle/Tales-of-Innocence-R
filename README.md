# Tales of Innocence R

An attempt to create an English patch for Tales of Innocence R.

![ToIR](https://raw.githubusercontent.com/pnvnd/Tales-of-Innocence-R/main/toir.png)

## Hacker Note 1

1. Get `pkg2zip` https://github.com/mmozeiko/pkg2zip and `psvpfstools` https://github.com/motoharu-gosuto/psvpfstools
2. With `pkg2zip` extract the `pkg` `pkg2zip.exe` `innocenceR.pkg`
3. It should produce this zip file `テイルズ オブ イノセンス R [PCSG00009] [JPN].zip`. Extract it.
4. It should extract a folder named app cut the folder PCSG00009 from it and paste it in the same folder as psvpfstools
5. Then run `psvpfsparser.exe -i PCSG00009 -o PCSG00009_dec -z <zRif> -f http://cma.henkaku.xyz`
6. Get `zRif` from somewhere
7. If everything's correct it will decrypt everything into the `PCSG00009_dec`
8. You still need a Vita to decrypt the `EBOOT.BIN` as it is an FSELF and it's encrypted

![L7CA_header](https://raw.githubusercontent.com/pnvnd/Tales-of-Innocence-R/main/L7CA_decrypted.png)


## Hacker Note 2

1. Compile `psvita-l7ctool.exe` from the taikotools submodule and run this command: `psvita-l7ctool.exe x toidata_release.l7c`
2. You'll get a message `This archive type is unsupported and most likely won't unpack properly.`
3. Files get extracted anyway, not sure if extracted correctly though: `_Data/Battle/Effect/00.pck`
