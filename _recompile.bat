::Download the CSV from the GoogleSheets
::Sheets with <space> in the name should be replaced with %20. 
::Using BAT file, escape an extra % like this %%20 instead.
if not exist "2_translated" mkdir 2_translated

curl -L "https://docs.google.com/spreadsheets/d/1hfZIQXpGyQw6dQtG_oVKI7bkO0teIUG9bXN9kKrANBw/gviz/tq?tqx=out:csv&sheet=Skits&range=A:H" > 2_translated/Skit.csv
curl -L "https://docs.google.com/spreadsheets/d/1hfZIQXpGyQw6dQtG_oVKI7bkO0teIUG9bXN9kKrANBw/gviz/tq?tqx=out:csv&sheet=Story&range=A:F" > 2_translated/Story.csv
curl -L "https://docs.google.com/spreadsheets/d/1hfZIQXpGyQw6dQtG_oVKI7bkO0teIUG9bXN9kKrANBw/gviz/tq?tqx=out:csv&sheet=Mapdata/NPC&range=A:G" > 2_translated/MapData.csv
curl -L "https://docs.google.com/spreadsheets/d/1hfZIQXpGyQw6dQtG_oVKI7bkO0teIUG9bXN9kKrANBw/gviz/tq?tqx=out:csv&sheet=Eboot&range=A:C" > 2_translated/eboot.csv
curl -L "https://docs.google.com/spreadsheets/d/1hfZIQXpGyQw6dQtG_oVKI7bkO0teIUG9bXN9kKrANBw/gviz/tq?tqx=out:csv&sheet=Artes&range=A:E" > 2_translated/ArtsDataPack.csv
curl -L "https://docs.google.com/spreadsheets/d/1hfZIQXpGyQw6dQtG_oVKI7bkO0teIUG9bXN9kKrANBw/gviz/tq?tqx=out:csv&sheet=Items&range=A:E" > 2_translated/ItemDataPack.csv
curl -L "https://docs.google.com/spreadsheets/d/1hfZIQXpGyQw6dQtG_oVKI7bkO0teIUG9bXN9kKrANBw/gviz/tq?tqx=out:csv&sheet=EnemyArtes&range=A:C" > 2_translated/EnemyParam_Artes.csv
curl -L "https://docs.google.com/spreadsheets/d/1hfZIQXpGyQw6dQtG_oVKI7bkO0teIUG9bXN9kKrANBw/gviz/tq?tqx=out:csv&sheet=EnemyNames&range=A:C" > 2_translated/EnemyParam_Names.csv
curl -L "https://docs.google.com/spreadsheets/d/1hfZIQXpGyQw6dQtG_oVKI7bkO0teIUG9bXN9kKrANBw/gviz/tq?tqx=out:csv&sheet=Names&range=A:C" > 2_translated/CharaNames.csv
curl -L "https://docs.google.com/spreadsheets/d/1hfZIQXpGyQw6dQtG_oVKI7bkO0teIUG9bXN9kKrANBw/gviz/tq?tqx=out:csv&sheet=Locations&range=A:C" > 2_translated/Locations.csv
curl -L "https://docs.google.com/spreadsheets/d/1hfZIQXpGyQw6dQtG_oVKI7bkO0teIUG9bXN9kKrANBw/gviz/tq?tqx=out:csv&sheet=Locations2&range=A:C" > 2_translated/Locations2.csv
curl -L "https://docs.google.com/spreadsheets/d/1hfZIQXpGyQw6dQtG_oVKI7bkO0teIUG9bXN9kKrANBw/gviz/tq?tqx=out:csv&sheet=Locations3&range=A:C" > 2_translated/Locations3.csv
curl -L "https://docs.google.com/spreadsheets/d/1hfZIQXpGyQw6dQtG_oVKI7bkO0teIUG9bXN9kKrANBw/gviz/tq?tqx=out:csv&sheet=SkitNames&range=A:C" > 2_translated/SkitNames.csv
curl -L "https://docs.google.com/spreadsheets/d/1hfZIQXpGyQw6dQtG_oVKI7bkO0teIUG9bXN9kKrANBw/gviz/tq?tqx=out:csv&sheet=Movie&range=A:C" > 2_translated/Movie.csv
curl -L "https://docs.google.com/spreadsheets/d/1hfZIQXpGyQw6dQtG_oVKI7bkO0teIUG9bXN9kKrANBw/gviz/tq?tqx=out:csv&sheet=CharaStyleDataPack&range=A:D" > 2_translated/CharaStyleDataPack.csv
curl -L "https://docs.google.com/spreadsheets/d/1hfZIQXpGyQw6dQtG_oVKI7bkO0teIUG9bXN9kKrANBw/gviz/tq?tqx=out:csv&sheet=Bond&range=A:D" > 2_translated/KizunaDataPack.csv
curl -L "https://docs.google.com/spreadsheets/d/1hfZIQXpGyQw6dQtG_oVKI7bkO0teIUG9bXN9kKrANBw/gviz/tq?tqx=out:csv&sheet=ShopNames&range=A:C" > 2_translated/ShopNames.csv
curl -L "https://docs.google.com/spreadsheets/d/1hfZIQXpGyQw6dQtG_oVKI7bkO0teIUG9bXN9kKrANBw/gviz/tq?tqx=out:csv&sheet=StrategyMenu&range=A:E" > 2_translated/Operation.csv
curl -L "https://docs.google.com/spreadsheets/d/1hfZIQXpGyQw6dQtG_oVKI7bkO0teIUG9bXN9kKrANBw/gviz/tq?tqx=out:csv&sheet=CharaAbility&range=A:E" > 2_translated/CharaAbility.csv
curl -L "https://docs.google.com/spreadsheets/d/1hfZIQXpGyQw6dQtG_oVKI7bkO0teIUG9bXN9kKrANBw/gviz/tq?tqx=out:csv&sheet=Newgame&range=A:E" > 2_translated/SuccessionData.csv
curl -L "https://docs.google.com/spreadsheets/d/1hfZIQXpGyQw6dQtG_oVKI7bkO0teIUG9bXN9kKrANBw/gviz/tq?tqx=out:csv&sheet=Mission&range=A:E" > 2_translated/MissionData.csv
curl -L "https://docs.google.com/spreadsheets/d/1hfZIQXpGyQw6dQtG_oVKI7bkO0teIUG9bXN9kKrANBw/gviz/tq?tqx=out:csv&sheet=Battlebook&range=A:E" > 2_translated/Battlebook.csv
curl -L "https://docs.google.com/spreadsheets/d/1hfZIQXpGyQw6dQtG_oVKI7bkO0teIUG9bXN9kKrANBw/gviz/tq?tqx=out:csv&sheet=Synopsis&range=A:E" > 2_translated/Storybook.csv
curl -L "https://docs.google.com/spreadsheets/d/1hfZIQXpGyQw6dQtG_oVKI7bkO0teIUG9bXN9kKrANBw/gviz/tq?tqx=out:csv&sheet=TutorialGame&range=A:D" > 2_translated/TutorialGame.csv

