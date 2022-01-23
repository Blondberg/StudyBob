import logging
from pydoc import describe

import discord
from discord.ext import commands,tasks


class Pomodoro(commands.Cog, name='pomodoro'):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()

        self.bot = bot
        self.logger = logging.getLogger('studybob')


        self.study_time = 0
        self.break_time = 0

        self.repetitions = 0

        self.countdown = 0


    @commands.command(
        name='pomodorostart',
        description='Start a pomodoro session',
        aliases=['pomstart', 'poms', 'pstart']
    )
    async def pomodoro_start(self, ctx: commands.Context, study_time: int, break_time: int, repetitions: int ) -> None:
        self.study_time = study_time
        self.break_time = break_time
        self.repetitions = repetitions
        
        try:
            self.timer.start(ctx)
            await ctx.send('Timer started')
        except:
            self.logger.exception('Error when pausing timer.')


    @commands.command(
        name='pomodorocurrent',
        description='Check current time on the clock',
        aliases=['pcurrent', 'pomc', 'pcurr']
    )
    async def pomodoro_current(self, ctx: commands.Context) -> None:
        await ctx.send(str(self.countdown))


    @commands.command(
        name='pomodoropause',
        description='Pause the current pomodoro timer',
        aliases=['ppause', 'pomp', 'pompause']
    )
    async def pomodoro_pause(self, ctx: commands.Context) -> None:
        try:
            self.timer.pause()
            await ctx.send('Timer paused!')
        except:
            self.logger.exception('Error when pausing timer')


    @commands.command(
        name='pomodorostop',
        description='Stops the current pomodoro timer',
        aliases=['pstop', 'pomstop']
    )
    async def pomodoro_stop(self, ctx: commands.Context) -> None:
        try:
            self.timer.stop()
            self.countdown = 0
            await ctx.send('Timer stopped!')
        except:
            self.logger.exception('Error when stopping timer.')


    @tasks.loop(seconds=1.0)
    async def timer(self, ctx: commands.Context):
        self.countdown -= 1
        if self.countdown <= 0:
            self.timer.stop()
            await ctx.send('Time stopped')


def setup(bot):
    bot.add_cog(Pomodoro(bot))
