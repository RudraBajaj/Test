import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from connection.keep_alive import keep_alive

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

if TOKEN is None:
    print("Error: DISCORD_TOKEN not found in .env file.")
    print("Please make sure you created the .env file and put your token in it.")
    exit()

intents = discord.Intents.default()
intents.members = True 
intents.message_content = True
intents.voice_states = True
intents.guilds = True

bot = commands.Bot(command_prefix='?', intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print('Bot is ready to use!')
    
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.streaming, name="Level Graph by Navaan Sandhu", url="https://youtu.be/GUePGok8QrA?si=zl-1T898mxUyoSDj"))
    
    log_channel_id = 1358552860811329638
    if log_channel_id:
        try:
            channel = bot.get_channel(int(log_channel_id))
            if channel:
                await channel.send("I am Alive! 🟢")
            else:
                print(f"Could not find channel with ID {log_channel_id}")
        except ValueError:
            print("Invalid LOG_CHANNEL_ID in .env")
    else:
        print("LOG_CHANNEL_ID not found in .env (Skipping startup message)")
    
    try:
        await bot.load_extension('features.fun.greetings')
        print("Loaded extension: features.fun.greetings")
    except Exception as e:
        print(f"Failed to load extension features.fun.greetings: {e}")

    try:
        await bot.load_extension('features.moderation.spam')
        print("Loaded extension: features.moderation.spam")
    except Exception as e:
        print(f"Failed to load extension features.moderation.spam: {e}")

    try:
        await bot.load_extension('features.moderation.clear')
        print("Loaded extension: features.moderation.clear")
    except Exception as e:
        print(f"Failed to load extension features.moderation.clear: {e}")

    try:
        await bot.load_extension('features.system.help')
        print("Loaded extension: features.system.help")
    except Exception as e:
        print(f"Failed to load extension features.system.help: {e}")

    try:
        await bot.load_extension('features.system.welcome')
        print("Loaded extension: features.system.welcome")
    except Exception as e:
        print(f"Failed to load extension features.system.welcome: {e}")


if __name__ == '__main__':
    keep_alive()
    try:
        bot.run(TOKEN)
    except discord.errors.LoginFailure:
        print("Error: Invalid Token. Please check your .env file.")

