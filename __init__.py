
# ──────────────────────────
# comfyui-sequential-prompt
# ──────────────────────────
# from .nodes import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS
import importlib.util
import glob
import os
import sys
from .protcol import init, get_ext_dir, log
from .nodes import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

# ──────────────────────────

init()
# ──────────────────────────
py = get_ext_dir("py")
WEB_DIRECTORY = "./js"
__all__ = ['NODE_CLASS_MAPPINGS',
           'NODE_DISPLAY_NAME_MAPPINGS', 'WEB_DIRECTORY']
