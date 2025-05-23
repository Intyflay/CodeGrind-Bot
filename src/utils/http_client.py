import asyncio
from random import random
from typing import TYPE_CHECKING

import aiohttp
import backoff

if TYPE_CHECKING:
    # To prevent circular imports
    from src.bot import DiscordBot

http_post_semaphore = asyncio.Semaphore(4)


class RateLimitExceededException(Exception):
    def __init__(self) -> None:
        super().__init__("RateLimitExceededException. Error: 429. Rate Limited.")


class HttpClient:
    def __init__(self, bot: "DiscordBot", session: aiohttp.ClientSession) -> None:
        self.bot = bot
        self.session = session

    async def fetch_data(self, *args, **kwargs) -> str | None:
        """
        Executes a GET request and handles any client errors.

        :return: The response text if the request is successful, otherwise None.
        """
        try:
            async with self.session.get(*args, **kwargs) as response:
                match response.status:
                    case 200:
                        return await response.text()
                    case _:
                        self.bot.logger.exception(
                            f"Failed to fetch data: (code: {response.status})"
                        )

        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            self.bot.logger.exception(f"Failed to fetch data: {e}")

    @backoff.on_exception(backoff.expo, RateLimitExceededException, logger=None)
    async def post_data(self, *args, **kwargs) -> dict | None:
        """
        Executes a POST request with rate limit handling and error logging.

        :return: The response JSON if the request is successful, otherwise None.
        """
        async with http_post_semaphore:
            try:
                async with self.session.post(*args, **kwargs) as response:
                    match response.status:
                        case 200:
                            # Add a small delay to avoid rate limits, using random to
                            # avoid patterns.
                            # TODO: Look into whether this is necessary:
                            # increases overall execution time but decreases the
                            # number of rate limited requests.
                            await asyncio.sleep(random())
                            return await response.json()
                        case 429:
                            self.bot.channel_logger.rate_limited()
                            raise RateLimitExceededException()
                        case 403:
                            self.bot.logger.exception(
                                f"Post request forbidden access "
                                f"(code: {response.status})",
                            )
                            self.bot.channel_logger.forbidden()
                        case _:
                            self.bot.logger.exception(
                                f"Post request error: (code: {response.status})"
                            )

            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                self.bot.logger.exception(f"Failed to post data: {e}")
