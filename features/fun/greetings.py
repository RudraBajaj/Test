import discord
from discord.ext import commands

class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # This event runs every time a message is sent in a channel the bot can see
    @commands.Cog.listener()
    async def on_message(self, message):
        # Check if the message was sent by the bot itself
        if message.author == self.bot.user:
            return

        content = message.content.lower()

        # Check if the message contains "hii"
        if "hii" in content:
            await message.channel.send("Hello! How are you?")
        
        if "ayush" in content:
            await message.channel.send("```Mera lawda haha```")

        # Check if the bot is mentioned (tagged) in the message
        if self.bot.user in message.mentions:
            await message.channel.send("```You tagged me! How can I help?```")

# This function is needed to load the Cog
async def setup(bot):
    await bot.add_cog(Greetings(bot))
