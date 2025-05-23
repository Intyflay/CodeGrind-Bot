from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands

from src.middleware import defer_interaction
from src.ui.embeds.general import help_embed
from src.ui.views.general import CommandCategorySelectView

if TYPE_CHECKING:
    # To prevent circular imports
    from src.bot import DiscordBot


class GeneralCog(commands.Cog):
    def __init__(self, bot: "DiscordBot") -> None:
        self.bot = bot

    @app_commands.command(name="help")
    @defer_interaction(ephemeral_default=True)
    async def help(self, interaction: discord.Interaction) -> None:
        """
        Get help with CodeGrind Bot commands
        """
        embed = help_embed()
        embed.set_footer(text="Love our bot? Vote on top.gg using /vote")

        await interaction.followup.send(embed=embed, view=CommandCategorySelectView())

    @app_commands.command(name="vote")
    @defer_interaction(ephemeral_default=True)
    async def vote(self, interaction: discord.Interaction) -> None:
        """
        Vote for CodeGrind Bot on top.gg
        """
        embed = discord.Embed(
            title="Vote for CodeGrind Bot on top.gg ",
            description="https://top.gg/bot/1059122559066570885/vote",
            colour=discord.Colour.purple(),
        )

        await interaction.followup.send(embed=embed)


async def setup(bot: "DiscordBot") -> None:
    await bot.add_cog(GeneralCog(bot))
