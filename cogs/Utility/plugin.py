from  __future__ import annotations
from core import Bot, Embed 
from .. import Plugin
from discord import Interaction, app_commands, Member
import discord
import config


class Utility(Plugin):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        
    @app_commands.command(name="ping", description="See bot's latency")
    async def ping_command(self, interaction: Interaction):
        embed=Embed(description=f"My ping is {round(self.bot.latency * 1000)}ms")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="serverinfo", description="Get info about the current server")
    async def server_info_command(self, interaction: Interaction):
        guild = interaction.guild
        embed = Embed(title=f"Server Info - {guild.name}")
        embed.add_field(name="ID", value=guild.id)
        embed.add_field(name="Owner", value=guild.owner)
        embed.add_field(name="Member Count", value=guild.member_count) 
        embed.add_field(name="Creation Date", value=guild.created_at.strftime("%b %d, %Y %I:%M %p"))
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="userinfo", description="Get info about yourself or another user")
    async def user_info_command(self, interaction: Interaction, user: discord.Member=None):
        user = user or interaction.user
        embed = Embed(title=f"User Info - {user.name}")
        embed.add_field(name="ID", value=user.id) 
        embed.add_field(name="Joined", value=user.joined_at)
        await interaction.response.send_message(embed=embed)
        
        
    async def member_on_join(self, member: Member):

        try:
            channel_id = config.JOIN_CHANNEL_ID
            channel = self.bot.get_channel(channel_id)

            if not channel:
                print(f"Channel {channel_id} not found")
                return

            embed = Embed(title="New Member Joined!", 
                description=f"{member.mention} just joined the server!")

            await channel.send(embed=embed)

        except Exception as e:
            print(f"Error sending join message: {e}")
            
            
    @app_commands.command(name="roleinfo", description="Get info about a role")
    async def role_info_command(self, interaction: Interaction, role: discord.Role):
        embed = Embed(title=f"Role Info - {role.name}")
        embed.add_field(name="ID", value=role.id)
        embed.add_field(name="Color", value=role.color)
        embed.add_field(name="Position", value=role.position)
        embed.add_field(name="Permissions", value=", ".join([perm for perm in role.permissions if perm]))
        await interaction.response.send_message(embed=embed)


    @app_commands.command(name="channelinfo", description="Get info about a text channel")  
    async def channel_info_command(self, interaction: Interaction, channel: discord.TextChannel):
        embed = Embed(title=f"Channel Info - {channel.name}")
        embed.add_field(name="ID", value=channel.id)
        embed.add_field(name="Category", value=channel.category) 
        embed.add_field(name="Position", value=channel.position)
        embed.add_field(name="NSFW", value=channel.is_nsfw())
        await interaction.response.send_message(embed=embed)
        
        
    @app_commands.command(name="avatar", description="Get a user's avatar")
    async def avatar(self, interaction: Interaction, user: discord.Member=None):
        user = user or interaction.user
        embed = Embed(title=f"Avatar for {user.name}")
        embed.set_image(url=user.avatar)
        await interaction.response.send_message(embed=embed)
        
        
        
    @app_commands.command(name="serverroles", description="List all roles on the server")
    async def server_roles_command(self, interaction: Interaction):
        guild = interaction.guild
        roles = ", ".join([role.name for role in guild.roles])
        embed = Embed(title=f"Roles in {guild.name}")
        embed.description = roles
        await interaction.response.send_message(embed=embed)


    @app_commands.command(name="channels", description="List all channels on the server")
    async def server_channels_command(self, interaction: Interaction):
        guild = interaction.guild
        channels = ", ".join([channel.name for channel in guild.channels]) 
        embed = Embed(title=f"Channels in {guild.name}")
        embed.description = channels
        await interaction.response.send_message(embed=embed)


    @app_commands.command(name="membercount", description="Get member count for a role")  
    async def member_count_command(self, interaction: Interaction, role: discord.Role):
        count = len([member for member in interaction.guild.members if role in member.roles])
        embed = Embed(title=f"Member Count for {role.name}")
        embed.add_field(name="Count", value=count)
        await interaction.response.send_message(embed=embed)
        
    @app_commands.command(name="invitelink", description="Get an invite link for the server")  
    async def invite_link_command(self, interaction: Interaction):
        invite = await interaction.channel.create_invite(max_age=3600)
        embed = Embed(title="Invite Link")
        embed.description = invite.url
        await interaction.response.send_message(embed=embed)
        
    @app_commands.command(name="memberlist", description="List all members of a role")
    async def member_list_command(self, interaction: Interaction, role: discord.Role):
        members = "\n".join([member.mention for member in interaction.guild.members if role in member.roles])
        embed = Embed(title=f"Members of {role.name}")
        embed.description = members 
        await interaction.response.send_message(embed=embed)
        
    @app_commands.command(name="botdetails", description="Get details about the bot")  
    async def get_bot_details(self, interaction: Interaction):
        bot = self.bot.user
        embed = Embed(title="Bot Info") 
        embed.add_field(name="Name", value=bot.name)
        embed.add_field(name="ID", value=bot.id)
        await interaction.response.send_message(embed=embed)
        
    @app_commands.command(name="emojis", description="List all emojis on the server")
    async def server_emojis_command(self, interaction: Interaction):
        guild = interaction.guild
        emojis = ", ".join([str(e) for e in guild.emojis])
        embed = Embed(title=f"Emojis in {guild.name}")
        embed.description = emojis
        await interaction.response.send_message(embed=embed)
        
    @app_commands.command(name="serverbanner", description="Get the banner image for the server")
    async def server_banner_command(self, interaction: Interaction):
        guild = interaction.guild
        embed = Embed(title=f"Banner for {guild.name}")
        if guild.banner:
            embed.set_image(url=guild.banner_url)
        else:
            embed.description = "No banner set"  
        await interaction.response.send_message(embed=embed)
        
    @app_commands.command(name="serverfeatures", description="List features enabled on the server")
    async def server_features_command(self, interaction: Interaction):
        guild = interaction.guild
        features = ", ".join(guild.features)
        embed = Embed(title=f"Features in {guild.name}")
        embed.description = features
        await interaction.response.send_message(embed=embed)


    @app_commands.command(name="memberjoined", description="Get when a member joined the server")  
    async def member_joined_command(self, interaction: Interaction, member: discord.Member):
        embed = Embed(title=f"Join Date for {member.name}")
        embed.add_field(name="Joined", value=member.joined_at)
        await interaction.response.send_message(embed=embed)
        
        
    @app_commands.command(name="membercountbystatus", description="Get member count filtered by status")
    async def member_count_by_status_command(self, interaction: Interaction, status: str):
        status = status.lower()
        if status == "online":
            status_filter = discord.Status.online
        elif status == "idle": 
            status_filter = discord.Status.idle
        elif status == "dnd":
            status_filter = discord.Status.dnd
        elif status == "offline":
            status_filter = discord.Status.offline
        else:
            await interaction.response.send_message("Invalid status")
            return

        count = len([m for m in interaction.guild.members if m.status == status_filter])
        embed = Embed(title=f"Member Count with Status: {status}")
        embed.add_field(name="Count", value=count)
        await interaction.response.send_message(embed=embed)
        
    @app_commands.command(name="serverchannelsbytype", description="List channels by type")
    async def server_channels_by_type_command(self, interaction: Interaction):
        guild = interaction.guild

        text_channels = ", ".join([channel.name for channel in guild.text_channels])
        voice_channels = ", ".join([channel.name for channel in guild.voice_channels])
        category_channels = ", ".join([channel.name for channel in guild.categories])

        embed = Embed(title=f"Channels in {guild.name} by Type")
        embed.add_field(name="Text Channels", value=text_channels)
        embed.add_field(name="Voice Channels", value=voice_channels) 
        embed.add_field(name="Category Channels", value=category_channels)

        await interaction.response.send_message(embed=embed)
        
async def setup(bot: Bot) -> None:
  utility = Utility(bot) 
  await bot.add_cog(utility)
  bot.add_listener(utility.member_on_join, "on_member_join")





