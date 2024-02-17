from __future__ import annotations
from datetime import datetime
from typing import Any, Optional, Union
from discord import colour, Embed as OriginalEmbed
from typing_extensions import Self

from discord.colour import Colour
from discord.types.embed import EmbedType

__all__ = ("Embed",)

class Embed(OriginalEmbed):
    def __init__(self, color: Optional[Union[int, Colour]] = Colour.blue(), **kwargs: Any):
        super().__init__(color=color, **kwargs)
        
        
    def credits(self) -> None:
        super().set_footer(text="Made by Aetherium")
        return self