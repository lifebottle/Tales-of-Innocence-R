from .artes import extract_artes
from .items import extract_items
from .battlebook import extract_battle_book
from .charaability import extract_chara_ability
from .charanames import extract_chara_names
from .tutorial import extract_tutorial
from .mission import extract_mission
from .enemies import extract_enemies
from .charastyles import extract_chara_styles
from .kizuna import extract_kizuna
from .shops import extract_shops
from .succession import extract_succession
from .operation import extract_operation
from .storybook import extract_story_book

_EXTRACTORS = [
    extract_items,
    extract_artes,
    extract_battle_book,
    extract_chara_ability,
    extract_chara_names,
    extract_chara_styles,
    extract_tutorial,
    extract_mission,
    extract_enemies,
    extract_kizuna,
    extract_shops,
    extract_succession,
    extract_operation,
    extract_story_book,
]

def extract_dat(l7cdir, outputdir):
    for extractor in _EXTRACTORS:
        extractor(l7cdir, outputdir)