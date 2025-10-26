import importlib
import pkgutil
from .base import db

# Automatically import all modules inside the 'models' package (except base)
for _, module_name, _ in pkgutil.iter_modules(__path__):
    if module_name != "base":
        importlib.import_module(f"{__name__}.{module_name}")

__all__ = ["db"]