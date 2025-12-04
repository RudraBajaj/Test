"""Music player UI controls - Interactive buttons for playback control"""
import discord


class MusicButtons(discord.ui.View):
    """Interactive music control buttons"""
    
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="⏸️ Pause", style=discord.ButtonStyle.primary, custom_id="pause_button")
    async def pause_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.guild.voice_client and interaction.guild.voice_client.is_playing():
            interaction.guild.voice_client.pause()
            await interaction.response.send_message("⏸️ Paused", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Nothing is playing!", ephemeral=True)

    @discord.ui.button(label="▶️ Resume", style=discord.ButtonStyle.success, custom_id="resume_button")
    async def resume_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.guild.voice_client and interaction.guild.voice_client.is_paused():
            interaction.guild.voice_client.resume()
            await interaction.response.send_message("▶️ Resumed", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Nothing is paused!", ephemeral=True)

    @discord.ui.button(label="⏹️ Stop", style=discord.ButtonStyle.danger, custom_id="stop_button")
    async def stop_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.guild.voice_client:
            interaction.guild.voice_client.stop()
            await interaction.response.send_message("⏹️ Stopped", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Not playing anything!", ephemeral=True)

    @discord.ui.button(label="👋 Leave", style=discord.ButtonStyle.grey, custom_id="leave_button")
    async def leave_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.guild.voice_client:
            await interaction.guild.voice_client.disconnect()
            await interaction.response.send_message("👋 Disconnected", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Not in voice!", ephemeral=True)
