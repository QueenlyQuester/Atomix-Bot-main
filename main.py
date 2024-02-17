from __future__ import annotations
import discord, asyncio
from core import Bot
from config import TOKEN


async def main():
    discord.utils.setup_logging()
    async with Bot() as bot:
        await bot.start(TOKEN, reconnect=True)
        
    
if __name__ == "__main__":
    asyncio.run(main())