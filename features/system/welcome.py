import discord
from discord.ext import commands
import os

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        # Get the welcome channel ID from .env
        welcome_channel_id = os.getenv('WELCOME_CHANNEL_ID')
        
        if welcome_channel_id:
            try:
                channel = self.bot.get_channel(int(welcome_channel_id))
                if channel:
                    # Get other channel IDs from .env for the links
                    role_channel_id = os.getenv('ROLE_CHANNEL_ID')
                    rules_channel_id = os.getenv('RULES_CHANNEL_ID')
                    complaints_channel_id = os.getenv('COMPLAINTS_CHANNEL_ID')

                    # Helper function to format channel link or fallback to text
                    def get_link(c_id, text):
                        return f"<#{c_id}>" if c_id else f"**{text}**"

                    # Create a stylish embed matching the user's request
                    embed = discord.Embed(
                        description=f"↪ **Welcome To Our Server**\n\n"
                                    f"☾ {get_link(role_channel_id, 'Self Roles')}\n"
                                    f"☾ {get_link(rules_channel_id, 'Read Rules')}\n"
                                    f"☾ {get_link(complaints_channel_id, 'For Any Complains')}\n\n"
                                    f"**Enjoy Your Stay Here !**",
                        color=discord.Color.dark_theme() # Using a dark color to match the image
                    )
                    
                    # Set user's avatar as thumbnail (Image on the right)
                    if member.avatar:
                        embed.set_thumbnail(url=member.avatar.url)
                    
                    # Optional: Set the author to the user's name
                    embed.set_author(name=f"{member.name}", icon_url=member.avatar.url if member.avatar else None)

                    await channel.send(f"Welcome {member.mention} <3", embed=embed)
                else:
                    print(f"Could not find welcome channel with ID {welcome_channel_id}")
            except ValueError:
                print("Invalid WELCOME_CHANNEL_ID in .env")

async def setup(bot):
    await bot.add_cog(Welcome(bot))
