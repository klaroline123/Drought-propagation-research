"""Repository-local plotting setup; no scientific analysis."""
from pathlib import Path
import os
def configure(root):
    cache=Path(root)/'outputs/runtime'; cache.mkdir(parents=True,exist_ok=True)
    for key in ['MPLCONFIGDIR','XDG_CACHE_HOME','TEMP','TMP','TMPDIR','NUMBA_CACHE_DIR']:
        os.environ[key]=str(cache)
    import tempfile
    tempfile.tempdir=str(cache)
