import random
import string
from typing import TYPE_CHECKING

import discord

from src.constants import StatsCardExtensions
from src.ui.embeds.common import error_embed, failure_embed
from src.utils.stats import stats_card

if TYPE_CHECKING:
    # To prevent circular imports
    from src.bot import DiscordBot


async def stats_embed(
    bot: "DiscordBot",
    leetcode_id: str,
    display_name: str,
    display_url: bool,
    extension: StatsCardExtensions,
) -> tuple[discord.Embed, discord.File | None]:
    # Use a randomised filename for privacy.
    filename = "".join(random.choices(string.ascii_letters + string.digits, k=25))

    file = await stats_card(bot, leetcode_id, filename, extension, display_url)

    if not file:
        return error_embed(), None

    embed = discord.Embed(
        title=display_name,
        url=f"https://leetcode.com/{leetcode_id}" if display_url else None,
        colour=discord.Colour.orange(),
    )
    embed.set_image(url=f"attachment://{filename}.png")

    return embed, file


def invalid_username_embed() -> discord.Embed:
    return error_embed(description="The username you entered is invalid")


def account_hidden_embed() -> discord.Embed:
    return failure_embed(
        title="Cannot access data",
        description="The user has chosen not to make their LeetCode account public",
    )
