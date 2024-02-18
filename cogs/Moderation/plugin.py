from __future__ import annotations
import os
import sys
from click import Context

import discord
from core import Bot
from datetime import timedelta
from discord import app_commands, Interaction, Member, TextChannel, User, utils as Utils
from humanfriendly import parse_timespan, InvalidTimespan
from typing import Literal, Optional
from .. import Plugin


def can_moderate():
    async def predicate(interaction: Interaction):
        target: Member = interaction.namespace.member or interaction.namespace.target
        if not target: 
            return True
        if interaction.guild is None:
            raise ValueError("Interaction must be in a guild")
        if not isinstance(interaction.user, Member):
            raise ValueError("Interaction user must be a Member")

        if(
            target.top_role.position > interaction.user.top_role.position
            or target.guild_permissions.kick_members
            or target.guild_permissions.ban_members
            or target.guild_permissions.manage_guild
        ):
            raise app_commands.CheckFailure(f"You can't moderate {target}")
        
        return True
    return app_commands.check(predicate)



class Moderate(Plugin):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        
    
    
    @app_commands.command(
        name="kick",
        description="kick a member from the server."
    )
    @app_commands.default_permissions(kick_members=True)
    @app_commands.describe(member="Select a member to kick from the server.",
    reason="Reason for kicking this user.")
    @app_commands.guild_only()
    async def kick_command(self, interaction: Interaction, member: Member, reason: 
    Optional[str]):
        if not reason: reason = "No reason provided."
        try:
            await member.kick(reason=reason)
        except:
            await self.bot.error(f"I'm not able to kick {member} from the server.",
            interaction)
        else:
            await self.bot.succes(
                f"Successfully kicked {member} from the server.", interaction
            )
            
            
    @app_commands.command(
        name="ban",
        description="ban a member from the server."
    )
    @app_commands.default_permissions(ban_members=True)
    @can_moderate()
    @app_commands.describe(member="Select a member to ban.", reason="Reason for a ban")
    @app_commands.guild_only()
    async def ban_command(self, interaction: Interaction, member: Member, reason: Optional[str]):
        if not reason: reason = "No reason provided."
        try:
            await member.ban(reason=reason)
        except:
            await self.bot.error(f"I'm not able to ban {member} from the server.",
            interaction)
        else:
            await self.bot.succes(
                f"Successfully banned {member} from the server.", interaction
            )
            
    @app_commands.command(
        name="unban",
        description="unban a member from the server."
    )
    @app_commands.default_permissions(ban_members=True)
    @can_moderate()
    @app_commands.describe(user="Provide user id to unban", reason="Reason for unban")
    @app_commands.guild_only()
    async def unban_command(self, interaction: Interaction, user: User, reason: Optional[str]):
        if not reason: reason = "No reason provided."
        assert interaction.guild is not None
        try:
            await interaction.guild.fetch_ban(user)
        except:
            await self.bot.error(f"{user} is not banned from the server.", interaction)
        else:
            try:
                await interaction.guild.unban(user, reason=reason)
            except:
                await self.bot.error(f"I'm not able to unban {user} from the server.", interaction)
            else:
                await self.bot.succes(f"Successfully unbanned {user} from the server.", interaction)
    
    
    
    @app_commands.command(name="mute", description="Mute a member.")       
    @app_commands.default_permissions(moderate_members=True)
    @can_moderate()
    @app_commands.describe(
        target="Please select a member to mute.", 
        duration="Duration of the mute. (1d, 1m, 10s)",
        reason="Reason for the mute."
    )
    async def mute_command(
        self,
        interaction: Interaction,
        target: Member,
        duration: Optional[str],
        reason: Optional[str]
    ):
        
        if not duration:
            duration = "1d"
        try:
            real_duration = parse_timespan(duration)
        except InvalidTimespan:
            await self.bot.error(
                f"**{duration}** is not valid",
                interaction
            )
        
        else:
            try:
                await target.timeout(
                    Utils.utcnow() + timedelta(seconds=real_duration) , reason=reason
                )
            except:
                self.bot.error(f"I'm not able to timeout {target}", interaction)
            else:
                await self.bot.success(f"Successfully muted **{target}** for **{duration}**", interaction)
         
     
     
     
    @app_commands.command(name="unmute", description="Unmute a member.")       
    @app_commands.default_permissions(moderate_members=True)
    @can_moderate()
    @app_commands.describe(
        target="Please select a member to unmute.", 
        reason="Reason for the unmute."
    )
    async def unmute_command(
        self,
        interaction: Interaction,
        target: Member,
        reason: Optional[str]
    ):     
        if not target.is_timed_out():
            return await self.bot.error(f"**{target}** is not muted.", interaction)
        try:
            await target.timeout(None, reason=reason)
        except:
            await self.bot.error(f"I'm not able to unmute {target}", interaction)
        else:
            await self.bot.success(f"Successfully unmuted **{target}**", interaction)
            
            
            
            
    #====================== Clear Messages ===================
 
    
    
    @app_commands.command(name="clear", description="Clears console messages")
    async def clear(self, interaction: discord.Interaction):
        if interaction.user.id != interaction.guild.owner_id:
            return await interaction.response.send_message("Only the server owner can use this command.")

        os.system("cls")
        embed = discord.Embed(
            title="Console Cleared",
            color=discord.Color.red(),
        )
        embed.description = "The console has been cleared!"
        await interaction.response.send_message(embed=embed)
        
    @app_commands.command(name="purge", description="Purges messages in a channel.")
    @app_commands.default_permissions(manage_messages=True)
    @app_commands.describe(
        channel="Channel to purge messages in.",
        amount="Number of messages to purge."
    )
    async def purge_command(
        self,
        interaction: Interaction,
        channel: TextChannel,
        amount: int
    ):
        if not isinstance(channel, TextChannel):
            await self.bot.error("Invalid channel provided", interaction)
            return
        if amount <= 0:
            await self.bot.error("Invalid amount. Please provide a positive integer.", interaction)
            return
        try:
            await channel.purge(limit=amount)
        except Exception as e:
            await self.bot.error(f"Unable to purge messages: {e}", interaction)
        else:
            await self.bot.success(f"Purged {amount} messages in {channel}", interaction)
            
    

            
    #====================== Lock Channel ===================
    
    @app_commands.command(
        name="lock",
        description="Lock the channel."
    )      
    @app_commands.describe(
        channel="Select a channel you want to lock."
    )
    @app_commands.guild_only()
    @app_commands.default_permissions(manage_channels=True)
    async def lock_command(self, interaction: Interaction, channel: Optional[TextChannel]):
        target = channel or interaction.channel
        assert interaction.guild is not None and isinstance(target, TextChannel)
        try:
            await target.set_permissions(interaction.guild.default_role, send_messages=False)
        except:
            await self.bot.error(f"I'm not able to lock {target} channel.", interaction)
        else:
            await self.bot.success(f"Successfully locked **{target}** channel.", interaction)

    @app_commands.command(
        name="unlock",
        description="Unlock the channel."
    )      
    @app_commands.describe(
        channel="Select a channel you want to unlock."
    )
    @app_commands.guild_only()
    @app_commands.default_permissions(manage_channels=True)
    async def unlock_command(self, interaction: Interaction, channel: Optional[TextChannel]):
        target = channel or interaction.channel
        assert interaction.guild is not None and isinstance(target, TextChannel)
        try:
            await target.set_permissions(interaction.guild.default_role, send_messages=True)
        except:
            await self.bot.error(f"I'm not able to unlock {target} channel.", interaction)
        else:
            await self.bot.success(f"Successfully unlocked **{target}** channel.", interaction)
            
        
    #====================== Restart the Bot ===================
    
    @app_commands.command(name="restart", description="Restart the bot")
    @app_commands.default_permissions(administrator=True)  
    async def restart(self, interaction: Interaction):

        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You do not have permissions to use this command")
            return

        embed = discord.Embed(title="Restarting...", color=discord.Color.orange())
        await interaction.response.send_message(embed=embed)

        try:
            restart_script = "main.py"
            print(f"Restarting with: {sys.executable}")
            try:
                os.execv(sys.executable, [sys.executable, restart_script])  
            except Exception as e:
                print(f"Restart failed: {e}")
                embed = discord.Embed(title="Restart failed", description=str(e))
                await interaction.followup.send(embed=embed)
                raise e
        except Exception as e:
            print(f"Error closing client: {e}")
            embed = discord.Embed(title="Restart failed", description=str(e))
            await interaction.followup.send(embed=embed)
            raise e
        finally:
            print("Bot has been restarted")

   
async def setup(bot: Bot):
    await bot.add_cog(Moderate(bot))
