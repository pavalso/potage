from . import _ingredient as ingredients

from ._pot import pot
from ._chef import Chef


prepare = pot.prepare
cook = pot.cook


__all__ = ["prepare", "cook", "Chef", "ingredients"]
