import logging
from pydoc import describe

import discord
from discord.ext import commands,tasks
from enum import Enum
import datetime

class State(Enum):
    BREAK = 'Break'
    STUDY = 'Study' 
    

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
    @commands.guild_only()
    async def pomodoro_start(self, ctx: commands.Context, study_time: int, break_time: int, repetitions: int ) -> None:
        self.study_time = study_time * 60
        self.break_time = break_time * 60
        self.repetitions = repetitions
        
        self.state = State.STUDY
        
        self.countdown = self.study_time
        
        try:
            self.timer.stop()
            
            self.timer.start(ctx)
            embed=discord.Embed(title=":tomato: Pomodoro Start :tomato:", color=0xff1414)
            embed.add_field(name="Study time", value=f'{study_time} min', inline=True)
            embed.add_field(name="Break time", value=f'{break_time} min', inline=True)
            embed.add_field(name="Repetitions", value=self.repetitions, inline=True)

            await ctx.send(embed=embed)
           
        except:
            self.logger.exception('Error when pausing timer.')


    @commands.command(
        name='pomodorocurrent',
        description='Check current time on the clock',
        aliases=['pcurrent', 'pomc', 'pcurr']
    )
    @commands.guild_only()
    async def pomodoro_current(self, ctx: commands.Context) -> None:
        embed=discord.Embed(title=":tomato: Pomodoro Current :tomato:", color=0xff1414)
        embed.add_field(name=f'{self.state.value}', value=str(datetime.timedelta(seconds=self.countdown)), inline=True)
        embed.add_field(name='Repetitions left', value=self.repetitions, inline=True)

        await ctx.send(embed=embed)
 
 
    @commands.command(
        name='pomodoropause',
        description='Pause the current pomodoro timer',
        aliases=['ppause', 'pomp', 'pompause']
    )
    @commands.guild_only()
    async def pomodoro_pause(self, ctx: commands.Context) -> None:
        try:
            self.timer.pause()
            embed=discord.Embed(title=":tomato: Pomodoro timer paused :tomato:", color=0xff1414)
            await ctx.send(embed=embed)
        except:
            self.logger.exception('Error when pausing timer')


    @commands.command(
        name='pomodorostop',
        description='Stops the current pomodoro timer',
        aliases=['pstop', 'pomstop']
    )
    @commands.guild_only()
    async def pomodoro_stop(self, ctx: commands.Context) -> None:
        try:
            self.timer.stop()
            self.countdown = 0
            embed=discord.Embed(title=":tomato: Pomodoro timer stopped :tomato:", color=0xff1414)
            await ctx.send(embed=embed)
        except:
            self.logger.exception('Error when stopping timer.')


    @tasks.loop(seconds=1.0)
    async def timer(self, ctx: commands.Context):
      
        self.countdown -= 1
        if self.countdown <= 0:
            if self.state is State.STUDY: 
                self.countdown = self.break_time
                self.state = State.BREAK
                self.repetitions -= 1
                if self.repetitions <= 0: 
                    embed=discord.Embed(title=":tomato: Pomodoro session over :tomato:", color=0xff1414)
                    embed.add_field(name='Study session is over', value='Well done!', inline=True)
                    await ctx.send(embed=embed)
                    # await self.send_to_members(ctx, embed)
                    
                    self.countdown = 0
                    self.timer.stop()
                else:
                    embed=discord.Embed(title=":tomato: Pomodoro study over :tomato:", color=0xff1414)
                    embed.add_field(name='Study time is over', value='Break time!', inline=True)
                    await ctx.send(embed=embed)
                    # await self.send_to_members(ctx, embed)
                    
            else: 
                self.countdown = self.study_time
                self.state = State.STUDY
                embed=discord.Embed(title=":tomato: Pomodoro break over :tomato:", color=0xff1414)
                embed.add_field(name='Break time is over', value='Back to work!', inline=True)
                await ctx.send(embed=embed)
                # await self.send_to_members(ctx, embed)
                
    async def send_to_members(self, ctx, embed): 
        for member in ctx.guild.get_channel(689078051920674819).members:
            await member.send(embed=embed)
            
def setup(bot):
    bot.add_cog(Pomodoro(bot))
