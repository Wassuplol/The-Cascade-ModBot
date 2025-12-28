import discord
from discord.ext import commands
import asyncio
import time

class Moderation(commands.Cog, name="Moderation"):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='ban')
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="No reason provided"):
        """Ban a member from the server"""
        try:
            await member.ban(reason=reason)
            embed = discord.Embed(
                title="Member Banned",
                description=f"{member.mention} has been banned by {ctx.author.mention}\nReason: {reason}",
                color=0xff0000
            )
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"Failed to ban {member.mention}: {e}")
    
    @commands.command(name='unban')
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user_id: int):
        """Unban a user by ID"""
        try:
            user = await self.bot.fetch_user(user_id)
            await ctx.guild.unban(user)
            embed = discord.Embed(
                title="User Unbanned",
                description=f"{user.mention} has been unbanned by {ctx.author.mention}",
                color=0x00ff00
            )
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"Failed to unban user: {e}")
    
    @commands.command(name='kick')
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="No reason provided"):
        """Kick a member from the server"""
        try:
            await member.kick(reason=reason)
            embed = discord.Embed(
                title="Member Kicked",
                description=f"{member.mention} has been kicked by {ctx.author.mention}\nReason: {reason}",
                color=0xff0000
            )
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"Failed to kick {member.mention}: {e}")
    
    @commands.command(name='mute')
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, duration: int = 10, *, reason="No reason provided"):
        """Mute a member for a specified duration (in minutes)"""
        # Create a mute role if it doesn't exist
        mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not mute_role:
            # Create the muted role with appropriate permissions
            perms = discord.Permissions(send_messages=False, speak=False)
            mute_role = await ctx.guild.create_role(name="Muted", permissions=perms)
            
            # Apply the role to all text channels
            for channel in ctx.guild.text_channels:
                await channel.set_permissions(mute_role, send_messages=False)
        
        try:
            await member.add_roles(mute_role, reason=reason)
            embed = discord.Embed(
                title="Member Muted",
                description=f"{member.mention} has been muted by {ctx.author.mention} for {duration} minutes\nReason: {reason}",
                color=0xff0000
            )
            await ctx.send(embed=embed)
            
            # Auto-unmute after duration
            await asyncio.sleep(duration * 60)
            await member.remove_roles(mute_role)
            unmute_embed = discord.Embed(
                title="Auto Unmute",
                description=f"{member.mention} has been unmuted automatically after {duration} minutes",
                color=0x00ff00
            )
            await ctx.send(embed=unmute_embed)
        except Exception as e:
            await ctx.send(f"Failed to mute {member.mention}: {e}")
    
    @commands.command(name='unmute')
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member):
        """Unmute a member"""
        mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not mute_role:
            await ctx.send("No 'Muted' role found!")
            return
        
        try:
            await member.remove_roles(mute_role)
            embed = discord.Embed(
                title="Member Unmuted",
                description=f"{member.mention} has been unmuted by {ctx.author.mention}",
                color=0x00ff00
            )
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"Failed to unmute {member.mention}: {e}")
    
    @commands.command(name='purge', aliases=['clear'])
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int):
        """Delete a specified number of messages"""
        if amount <= 0 or amount > 100:
            await ctx.send("Please specify a number between 1 and 100")
            return
        
        deleted = await ctx.channel.purge(limit=amount + 1)  # +1 to include the command message
        response = await ctx.send(f"Deleted {len(deleted) - 1} messages!", delete_after=3)
    
    @commands.command(name='warn')
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, member: discord.Member, *, reason="No reason provided"):
        """Warn a member"""
        embed = discord.Embed(
            title="Member Warned",
            description=f"{member.mention} has been warned by {ctx.author.mention}\nReason: {reason}",
            color=0xffff00
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='warnings')
    @commands.has_permissions(manage_messages=True)
    async def warnings(self, ctx, member: discord.Member):
        """View warnings for a member (placeholder - would need a warning system)"""
        embed = discord.Embed(
            title=f"Warnings for {member.display_name}",
            description="No warnings system implemented yet (would store in database)",
            color=0xffff00
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='lock')
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx, channel: discord.TextChannel = None):
        """Lock a channel so only admins can send messages"""
        if channel is None:
            channel = ctx.channel
        
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        
        embed = discord.Embed(
            title="Channel Locked",
            description=f"{channel.mention} has been locked by {ctx.author.mention}",
            color=0xff0000
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='unlock')
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx, channel: discord.TextChannel = None):
        """Unlock a channel"""
        if channel is None:
            channel = ctx.channel
        
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = None  # Remove the overwrite
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        
        embed = discord.Embed(
            title="Channel Unlocked",
            description=f"{channel.mention} has been unlocked by {ctx.author.mention}",
            color=0x00ff00
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='slowmode')
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, seconds: int, channel: discord.TextChannel = None):
        """Set slowmode for a channel"""
        if channel is None:
            channel = ctx.channel
        
        if seconds < 0 or seconds > 21600:  # 6 hours max
            await ctx.send("Slowmode must be between 0 and 21600 seconds (6 hours)")
            return
        
        await channel.edit(slowmode_delay=seconds)
        
        if seconds == 0:
            embed = discord.Embed(
                title="Slowmode Disabled",
                description=f"Slowmode has been disabled in {channel.mention}",
                color=0x00ff00
            )
        else:
            embed = discord.Embed(
                title="Slowmode Set",
                description=f"Slowmode set to {seconds} seconds in {channel.mention}",
                color=0x00ff00
            )
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Moderation(bot))