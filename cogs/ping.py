import logging

import discord
from discord.ext import commands


class Ping(commands.Cog, name="ping"):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
        self.bot = bot

        self.logger = logging.getLogger('studybob')


    @commands.command(
        name='ping',
        description='Ping the bot to see if it\'s alive'
    )
    @commands.guild_only()
    async def ping(self, ctx: commands.Context) -> None:
        await ctx.send(f'Pong! {ctx.author.mention}')


def setup(bot):
    bot.add_cog(Ping(bot))