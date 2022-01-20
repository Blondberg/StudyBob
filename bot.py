import logging
import os
import platform
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Setup logging
logger = logging.getLogger('studybob')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='studybob.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s :: %(levelname)-7s :: %(message)s'))
logger.addHandler(handler)


# Load environment variables
load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
BOT_PREFIX = os.getenv('BOT_PREFIX')

bot = commands.Bot(command_prefix=BOT_PREFIX)

INITIAL_EXTENSIONS = {
    'cogs.ping'
}

@bot.event
async def on_ready() -> None:
    """Code that is executed when bot is ready
    """
    print(f'Logged in as: {bot.user.name}')
    print(f'Python version: {platform.python_version()}')
    print(f'System OS: {platform.system()} {platform.release()}')

    logger.info('Bot is ready!')

    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Game(f'nothing')
    )


@bot.event
async def on_command(ctx: commands.Context) -> None:
    """Executed before every commands

    Args:
        ctx (commands.Context): Context of the command
    """
    logger.debug('Command invoked -  \'%s\' in guild %s (ID: %i) by %s (ID: %i)',
                 ctx.command, ctx.guild.name, ctx.guild.id, ctx.author, ctx.author.id)


@bot.event
async def on_command_error(ctx: commands.Context, error: Exception) -> None:
    """Handles errors for wrongly used commands

    Args:
        ctx (commands.Context): Context of the command
        error (Exception): thrown exception
    """
    logger.error('An error occured when using command %s - %s', ctx.command, error)


# Load in all extensions
for extension in INITIAL_EXTENSIONS:
    try:
        bot.load_extension(extension)
        logger.debug('Loaded extension - %s', extension)
    except Exception as e:
        logger.error('Failed to load extension %s. %s', extension, e)


# Run the bot
bot.run(DISCORD_TOKEN, reconnect=True)