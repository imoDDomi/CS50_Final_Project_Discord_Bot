from redbot.core import commands
import asyncpraw
import asyncio
import random
from discord.ext import tasks
import pytz
from datetime import datetime, time, timedelta
import discord

class Memes(commands.Cog):
    """Discord Bot für de Jungs"""

    def __init__(self, bot):
        self.bot = bot
        self.reddit = None
        self.bot.loop.create_task(self.start_bot())
        
        # set channel you want the bot to post in daily
        self.channel_id = 1143295869475622953

        # set your id and secret from reddit
        self.praw_client_id = "5PLfZs16g96Iw150I3La8A"
        self.praw_client_secret = "9grVLdIRu4h8sCKpDp6OooslxZGroA"
        self.praw_user_agent = "MemesImgScraper"

    async def start_bot(self):
        await self.bot.wait_until_ready()
        self.reddit = self.create_reddit_instance()
        await self.schedule_next_post()
        if not self.daily_post.is_running():
            self.daily_post.start()

    def cog_unload(self):
        if self.reddit:
            self.bot.loop.create_task(self.reddit.close())
        self.daily_post.cancel()

    async def schedule_next_post(self):
        now = datetime.now(pytz.timezone('Europe/Berlin'))
        target_time = time(22, 41, tzinfo=now.tzinfo)
        next_post_time = datetime.combine(now.date(), target_time)
        if now.time() > target_time:
            next_post_time += timedelta(days=1)
        wait_time = (next_post_time - now).seconds
        await asyncio.sleep(wait_time)

    @tasks.loop(hours=24)
    async def daily_post(self, channel_id):
        channel = self.bot.get_channel(channel_id)
        await self.send_random_post(channel, "dankmemes")

    async def send_random_post(self, channel, subreddit_name):
        if not await self.is_subreddit_valid(subreddit_name):
            await channel.send("Dieser Subreddit existiert nicht.")
            return

        post_url = await self.get_random_post(subreddit_name)
        if post_url:
            await channel.send(post_url)
        else:
            await channel.send("Konnte keinen passenden Post finden.")

    async def get_random_post(self, subreddit_name):
        subreddit = await self.reddit.subreddit(subreddit_name)
        posts = []
        async for post in subreddit.hot(limit=100):
            if post.url.endswith(("png", "jpg", "gif", "mp4")):
                posts.append(post.url)
        return random.choice(posts) if posts else None

    async def is_subreddit_valid(self, subreddit_name):
        try:
            subreddit = await self.reddit.subreddit(subreddit_name)
            await subreddit.load()
            return True
        except Exception:
            return False

    def create_reddit_instance(self):
        return asyncpraw.Reddit(
            client_id=self.praw_client_id,
            client_secret=self.praw_client_secret,
            user_agent=self.praw_user_agent
        )

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def post(self, ctx, subreddit: str):
        await self.send_random_post(ctx.channel, subreddit)
        await ctx.message.delete()

    @commands.command()
    async def delete(self, ctx):
        channel = ctx.channel
        bot_id = self.bot.user.id
        
        # Convert date to datetime at the start of the day
        today = datetime.now(pytz.timezone('Europe/Berlin')).replace(hour=0, minute=0, second=0, microsecond=0)

        deleted_count = 0
        async for message in channel.history(after=today):
            if message.author.id == bot_id and message.content.startswith("https://"):
                try:
                    await message.delete()
                    deleted_count += 1
                    await asyncio.sleep(0.5)
                except discord.errors.NotFound:
                    # Message was already deleted
                    pass
                except discord.errors.Forbidden:
                    await ctx.send("Ich habe keine Berechtigung, diese Nachricht zu löschen.")
                    return

        await ctx.send(f"Channel aufgeräumt. {deleted_count} Nachrichten gelöscht.")

    @commands.command()
    async def test(self, ctx):
        await ctx.send("test erfolgreich")


async def setup(bot):
    await bot.add_cog(Memes(bot))