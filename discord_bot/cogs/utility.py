import discord
from discord.ext import commands
import datetime
import time
import asyncio
import psutil
import platform

class Utility(commands.Cog, name="Utility"):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='serverinfo', aliases=['guildinfo'])
    async def serverinfo(self, ctx):
        """Get information about the server"""
        guild = ctx.guild
        embed = discord.Embed(
            title=f"Server Info - {guild.name}",
            color=0x00ff00,
            timestamp=guild.created_at
        )
        embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
        embed.add_field(name="Name", value=guild.name, inline=True)
        embed.add_field(name="ID", value=guild.id, inline=True)
        embed.add_field(name="Owner", value=guild.owner.mention, inline=True)
        embed.add_field(name="Members", value=guild.member_count, inline=True)
        embed.add_field(name="Roles", value=len(guild.roles), inline=True)
        embed.add_field(name="Channels", value=len(guild.channels), inline=True)
        embed.add_field(name="Boosts", value=guild.premium_subscription_count, inline=True)
        embed.add_field(name="Region", value=guild.preferred_locale, inline=True)
        embed.add_field(name="Created", value=guild.created_at.strftime("%B %d, %Y"), inline=False)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='userinfo', aliases=['whois'])
    async def userinfo(self, ctx, member: discord.Member = None):
        """Get information about a user"""
        if member is None:
            member = ctx.author
        
        embed = discord.Embed(
            title=f"User Info - {member.display_name}",
            color=0x00ff00,
            timestamp=member.joined_at
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.add_field(name="Display Name", value=member.display_name, inline=True)
        embed.add_field(name="Username", value=member.name, inline=True)
        embed.add_field(name="Discriminator", value=f"#{member.discriminator}", inline=True)
        embed.add_field(name="ID", value=member.id, inline=True)
        embed.add_field(name="Status", value=str(member.status).title(), inline=True)
        embed.add_field(name="Joined Server", value=member.joined_at.strftime("%B %d, %Y"), inline=True)
        embed.add_field(name="Account Created", value=member.created_at.strftime("%B %d, %Y"), inline=True)
        
        # Show roles
        roles = [role.mention for role in member.roles if role.name != "@everyone"]
        if roles:
            roles_str = " ".join(roles[-5:])  # Show up to 5 most important roles
            embed.add_field(name="Roles", value=roles_str, inline=False)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='avatar', aliases=['pfp'])
    async def avatar(self, ctx, member: discord.Member = None):
        """Get a user's avatar"""
        if member is None:
            member = ctx.author
        
        embed = discord.Embed(
            title=f"{member.display_name}'s Avatar",
            color=0x00ff00
        )
        embed.set_image(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.set_footer(text=f"Requested by {ctx.author.display_name}")
        await ctx.send(embed=embed)
    
    @commands.command(name='botinfo')
    async def botinfo(self, ctx):
        """Get information about the bot"""
        embed = discord.Embed(
            title=f"Bot Information - {self.bot.user.name}",
            color=0x00ff00
        )
        embed.set_thumbnail(url=self.bot.user.avatar.url if self.bot.user.avatar else self.bot.user.default_avatar.url)
        embed.add_field(name="Name", value=self.bot.user.name, inline=True)
        embed.add_field(name="ID", value=self.bot.user.id, inline=True)
        embed.add_field(name="Discriminator", value=f"#{self.bot.user.discriminator}", inline=True)
        embed.add_field(name="Created", value=self.bot.user.created_at.strftime("%B %d, %Y"), inline=True)
        embed.add_field(name="Servers", value=len(self.bot.guilds), inline=True)
        embed.add_field(name="Users", value=len(self.bot.users), inline=True)
        embed.add_field(name="Commands", value=len(self.bot.commands), inline=True)
        embed.add_field(name="Uptime", value=str(datetime.datetime.now() - self.bot.uptime), inline=False)
        
        # System info
        process = psutil.Process()
        memory_usage = process.memory_info().rss / 1024 / 1024  # MB
        cpu_percent = process.cpu_percent()
        
        embed.add_field(name="Memory Usage", value=f"{memory_usage:.2f} MB", inline=True)
        embed.add_field(name="CPU Usage", value=f"{cpu_percent}%", inline=True)
        embed.add_field(name="Python Version", value=platform.python_version(), inline=True)
        embed.add_field(name="Discord.py Version", value=discord.__version__, inline=True)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='invite')
    async def invite(self, ctx):
        """Get an invite link for the bot"""
        permissions = discord.Permissions(administrator=True)
        invite_url = discord.utils.oauth_url(
            self.bot.user.id,
            permissions=permissions,
            scopes=("bot", "applications.commands")
        )
        
        embed = discord.Embed(
            title="Invite Bot",
            description=f"[Click here to invite the bot to your server]({invite_url})",
            color=0x00ff00
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='uptime')
    async def uptime(self, ctx):
        """Get the bot's uptime"""
        uptime = datetime.datetime.now() - self.bot.uptime
        hours, remainder = divmod(int(uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        
        embed = discord.Embed(
            title="Uptime",
            description=f"{days}d {hours}h {minutes}m {seconds}s",
            color=0x00ff00
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='stats')
    async def stats(self, ctx):
        """Get bot statistics"""
        guild_count = len(self.bot.guilds)
        user_count = len(self.bot.users)
        command_count = len(self.bot.commands)
        
        # Count messages processed
        # (This would require tracking in a real implementation)
        
        embed = discord.Embed(
            title="Bot Statistics",
            color=0x00ff00
        )
        embed.add_field(name="Servers", value=guild_count, inline=True)
        embed.add_field(name="Users", value=user_count, inline=True)
        embed.add_field(name="Commands", value=command_count, inline=True)
        embed.add_field(name="Latency", value=f"{round(self.bot.latency * 1000)}ms", inline=True)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='suggest')
    async def suggest(self, ctx, *, suggestion):
        """Make a suggestion for the bot"""
        embed = discord.Embed(
            title="Suggestion Received",
            description=f"Thank you for your suggestion, {ctx.author.mention}!\n\n**Suggestion:** {suggestion}",
            color=0x00ff00
        )
        # In a real implementation, this would send to a specific channel
        await ctx.send(embed=embed)
    
    @commands.command(name='vote')
    async def vote(self, ctx, *, options_str):
        """Create a simple vote with multiple options"""
        options = [opt.strip() for opt in options_str.split(',')]
        
        if len(options) < 2:
            await ctx.send("Please provide at least 2 options separated by commas.")
            return
        
        if len(options) > 10:
            await ctx.send("You can't have more than 10 options.")
            return
        
        embed = discord.Embed(
            title="📊 Vote",
            description="React to vote!",
            color=0x00ff00
        )
        
        for i, option in enumerate(options):
            embed.add_field(name=f"Option {i+1}", value=option, inline=False)
        
        message = await ctx.send(embed=embed)
        
        # Add reactions for voting
        reactions = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
        for i in range(len(options)):
            await message.add_reaction(reactions[i])
    
    @commands.command(name='poll')
    async def poll(self, ctx, *, question):
        """Create a yes/no poll"""
        embed = discord.Embed(
            title="📊 Poll",
            description=question,
            color=0x00ff00
        )
        embed.set_footer(text=f"Poll by {ctx.author.display_name}")
        
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
        await message.add_reaction('👎')
    
    @commands.command(name='remind', aliases=['timer'])
    async def remind(self, ctx, time_str: str, *, reminder: str):
        """Set a reminder"""
        # Parse time (simple implementation - hours, minutes, seconds)
        try:
            if time_str.endswith('s'):
                seconds = int(time_str[:-1])
            elif time_str.endswith('m'):
                seconds = int(time_str[:-1]) * 60
            elif time_str.endswith('h'):
                seconds = int(time_str[:-1]) * 3600
            else:
                seconds = int(time_str)  # Assume seconds if no suffix
                
            if seconds <= 0 or seconds > 86400:  # Max 24 hours
                await ctx.send("Please specify a time between 1 second and 24 hours.")
                return
                
            embed = discord.Embed(
                title="⏰ Reminder Set",
                description=f"I'll remind you about '{reminder}' in {time_str}",
                color=0x00ff00
            )
            await ctx.send(embed=embed)
            
            await ctx.send(f"Waiting for {time_str}...")
            await asyncio.sleep(seconds)
            
            embed = discord.Embed(
                title="⏰ Reminder",
                description=f"{ctx.author.mention}, you asked to be reminded about: {reminder}",
                color=0x00ff00
            )
            await ctx.send(embed=embed)
            
        except ValueError:
            await ctx.send("Please specify a valid time format (e.g., 5m, 1h, 30s)")

async def setup(bot):
    bot.uptime = datetime.datetime.now()
    await bot.add_cog(Utility(bot))