"""Music player main cog - Simple, reliable YouTube playback"""
import discord
from discord.ext import commands
import asyncio
import os

from .controls import MusicButtons
from .utils import extract_info, download_audio


class MusicPlayer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.current = None

    @commands.command(name="join", aliases=['connect'])
    async def join(self, ctx):
        """Joins your voice channel. Usage: !join"""
        if not ctx.author.voice:
            return await ctx.send("❌ You need to be in a voice channel!")

        channel = ctx.author.voice.channel
        
        try:
            if ctx.voice_client:
                await ctx.voice_client.move_to(channel)
                embed = discord.Embed(description=f"🔊 Moved to {channel.name}!", color=discord.Color.green())
            else:
                await channel.connect(timeout=60.0, reconnect=True)
                embed = discord.Embed(description=f"🔊 Joined {channel.name}!", color=discord.Color.green())
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"❌ Connection failed: {str(e)}")

    @commands.command(name="play", aliases=['p'])
    async def play(self, ctx, *, search: str):
        """Plays from YouTube. Usage: !play <song name or URL>"""
        if not ctx.author.voice:
            return await ctx.send("❌ Join a voice channel first!")

        # Auto-join
        if not ctx.voice_client:
            try:
                await ctx.author.voice.channel.connect(timeout=60.0, reconnect=True)
            except:
                return await ctx.send("❌ Couldn't join voice channel!")

        # Check if already playing
        if ctx.voice_client.is_playing():
            return await ctx.send("⚠️ Already playing! Use `!stop` first.")

        # Show searching message
        searching_msg = await ctx.send(f"🔎 **Searching** for `{search}`...")

        try:
            # Extract video info
            data = await extract_info(search)
            
            if not data:
                await searching_msg.delete()
                await ctx.send("❌ Could not find that song.")
                return

            # Get song details
            title = data.get('title', 'Unknown')
            thumbnail = data.get('thumbnail')
            duration = data.get('duration', 0)
            video_id = data.get('id', 'unknown')

            await searching_msg.edit(content=f"⬇️ **Downloading** {title}...")

            # Download audio to /tmp (optimized for low CPU/RAM)
            audio_file = await download_audio(data, video_id)
            
            if not audio_file or not os.path.exists(audio_file):
                await searching_msg.delete()
                await ctx.send("❌ Failed to download audio.")
                return

            await searching_msg.delete()

            # Play from local file (100% reliable, no segments)
            def after_playing(error):
                if error:
                    print(f'Player error: {error}')
                # Delete file after playback
                try:
                    if os.path.exists(audio_file):
                        os.remove(audio_file)
                        print(f"Deleted: {audio_file}")
                except Exception as e:
                    print(f"Cleanup error: {e}")
                
                self.current = None

            source = discord.FFmpegOpusAudio(audio_file)
            ctx.voice_client.play(source, after=after_playing)
            
            self.current = title

            # Create now playing embed
            embed = discord.Embed(
                title="🎵 Now Playing",
                description=f"**{title}**",
                color=discord.Color.blue()
            )
            
            if thumbnail:
                embed.set_thumbnail(url=thumbnail)
            
            if duration:
                minutes = duration // 60
                seconds = duration % 60
                embed.add_field(name="Duration", value=f"{minutes}:{seconds:02d}", inline=True)
            
            embed.add_field(name="Requested by", value=ctx.author.mention, inline=True)
            
            # Add interactive buttons
            view = MusicButtons()
            await ctx.send(embed=embed, view=view)

        except Exception as e:
            try:
                await searching_msg.delete()
            except:
                pass
                
            print(f"Play error: {e}")
            await ctx.send(f"❌ Error: {str(e)}")

    @commands.command(name="stop")
    async def stop(self, ctx):
        """Stops and disconnects! Usage: !stop"""
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            self.current = None
            await ctx.send(embed=discord.Embed(description="⏹️ Stopped!", color=discord.Color.red()))
        else:
            await ctx.send("❌ Not in voice!")

    @commands.command(name="pause")
    async def pause(self, ctx):
        """Pauses playback. Usage: !pause"""
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send(embed=discord.Embed(description="⏸️ Paused", color=discord.Color.yellow()))
        else:
            await ctx.send("❌ Nothing playing!")

    @commands.command(name="resume")
    async def resume(self, ctx):
        """Resumes playback. Usage: !resume"""
        if ctx.voice_client and ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send(embed=discord.Embed(description="▶️ Resumed", color=discord.Color.green()))
        else:
            await ctx.send("❌ Nothing paused!")
    
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """Auto-disconnect if alone"""
        if member.id == self.bot.user.id:
            return
        
        vc = member.guild.voice_client
        if vc and vc.channel:
            members = [m for m in vc.channel.members if not m.bot]
            if len(members) == 0 and vc.is_connected():
                await asyncio.sleep(60)
                members = [m for m in vc.channel.members if not m.bot]
                if len(members) == 0:
                    await vc.disconnect()


async def setup(bot):
    await bot.add_cog(MusicPlayer(bot))