::These are still hex edited so we need to move the binary from translated to patched
Copy "2_translated/Battle/MissionData.dat" "3_patched/toidata_release/_Data/Battle/MissionData.dat"
Copy "2_translated/System/OperationDataPack.dat" "3_patched/toidata_release/_Data/System/OperationDataPack.dat"

::patched and move the file from Inno-remaining repo to the this repo
::pushd "..\Inno-remaining\Mine\"
::CALL insert.bat
::popd
:: I don't think we need the field file or battlebook anymore
::Copy "..\Inno-remaining\Mine\Data\Archives\Field\New" 3_patched\toidata_release\_Data\Field
::Copy "..\Inno-remaining\Mine\Data\Archives\Battle\New\TutorialData.dat" 3_patched\toidata_release\_Data\Battle
::Copy "..\Inno-remaining\Mine\Data\Archives\System\New\BattleBookDataPack.dat" 3_patched\toidata_release\_Data\System
::Copy "..\Inno-remaining\Mine\Data\Archives\System\New\KizunaDataPack.dat" 3_patched\toidata_release\_Data\System
::Copy "..\Inno-remaining\Mine\Data\Archives\System\New\StoryBookDataPack.dat" 3_patched\toidata_release\_Data\System

:: wordwrap script
pushd "tools\Wordwrap"
python StoryWordWrap.py
python SkitWordWrap.py
popd

::Build command for LT tool, other settings need to be decommented in recompile.py
python ./tools/toir/recompile.py 0_gamefiles 2_translated 3_patched

::Build command for the asm hacks
pushd "tools/asm/"
armips.exe InnocenceR.asm
popd

pause