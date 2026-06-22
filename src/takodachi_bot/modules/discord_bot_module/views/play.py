from discord import ButtonStyle, Integration
from discord.ui import View, button, Button

class PlayView(View):
    @button(label="stop", style=ButtonStyle.red, emoji="✅")
    async def stop(self, interaction: Integration, button: Button):
        await interaction.response.edit_message(content="Game stopped", view=None)