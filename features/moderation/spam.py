
from discord.ext import commands
import asyncio

class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="spam")
    @commands.has_permissions(administrator=True)
    async def spam(self, ctx, count: int, *, message: str):
        """
        Spams a message a specific number of times.
        Usage: !spam <count> <message>
        Example: !spam 5 Hello World
        """
        # Check if count is within range
        if count < 2 or count > 100:
            await ctx.send("❌ Please provide a number between 2 and 100.")
            return

        # Send the messages
        for i in range(count):
            await ctx.send(message)
            # Add a tiny delay to prevent rate limiting issues (optional but good practice)
            await asyncio.sleep(0.5)

    @spam.error
    async def spam_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("⛔ You do not have permission to use this command. (Admin only)")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Usage: `!spam <count> <message>`\nExample: `!spam 5 Hello`")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please provide a valid number.")

async def setup(bot):
    await bot.add_cog(Utilities(bot))
