from __future__ import annotations
import os
import sys
from typing import Optional
from .embed import Embed
from discord.ext import commands
from logging import getLogger
log = getLogger("Bot")
import discord


__all__ = ("Bot",)

class Bot(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=discord.Intents.all(),
            chunk_guild_at_startup=False
        )


        
    async def setup_hook(self) -> None:
       for file in os.listdir("cogs"):
           if not file.startswith("_"):
               await self.load_extension(f"cogs.{file}.plugin")
        
    async def on_ready(self) -> None:
       log.info(f"logged in as {self.user}")
        
    async def on_connect(self) -> None:
       if '-sync' in sys.argv:
           synced_commmands = await self.tree.sync()
           log.info(f"Successfully synced {len(synced_commmands)} commands.")
        
    async def success(
       self,  
       message: str,
       interaction: discord.Interaction, *,
       ephemeral: bool = False,
       embed: Optional[bool] = True
    ) -> Optional[discord.WebhookMessage]:
        if embed:
            if interaction.response.is_done():
                return await interaction.followup.send(
                    embed=Embed(description=message, color=discord.Color.green())
                )
                
            return await interaction.response.send_message(
                embed=Embed(description=message, color=discord.Color.green()),
                ephemeral=ephemeral
            )

        
    async def error(
       self,
       message: str,
       interaction: discord.Interaction, *,
       ephemeral: bool = True,
       embed: Optional[bool] = True
    ) -> Optional[discord.WebhookMessage]:
        if embed:
            if interaction.response.is_done():
                return await interaction.followup.send(
                    embed=Embed(description=message, color=discord.Color.red())
                )
                
            return await interaction.response.send_message(
                embed=Embed(description=message, color=discord.Color.red()),
                ephemeral=ephemeral
            )
        
        else:
            if interaction.response.is_done():
                return await interaction.followup.send(content=f"{message}", ephemeral=ephemeral)
            return await interaction.response.send_message(content=f"{message}", ephemeral=ephemeral
            )
