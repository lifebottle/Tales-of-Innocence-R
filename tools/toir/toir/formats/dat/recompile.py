from .items import recompile_items
from .artes import recompile_artes
from .packfield import recompile_pack_field
from .enemies import recompile_enemies
from .charaability import recompile_chara_ability
from .mission import recompile_mission
from .charastyles import recompile_chara_styles
from .kizuna import recompile_bond
from .shops import recompile_shop_names
from .operation import recompile_operations
from .succession import recompile_succession
from .battlebook import recompile_battlebook
from .storybook import recompile_storybook
from .tutorial import recompile_tutorial


_RECOMPILERS = [
    recompile_items, #done
    recompile_artes, #done
    recompile_pack_field, #done
    recompile_chara_styles, #done
    recompile_enemies, #done
    recompile_chara_ability,#done
    recompile_succession, #done with ethanol help
    recompile_battlebook, #done with Stewie's help
    recompile_storybook, #done copied stewie's code
    recompile_tutorial, #done stewie
    recompile_operations, #done with Stewie's help
    recompile_shop_names, #done with Stewie's help
    recompile_bond, #copied stewie's code
    recompile_mission  #done with Stewie's help
]

def recompile_dat(l7cdir, csvdir, outputdir):
    for recompiler in _RECOMPILERS:
        recompiler(l7cdir, csvdir, outputdir)