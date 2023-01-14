from .items import recompile_items
from .artes import recompile_artes
from .charanames import recompile_pack_field

_RECOMPILERS = [
    recompile_items,
    recompile_artes,
    #recompile_pack_field,
]

def recompile_dat(l7cdir, csvdir, outputdir):
    for recompiler in _RECOMPILERS:
        recompiler(l7cdir, csvdir, outputdir)