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

_RECOMPILERS = [
    recompile_items, #done
    recompile_artes, #done
    recompile_pack_field, #done
    recompile_chara_styles, #done
    recompile_enemies, #done
    recompile_chara_ability,#done
    recompile_succession #done with ethanol help
    #recompile_operations, #wip
    #recompile_shop_names #wip
    #recompile_bond #wip
    #recompile_mission  #wip 
]

def recompile_dat(l7cdir, csvdir, outputdir):
    for recompiler in _RECOMPILERS:
        recompiler(l7cdir, csvdir, outputdir)