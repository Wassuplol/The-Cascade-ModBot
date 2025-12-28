import discord
from discord.ext import commands
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot configuration
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('BOT_PREFIX', '!')

# Intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

# Initialize bot
bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f'{bot.user} has successfully connected to Discord!')
    print(f'Bot is in {len(bot.guilds)} guild(s) with {len(bot.users)} users')
    await bot.change_presence(activity=discord.Game(name=f"Prefix: {PREFIX} | {len(bot.guilds)} servers"))

@bot.command(name='help', aliases=['info'])
async def help_command(ctx, *, command_name=None):
    """Display help information for commands"""
    if command_name:
        # Show specific command help
        command = bot.get_command(command_name)
        if command:
            embed = discord.Embed(
                title=f"Command: {command.name}",
                description=command.help or "No description provided",
                color=0x00ff00
            )
            embed.add_field(name="Usage", value=f"`{PREFIX}{command.name} {command.signature}`", inline=False)
            if command.aliases:
                embed.add_field(name="Aliases", value=", ".join(command.aliases), inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"Command `{command_name}` not found!")
    else:
        # Show general help
        embed = discord.Embed(
            title="Bot Commands",
            description="Here are all available commands:",
            color=0x00ff00
        )
        
        # Group commands by category
        categories = {
            "Moderation": [],
            "Fun": [],
            "Economy": [],
            "Utility": [],
            "Utility": []
        }
        
        for command in bot.commands:
            if command.cog_name == "Moderation":
                categories["Moderation"].append(f"`{PREFIX}{command.name}` - {command.short_doc or 'No description'}")
            elif command.cog_name == "Fun":
                categories["Fun"].append(f"`{PREFIX}{command.name}` - {command.short_doc or 'No description'}")
            elif command.cog_name == "Economy":
                categories["Economy"].append(f"`{PREFIX}{command.name}` - {command.short_doc or 'No description'}")
            else:
                categories["Utility"].append(f"`{PREFIX}{command.name}` - {command.short_doc or 'No description'}")
        
        for category, cmds in categories.items():
            if cmds:
                embed.add_field(name=category, value="\n".join(cmds), inline=False)
        
        await ctx.send(embed=embed)

# Load cogs
def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                bot.load_extension(f'cogs.{filename[:-3]}')
                print(f'Loaded {filename}')
            except Exception as e:
                print(f'Failed to load {filename}: {e}')

if __name__ == "__main__":
    load_cogs()
    bot.run(TOKEN)