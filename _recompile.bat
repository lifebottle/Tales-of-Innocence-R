::Download the CSV from the GoogleSheets
::Sheets with <space> in the name should be replaced with %20. 
::Using BAT file, escape an extra % like this %%20 instead.
if not exist "2_translated" mkdir 2_translated
curl -L "https://docs.google.com/spreadsheets/d/1hfZIQXpGyQw6dQtG_oVKI7bkO0teIUG9bXN9kKrANBw/gviz/tq?tqx=out:csv&sheet=Skits&range=A:G" > 2_translated/Skit.csv
curl -L "https://docs.google.com/spreadsheets/d/1hfZIQXpGyQw6dQtG_oVKI7bkO0teIUG9bXN9kKrANBw/gviz/tq?tqx=out:csv&sheet=Story&range=A:E" > 2_translated/Story.csv
curl -L "https://docs.google.com/spreadsheets/d/1hfZIQXpGyQw6dQtG_oVKI7bkO0teIUG9bXN9kKrANBw/gviz/tq?tqx=out:csv&sheet=Eboot&range=A:C" > 2_translated/eboot.csv
curl -L "https://docs.google.com/spreadsheets/d/1hfZIQXpGyQw6dQtG_oVKI7bkO0teIUG9bXN9kKrANBw/gviz/tq?tqx=out:csv&sheet=Artes&range=A:E" > 2_translated/ArtsDataPack.csv
curl -L "https://docs.google.com/spreadsheets/d/1hfZIQXpGyQw6dQtG_oVKI7bkO0teIUG9bXN9kKrANBw/gviz/tq?tqx=out:csv&sheet=Items&range=A:E" > 2_translated/ItemDataPack.csv
curl -L "https://docs.google.com/spreadsheets/d/1hfZIQXpGyQw6dQtG_oVKI7bkO0teIUG9bXN9kKrANBw/gviz/tq?tqx=out:csv&sheet=Mapdata/NPC&range=A:G" > 2_translated/MapData.csv
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



::patched and move the file from Inno-remaining repo to the this repo
pushd "..\Inno-remaining\Mine\"
CALL insert.bat
popd
:: I don't think we need the field file anymore
::Copy "..\Inno-remaining\Mine\Data\Archives\Field\New" 3_patched\toidata_release\_Data\Field
Copy "..\Inno-remaining\Mine\Data\Archives\Battle\New\TutorialData.dat" 3_patched\toidata_release\_Data\Battle
Copy "..\Inno-remaining\Mine\Data\Archives\System\New\BattleBookDataPack.dat" 3_patched\toidata_release\_Data\System
Copy "..\Inno-remaining\Mine\Data\Archives\System\New\KizunaDataPack.dat" 3_patched\toidata_release\_Data\System
Copy "..\Inno-remaining\Mine\Data\Archives\System\New\StoryBookDataPack.dat" 3_patched\toidata_release\_Data\System

::Build command for LT tool, other settings need to be decommented in recompile.py
python recompile.py 0_PCSG00009_dec 2_translated 3_patched

Build command for the asm hacks
pushd "tools/asm/"
armips.exe InnocenceR.asm
popd

pause
