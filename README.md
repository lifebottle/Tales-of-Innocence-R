# Tales of Innocence R
An attempt to create an English patch for Tales of Innocence R.

## Hacker Note 1
1. Get `pkg2zip` https://github.com/mmozeiko/pkg2zip and `psvpfstools` https://github.com/motoharu-gosuto/psvpfstools
1. With `pkg2zip` extract the `pkg` `pkg2zip.exe` `innocenceR.pkg`
1. It should produce this zip file `テイルズ オブ イノセンス R [PCSG00009] [JPN].zip`. Extract it.
1. It should extract a folder named app cut the folder PCSG00009 from it and paste it in the same folder as psvpfstools
1. Then `run psvpfsparser.exe -i PCSG00009 -o PCSG00009_dec -z <zRif> -f http://cma.henkaku.xyz`
1. Get `zRif` from somewhere
1. If everything's correct it will decrypt everything into the `PCSG00009_dec`
1. You still need a Vita to decrypt the `EBOOT.BIN` as it is an FSELF and it's encrypted
