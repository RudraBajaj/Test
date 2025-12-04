# Import the discord library to use its features
import discord
# Import the commands extension to create bot commands easily
from discord.ext import commands
# Import os to interact with the operating system (like reading files)
import os
# Import load_dotenv to read the .env file
from dotenv import load_dotenv
# Import the keep_alive function from our new folder
from connection.keep_alive import keep_alive

# Load the variables from the .env file into the program
load_dotenv()

# Get the token from the environment variables
TOKEN = os.getenv('DISCORD_TOKEN')

# Check if the token was found
if TOKEN is None:
    print("Error: DISCORD_TOKEN not found in .env file.")
    print("Please make sure you created the .env file and put your token in it.")
    exit()

# Create cookies.txt from environment variable (for Render deployment)
COOKIES_CONTENT = os.getenv('YOUTUBE_COOKIES')
if COOKIES_CONTENT:
    print("Found YOUTUBE_COOKIES env var, creating cookies.txt...")
    with open('cookies.txt', 'w') as f:
        f.write(COOKIES_CONTENT)
    print("Successfully created cookies.txt")
else:
    print("Warning: YOUTUBE_COOKIES not found. Music might fail.")

# Set up the "intents" for the bot.
intents = discord.Intents.default()
intents.members = True 
intents.message_content = True
intents.voice_states = True  # Required for voice connections
intents.guilds = True  # Required for guild info 

# Create the bot instance
bot = commands.Bot(command_prefix='?', intents=intents, help_command=None)

# This event runs when the bot has successfully connected to Discord
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print('Bot is ready to use!')
    
    # Set the bot's status
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.streaming, name="Level Graph by Navaan Sandhu", url="https://youtu.be/GUePGok8QrA?si=zl-1T898mxUyoSDj"))
    
    # Send "I am Alive" message to a specific channel
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
    
    # Load the greetings feature (Fun)
    try:
        await bot.load_extension('features.fun.greetings')
        print("Loaded extension: features.fun.greetings")
    except Exception as e:
        print(f"Failed to load extension features.fun.greetings: {e}")

    # Load the spam command (Moderation)
    try:
        await bot.load_extension('features.moderation.spam')
        print("Loaded extension: features.moderation.spam")
    except Exception as e:
        print(f"Failed to load extension features.moderation.spam: {e}")

    # Load the clear command (Moderation)
    try:
        await bot.load_extension('features.moderation.clear')
        print("Loaded extension: features.moderation.clear")
    except Exception as e:
        print(f"Failed to load extension features.moderation.clear: {e}")

    # Load the help command (System)
    try:
        await bot.load_extension('features.system.help')
        print("Loaded extension: features.system.help")
    except Exception as e:
        print(f"Failed to load extension features.system.help: {e}")

    # Load the welcome feature (System)
    try:
        await bot.load_extension('features.system.welcome')
        print("Loaded extension: features.system.welcome")
    except Exception as e:
        print(f"Failed to load extension features.system.welcome: {e}")

    # Load the music player (Music)
    try:
        await bot.load_extension('features.music.player')
        print("Loaded extension: features.music.player")
    except Exception as e:
        print(f"Failed to load extension features.music.player: {e}")

# Run the bot with the token
if __name__ == '__main__':
    keep_alive() # Start the web server
    try:
        bot.run(TOKEN)
    except discord.errors.LoginFailure:
        print("Error: Invalid Token. Please check your .env file.")

