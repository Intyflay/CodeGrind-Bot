import discord

from src.ui.embeds.roles import roles_created_embed, roles_removed_embed
from src.utils.roles import create_roles, remove_roles, update_roles


class RolesView(discord.ui.View):
    @discord.ui.button(label="Enable", style=discord.ButtonStyle.blurple)
    async def enable(
        self, interaction: discord.Interaction, _: discord.ui.Button
    ) -> None:
        await interaction.response.defer()

        await create_roles(interaction.guild)
        await update_roles(interaction.guild, interaction.guild.id)

        await interaction.followup.send(embed=roles_created_embed())

    @discord.ui.button(label="Disable", style=discord.ButtonStyle.gray)
    async def disable(
        self, interaction: discord.Interaction, _: discord.ui.Button
    ) -> None:
        await interaction.response.defer()

        await remove_roles(interaction.guild)

        await interaction.followup.send(embed=roles_removed_embed())
