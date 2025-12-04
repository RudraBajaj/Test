import discord
from discord.ext import commands

class HelpView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60) # Buttons stop working after 60 seconds

    async def update_embed(self, interaction, title, description, color):
        embed = discord.Embed(title=title, description=description, color=color)
        embed.set_footer(text="Developed by Rudra")
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="🏠 Home", style=discord.ButtonStyle.primary)
    async def home_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.update_embed(
            interaction,
            "🐺 Madwolf Bot Help",
            "Select a category below to see commands.",
            discord.Color.purple()
        )

    @discord.ui.button(label="🎉 Fun", style=discord.ButtonStyle.success)
    async def fun_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.update_embed(
            interaction,
            "🎉 Fun Commands",
            "`Hii` - Say hello\n`@Madwolf` - Tag me for a reply",
            discord.Color.green()
        )

    @discord.ui.button(label="🛡️ Moderation", style=discord.ButtonStyle.danger)
    async def mod_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.update_embed(
            interaction,
            "🛡️ Moderation Commands",
            "`!spam <count> <msg>` - Spam a message (Admin only)\n`!clear <amount>` - Delete messages (Manage Msgs only)",
            discord.Color.red()
        )
    
    @discord.ui.button(label="⚙️ System", style=discord.ButtonStyle.secondary)
    async def sys_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.update_embed(
            interaction,
            "⚙️ System Features",
            "**Welcome System**: Sends a card when users join.\n**Help**: This command.",
            discord.Color.light_grey()
        )
    
    @discord.ui.button(label="🎵 Music", style=discord.ButtonStyle.blurple)
    async def music_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.update_embed(
            interaction,
            "🎵 Music Commands",
            "`?join` - Join your voice channel\n`?play <song>` - Play a song from YouTube\n`?pause` - Pause playback\n`?resume` - Resume playback\n`?stop` - Stop and disconnect",
            discord.Color.blue()
        )

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help(self, ctx):
        """
        Shows the interactive help menu.
        """
        embed = discord.Embed(
            title="🐺 Madwolf Bot Help",
            description="Select a category below to see commands.",
            color=discord.Color.purple()
        )
        embed.set_footer(text="Developed by Rudra")
        
        await ctx.send(embed=embed, view=HelpView())

async def setup(bot):
    # Remove the default help command so we can use our own
    # (Already removed in main.py, but good practice to check)
    if bot.help_command:
        bot.remove_command('help')
    await bot.add_cog(Help(bot))
