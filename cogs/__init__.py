from __future__ import annotations
from discord.ext.commands import Cog
from core import Bot
from logging import getLogger; log = getLogger(__name__)

__all__ = ("Plugin",)

class Plugin(Cog):
    def __init__(self, bot: Bot) -> None:
        super().__init__()
        
    async def cog_load(self) -> None:
        log.info(f"Loaded {self.qualified_name} cog.")