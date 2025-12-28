import discord
from discord.ext import commands
import json
import os
import random
from datetime import datetime, timedelta
import asyncio

class Economy(commands.Cog, name="Economy"):
    def __init__(self, bot):
        self.bot = bot
        self.data_file = "data/economy.json"
        self.load_data()
    
    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                self.economy_data = json.load(f)
        else:
            self.economy_data = {}
    
    def save_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.economy_data, f, indent=4)
    
    def get_user_data(self, user_id):
        user_id = str(user_id)
        if user_id not in self.economy_data:
            self.economy_data[user_id] = {
                "balance": 100,
                "bank": 0,
                "last_daily": None,
                "last_work": None,
                "inventory": {},
                "reputation": 0
            }
        return self.economy_data[user_id]
    
    @commands.command(name='balance', aliases=['bal', 'money', 'wallet'])
    async def balance(self, ctx, member: discord.Member = None):
        """Check your or another user's balance"""
        if member is None:
            member = ctx.author
        
        user_data = self.get_user_data(member.id)
        embed = discord.Embed(
            title=f"{member.display_name}'s Balance",
            color=0x00ff00
        )
        embed.add_field(name="Wallet", value=f"🪙 {user_data['balance']}", inline=False)
        embed.add_field(name="Bank", value=f"🏦 {user_data['bank']}", inline=False)
        embed.add_field(name="Total", value=f"💰 {user_data['balance'] + user_data['bank']}", inline=False)
        await ctx.send(embed=embed)
    
    @commands.command(name='daily')
    async def daily(self, ctx):
        """Claim your daily coins"""
        user_data = self.get_user_data(ctx.author.id)
        now = datetime.now()
        
        if user_data['last_daily']:
            last_daily = datetime.fromisoformat(user_data['last_daily'])
            if now - last_daily < timedelta(days=1):
                time_left = timedelta(days=1) - (now - last_daily)
                hours, remainder = divmod(time_left.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                await ctx.send(f"You've already claimed your daily reward! Try again in {hours}h {minutes}m {seconds}s")
                return
        
        amount = random.randint(50, 200)
        user_data['balance'] += amount
        user_data['last_daily'] = now.isoformat()
        self.save_data()
        
        embed = discord.Embed(
            title="Daily Reward!",
            description=f"You received 🪙 {amount} coins!",
            color=0x00ff00
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='work')
    async def work(self, ctx):
        """Work to earn coins"""
        user_data = self.get_user_data(ctx.author.id)
        now = datetime.now()
        
        if user_data['last_work']:
            last_work = datetime.fromisoformat(user_data['last_work'])
            if now - last_work < timedelta(hours=1):
                time_left = timedelta(hours=1) - (now - last_work)
                minutes, seconds = divmod(time_left.seconds, 60)
                await ctx.send(f"You need to wait {minutes}m {seconds}s before working again!")
                return
        
        jobs = [
            ("Programmer", "coded a Discord bot"),
            ("Chef", "cooked a delicious meal"),
            ("Teacher", "taught a class"),
            ("Artist", "painted a masterpiece"),
            ("Gardener", "tended to plants"),
            ("Writer", "wrote a novel"),
            ("Mechanic", "fixed a car"),
            ("Doctor", "helped patients"),
            ("Engineer", "built a bridge"),
            ("Scientist", "made a discovery")
        ]
        
        job = random.choice(jobs)
        amount = random.randint(100, 300)
        user_data['balance'] += amount
        user_data['last_work'] = now.isoformat()
        self.save_data()
        
        embed = discord.Embed(
            title=f"Work Completed!",
            description=f"You worked as a {job[0]} and {job[1]}, earning 🪙 {amount} coins!",
            color=0x00ff00
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='deposit', aliases=['dep'])
    async def deposit(self, ctx, amount: int):
        """Deposit coins to your bank"""
        user_data = self.get_user_data(ctx.author.id)
        
        if amount <= 0:
            await ctx.send("Amount must be positive!")
            return
        
        if user_data['balance'] < amount:
            await ctx.send("You don't have enough coins in your wallet!")
            return
        
        user_data['balance'] -= amount
        user_data['bank'] += amount
        self.save_data()
        
        await ctx.send(f"Deposited 🪙 {amount} to your bank! New balance: 🪙 {user_data['balance']} | Bank: 🏦 {user_data['bank']}")
    
    @commands.command(name='withdraw', aliases=['with'])
    async def withdraw(self, ctx, amount: int):
        """Withdraw coins from your bank"""
        user_data = self.get_user_data(ctx.author.id)
        
        if amount <= 0:
            await ctx.send("Amount must be positive!")
            return
        
        if user_data['bank'] < amount:
            await ctx.send("You don't have enough coins in your bank!")
            return
        
        user_data['bank'] -= amount
        user_data['balance'] += amount
        self.save_data()
        
        await ctx.send(f"Withdrew 🪙 {amount} from your bank! New balance: 🪙 {user_data['balance']} | Bank: 🏦 {user_data['bank']}")
    
    @commands.command(name='transfer', aliases=['send', 'pay'])
    async def transfer(self, ctx, member: discord.Member, amount: int):
        """Transfer coins to another user"""
        if member.id == ctx.author.id:
            await ctx.send("You can't transfer to yourself!")
            return
        
        sender_data = self.get_user_data(ctx.author.id)
        receiver_data = self.get_user_data(member.id)
        
        if amount <= 0:
            await ctx.send("Amount must be positive!")
            return
        
        if sender_data['balance'] < amount:
            await ctx.send("You don't have enough coins to transfer!")
            return
        
        sender_data['balance'] -= amount
        receiver_data['balance'] += amount
        self.save_data()
        
        embed = discord.Embed(
            title="Transfer Successful!",
            description=f"You sent 🪙 {amount} to {member.display_name}",
            color=0x00ff00
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='leaderboard', aliases=['lb', 'top'])
    async def leaderboard(self, ctx):
        """Show the richest users"""
        sorted_users = sorted(self.economy_data.items(), key=lambda x: x[1]['balance'] + x[1]['bank'], reverse=True)
        
        if not sorted_users:
            await ctx.send("No one has any coins yet!")
            return
        
        embed = discord.Embed(
            title=" wealthiest Users",
            color=0x00ff00
        )
        
        for i, (user_id, data) in enumerate(sorted_users[:10]):
            user = self.bot.get_user(int(user_id))
            if user:
                embed.add_field(
                    name=f"#{i+1} {user.display_name}",
                    value=f"💰 {data['balance'] + data['bank']}",
                    inline=False
                )
        
        await ctx.send(embed=embed)
    
    @commands.command(name='rob')
    async def rob(self, ctx, member: discord.Member):
        """Try to rob another user"""
        if member.id == ctx.author.id:
            await ctx.send("You can't rob yourself!")
            return
        
        sender_data = self.get_user_data(ctx.author.id)
        target_data = self.get_user_data(member.id)
        
        if target_data['balance'] < 50:
            await ctx.send(f"{member.display_name} doesn't have enough coins to rob!")
            return
        
        if random.random() < 0.7:  # 70% chance of failure
            fine = random.randint(10, 50)
            if sender_data['balance'] < fine:
                fine = sender_data['balance']
            sender_data['balance'] -= fine
            self.save_data()
            
            embed = discord.Embed(
                title="Robbery Failed!",
                description=f"You were caught! You paid a fine of 🪙 {fine}",
                color=0xff0000
            )
            await ctx.send(embed=embed)
        else:
            stolen = random.randint(20, int(target_data['balance'] * 0.3))
            sender_data['balance'] += stolen
            target_data['balance'] -= stolen
            self.save_data()
            
            embed = discord.Embed(
                title="Robbery Successful!",
                description=f"You stole 🪙 {stolen} from {member.display_name}!",
                color=0x00ff00
            )
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Economy(bot))