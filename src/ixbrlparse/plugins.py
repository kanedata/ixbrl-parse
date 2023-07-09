import importlib

import pluggy

from ixbrlparse import hookspecs

DEFAULT_PLUGINS = ["ixbrlparse.components.formats"]

pm = pluggy.PluginManager("ixbrlparse")
pm.add_hookspecs(hookspecs)

pm.load_setuptools_entrypoints("ixbrlparse")

# Load default plugins
for plugin in DEFAULT_PLUGINS:
    mod = importlib.import_module(plugin)
    pm.register(mod, plugin)
