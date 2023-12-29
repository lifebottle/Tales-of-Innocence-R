REM Sheets with <space> in the name should be replaced with %20. Using BAT file, escape % by using %%20 instead.
if not exist "translated" mkdir translated
curl -L "https://docs.google.com/spreadsheets/d/1hfZIQXpGyQw6dQtG_oVKI7bkO0teIUG9bXN9kKrANBw/gviz/tq?tqx=out:csv&sheet=Skits%%205.0&range=A:G" > ./translated/Skit.csv
curl -L "https://docs.google.com/spreadsheets/d/1hfZIQXpGyQw6dQtG_oVKI7bkO0teIUG9bXN9kKrANBw/gviz/tq?tqx=out:csv&sheet=Story%%201.0" > ./translated/Story.csv
curl -L "https://docs.google.com/spreadsheets/d/1hfZIQXpGyQw6dQtG_oVKI7bkO0teIUG9bXN9kKrANBw/gviz/tq?tqx=out:csv&sheet=TESTING-eboot&range=A:C" > ./translated/eboot.csv
curl -L "https://docs.google.com/spreadsheets/d/1hfZIQXpGyQw6dQtG_oVKI7bkO0teIUG9bXN9kKrANBw/gviz/tq?tqx=out:csv&sheet=Done--Artes&range=A:E" > ./translated/ArtsDataPack.csv
curl -L "https://docs.google.com/spreadsheets/d/1hfZIQXpGyQw6dQtG_oVKI7bkO0teIUG9bXN9kKrANBw/gviz/tq?tqx=out:csv&sheet=WIP-Items&range=A:E" > ./translated/ItemDataPack.csv
curl -L "https://docs.google.com/spreadsheets/d/1hfZIQXpGyQw6dQtG_oVKI7bkO0teIUG9bXN9kKrANBw/gviz/tq?tqx=out:csv&sheet=Done--Names&range=A:C" > ./translated/CharaNames.csv
curl -L "https://docs.google.com/spreadsheets/d/1hfZIQXpGyQw6dQtG_oVKI7bkO0teIUG9bXN9kKrANBw/gviz/tq?tqx=out:csv&sheet=Mapdata/NPC%%201.0&range=A:G" > ./translated/MapData.csv
pause