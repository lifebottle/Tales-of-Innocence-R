::::THIS PART IS WORKING
::::this has been extracted 2023-12-30
::pushd "0_gamefiles/toidata_release/_Data/Battle/Voice/Result"
::for /f "tokens=1* delims=." %%f in ('dir /b /a-d') do (
::	pushd "tools/Audio/AT9_AT3_Converter/ATRAC"
::    PSVita_at9tool.exe -d "../../../../0_gamefiles/toidata_release/_Data/Battle/Voice/Result/%%f.at9" "../../../../1_extracted/Battle/Voice/Result/%%f.wav"
::	popd
::)
::popd

::::this has been extracted 2023-12-30
::pushd "0_gamefiles/toidata_release/_Data/Field/Skit/Voice"
::for /f "tokens=1* delims=." %%f in ('dir /b /a-d') do (
::	pushd "tools/Audio/AT9_AT3_Converter/ATRAC"
::    PSVita_at9tool.exe -d "../../../../0_gamefiles/toidata_release/_Data/Field/Skit/Voice/%%f.at9" "../../../../1_extracted/Field/Skit/Voice/%%f.wav"
::	popd
::)
::popd

::::this has been extracted 2023-12-30
::pushd "0_gamefiles/toidata_release/_Data/Field/Voice/01"
::for /f "tokens=1* delims=." %%f in ('dir /b /a-d') do (
::	pushd "tools/Audio/AT9_AT3_Converter/ATRAC"
::    PSVita_at9tool.exe -d "../../../../0_gamefiles/toidata_release/_Data/Field/Voice/01/%%f.at9" "../../../../1_extracted/Field/Voice/01/%%f.wav"
::	popd
::)
::popd


::::this has been extracted 2024-01-15
::pushd "0_gamefiles/toidata_release/_Data/Battle/Voice/GameOver"
::for /f "tokens=1* delims=." %%f in ('dir /b /a-d') do (
::	pushd "tools/Audio/AT9_AT3_Converter/ATRAC"
::    PSVita_at9tool.exe -d "../../../../0_gamefiles/toidata_release/_Data/Battle/Voice/GameOver/%%f.at9" "../../../../1_extracted/Battle/Voice/GameOver/%%f.wav"
::	popd
::)
::popd

::::this has been extracted 2024-01-15
::pushd "0_gamefiles/toidata_release/_Data/Battle/Voice/Start/Enemy"
::for /f "tokens=1* delims=." %%f in ('dir /b /a-d') do (
::	pushd "tools/Audio/AT9_AT3_Converter/ATRAC"
::    PSVita_at9tool.exe -d "../../../../0_gamefiles/toidata_release/_Data/Battle/Voice/Start/Enemy/%%f.at9" "../../../../1_extracted/Battle/Voice/Start/Enemy/%%f.wav"
::	popd
::)
::popd

::::this has been extracted 2024-01-15
::pushd "0_gamefiles/toidata_release/_Data/Battle/Voice/Start/Player"
::for /f "tokens=1* delims=." %%f in ('dir /b /a-d') do (
::	pushd "tools/Audio/AT9_AT3_Converter/ATRAC"
::    PSVita_at9tool.exe -d "../../../../0_gamefiles/toidata_release/_Data/Battle/Voice/Start/Player/%%f.at9" "../../../../1_extracted/Battle/Voice/Start/Player/%%f.wav"
::	popd
::)
::popd

:::: THIS PART IS WORKING extracted on 2024-05-16
::pushd "tools/Audio/Audio_Dat_Script"
::python AudioDatSplitter_1.py "--extract" "../../../0_gamefiles/toidata_release/_Data/Battle/Voice/" "../../../1_extracted/Battle/Voice/" "../vgmstream-win64/vgmstream-cli.exe"
::popd

:::: THIS PART IS WORKING extracted on 2024-05-16
::pushd "tools/Audio/Audio_Dat_Script"
::python AudioDatSplitter_dat.py "--extract" "../../../0_gamefiles/toidata_release/_Data/Sound/" "../../../1_extracted/Sound/" "../vgmstream-win64/vgmstream-cli.exe"
::popd

:: THIS PART IS WORKING extracted on  2024-05-16
::pushd "tools/Audio/Audio_Dat_Script"
::python AudioDatSplitter_1.py "--extract" "../../../0_gamefiles/toidata_release/_Data/CharaModel/Player/" "../../../1_extracted/CharaModel/Player/" "../vgmstream-win64/vgmstream-cli.exe"
::popd

::::this has been extracted 2024-05-16
::pushd "0_gamefiles/toidata_release/_Data/Logo"
::for /f "tokens=1* delims=." %%f in ('dir /b /a-d') do (
::	pushd "tools/Audio/AT9_AT3_Converter/ATRAC"
::    PSVita_at9tool.exe -d "../../../../0_gamefiles/toidata_release/_Data/Logo/%%f.at9" "../../../../1_extracted/Logo/%%f.wav"
::	popd
::)
::popd

pause 