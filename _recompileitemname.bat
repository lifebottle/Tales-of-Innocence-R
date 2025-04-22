


curl -L "https://docs.google.com/spreadsheets/d/1hfZIQXpGyQw6dQtG_oVKI7bkO0teIUG9bXN9kKrANBw/gviz/tq?tqx=out:csv&sheet=Items&range=A:F" > 2_translated/ItemDataPack.csv


pushd "tools\Wordwrap"

python ItemWordWrap.py
popd

pause