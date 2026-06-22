from discord import ButtonStyle, Integration
from discord.ui import View, button, Button

class ArchiveView(View):
    @button(label="Yes", style=ButtonStyle.green, emoji="✅")
    async def stop(self, interaction: Integration, button: Button):
        await interaction.response.edit_message(content="Game stopped", view=None)

    @button(label="No", style=ButtonStyle.red, emoji="❌")
    async def stop(self, interaction: Integration, button: Button):
        await interaction.response.edit_message(content="Game stopped", view=None)