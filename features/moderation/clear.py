
from discord.ext import commands
import asyncio

class Clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="clear", aliases=["purge"])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        """
        Clears a specified number of messages.
        Usage: !clear <amount>
        """
        if amount < 1:
            
            await ctx.send("Please specify a number greater than 0.")
            return

        # Purge messages
        deleted = await ctx.channel.purge(limit=amount + 1) # +1 to include the command message itself
        
        # Send confirmation and delete it after 3 seconds
        msg = await ctx.send(f"🗑️ Deleted {len(deleted) - 1} messages.")
        await asyncio.sleep(3)
        await msg.delete()

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("⛔ You do not have permission to manage messages.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Usage: `!clear <amount>`")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please provide a valid number.")

async def setup(bot):
    await bot.add_cog(Clear(bot))
