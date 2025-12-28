import discord
from discord.ext import commands
import random
import asyncio
import aiohttp
import json

class Fun(commands.Cog, name="Fun"):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='ping')
    async def ping(self, ctx):
        """Check the bot's latency"""
        await ctx.send(f'Pong! {round(self.bot.latency * 1000)}ms')
    
    @commands.command(name='roll', aliases=['dice'])
    async def roll(self, ctx, dice: str = "1d6"):
        """Roll a dice in NdN format"""
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await ctx.send('Format has to be in NdN!')
            return
        
        if rolls > 100:
            await ctx.send('You can\'t roll more than 100 dice at once!')
            return
        
        if limit > 1000:
            await ctx.send('Dice can\'t have more than 1000 sides!')
            return
        
        results = [random.randint(1, limit) for r in range(rolls)]
        embed = discord.Embed(
            title="Dice Roll",
            description=f"You rolled: {' + '.join(map(str, results))} = {sum(results)}",
            color=0x00ff00
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='flip', aliases=['coin'])
    async def flip(self, ctx):
        """Flip a coin"""
        outcome = random.choice(['Heads', 'Tails'])
        embed = discord.Embed(
            title="Coin Flip",
            description=f"It's {outcome}!",
            color=0x00ff00
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='rps')
    async def rps(self, ctx, choice: str):
        """Play Rock Paper Scissors"""
        choices = ['rock', 'paper', 'scissors']
        user_choice = choice.lower()
        
        if user_choice not in choices:
            await ctx.send("Please choose rock, paper, or scissors!")
            return
        
        bot_choice = random.choice(choices)
        
        # Determine winner
        if user_choice == bot_choice:
            result = "It's a tie!"
            color = 0xffff00
        elif (user_choice == "rock" and bot_choice == "scissors") or \
             (user_choice == "paper" and bot_choice == "rock") or \
             (user_choice == "scissors" and bot_choice == "paper"):
            result = "You win!"
            color = 0x00ff00
        else:
            result = "Bot wins!"
            color = 0xff0000
        
        embed = discord.Embed(
            title="Rock Paper Scissors",
            description=f"You chose {user_choice}\nBot chose {bot_choice}\n\n{result}",
            color=color
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='meme')
    async def meme(self, ctx):
        """Get a random meme"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://meme-api.com/gimme') as response:
                    data = await response.json()
                    embed = discord.Embed(
                        title=data['title'],
                        url=data['postLink'],
                        color=0x00ff00
                    )
                    embed.set_image(url=data['url'])
                    embed.set_footer(text=f"From r/{data['subreddit']}")
                    await ctx.send(embed=embed)
        except Exception:
            await ctx.send("Failed to fetch a meme. Try again later!")
    
    @commands.command(name='joke')
    async def joke(self, ctx):
        """Get a random joke"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://official-joke-api.appspot.com/random_joke') as response:
                    data = await response.json()
                    embed = discord.Embed(
                        title=data['setup'],
                        description=data['punchline'],
                        color=0x00ff00
                    )
                    await ctx.send(embed=embed)
        except Exception:
            await ctx.send("Failed to fetch a joke. Try again later!")
    
    @commands.command(name='cat')
    async def cat(self, ctx):
        """Get a random cat image"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://api.thecatapi.com/v1/images/search') as response:
                    data = await response.json()
                    if data:
                        embed = discord.Embed(
                            title="Here's a cat for you!",
                            color=0x00ff00
                        )
                        embed.set_image(url=data[0]['url'])
                        await ctx.send(embed=embed)
                    else:
                        await ctx.send("No cats available right now!")
        except Exception:
            await ctx.send("Failed to fetch a cat. Try again later!")
    
    @commands.command(name='dog')
    async def dog(self, ctx):
        """Get a random dog image"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://dog.ceo/api/breeds/image/random') as response:
                    data = await response.json()
                    embed = discord.Embed(
                        title="Here's a dog for you!",
                        color=0x00ff00
                    )
                    embed.set_image(url=data['message'])
                    await ctx.send(embed=embed)
        except Exception:
            await ctx.send("Failed to fetch a dog. Try again later!")
    
    @commands.command(name='8ball', aliases=['eightball'])
    async def eightball(self, ctx, *, question):
        """Ask the magic 8-ball a question"""
        responses = [
            "It is certain.",
            "It is decidedly so.",
            "Without a doubt.",
            "Yes - definitely.",
            "You may rely on it.",
            "As I see it, yes.",
            "Most likely.",
            "Outlook good.",
            "Yes.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful."
        ]
        
        embed = discord.Embed(
            title="🎱 Magic 8-Ball",
            description=f"Question: {question}\nAnswer: {random.choice(responses)}",
            color=0x00ff00
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='riddle')
    async def riddle(self, ctx):
        """Get a random riddle"""
        riddles = [
            {
                "question": "I speak without a mouth and hear without ears. I have no body, but I come alive with the wind. What am I?",
                "answer": "An echo"
            },
            {
                "question": "I'm tall when I'm young and short when I'm old. What am I?",
                "answer": "A candle"
            },
            {
                "question": "What has hands but cannot clap?",
                "answer": "A clock"
            },
            {
                "question": "What gets wetter the more it dries?",
                "answer": "A towel"
            },
            {
                "question": "What has a face and two hands but no arms or legs?",
                "answer": "A clock"
            },
            {
                "question": "What can travel around the world while staying in a corner?",
                "answer": "A stamp"
            },
            {
                "question": "What has many keys but can't open any doors?",
                "answer": "A piano"
            },
            {
                "question": "What comes once in a minute, twice in a moment, but never in a thousand years?",
                "answer": "The letter 'M'"
            }
        ]
        
        riddle = random.choice(riddles)
        embed = discord.Embed(
            title="Riddle",
            description=riddle["question"],
            color=0x00ff00
        )
        await ctx.send(embed=embed)
        
        # Wait for answer (simplified - doesn't validate answers)
        await ctx.send(f"*Answer: {riddle['answer']}*")
    
    @commands.command(name='trivia')
    async def trivia(self, ctx):
        """Get a random trivia question"""
        questions = [
            {"question": "What is the capital of France?", "answer": "Paris"},
            {"question": "What is the largest planet in our solar system?", "answer": "Jupiter"},
            {"question": "How many bones are in the human body?", "answer": "206"},
            {"question": "What is the chemical symbol for gold?", "answer": "Au"},
            {"question": "Who painted the Mona Lisa?", "answer": "Leonardo da Vinci"},
            {"question": "What is the largest ocean on Earth?", "answer": "Pacific Ocean"},
            {"question": "What is the hardest natural substance on Earth?", "answer": "Diamond"},
            {"question": "How many elements are in the periodic table?", "answer": "118"}
        ]
        
        trivia = random.choice(questions)
        embed = discord.Embed(
            title="Trivia Question",
            description=trivia["question"],
            color=0x00ff00
        )
        await ctx.send(embed=embed)
        
        # Wait for answer (simplified - doesn't validate answers)
        await ctx.send(f"*Answer: {trivia['answer']}*")
    
    @commands.command(name='ascii')
    async def ascii(self, ctx, *, text):
        """Convert text to ASCII art"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f'http://artii.herokuapp.com/make?text={text}') as response:
                    ascii_text = await response.text()
                    if len(ascii_text) > 2000:
                        await ctx.send("Text is too long for ASCII art!")
                        return
                    await ctx.send(f"```\n{ascii_text}\n```")
        except Exception:
            await ctx.send("Failed to create ASCII art. Try again later!")
    
    @commands.command(name='fact')
    async def fact(self, ctx):
        """Get a random fact"""
        facts = [
            "Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly edible.",
            "Octopuses have three hearts and blue blood.",
            "A group of flamingos is called a 'flamboyance'.",
            "The shortest war in history was between Britain and Zanzibar on August 27, 1896. Zanzibar surrendered after 38 minutes.",
            "Bananas are berries, but strawberries aren't.",
            "A day on Venus is longer than a year on Venus.",
            "The Eiffel Tower can be 15 cm taller during the summer due to thermal expansion.",
            "The inventor of the frisbee was turned into a frisbee after he died.",
            "The dot over the letter 'i' is called a tittle.",
            "The total weight of all ants on Earth is about the same as the total weight of all humans."
        ]
        
        embed = discord.Embed(
            title="Random Fact",
            description=random.choice(facts),
            color=0x00ff00
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='insult')
    async def insult(self, ctx, member: discord.Member = None):
        """Generate a random insult"""
        if member is None:
            member = ctx.author
        
        insults = [
            "I'd agree with you but then we'd both be wrong.",
            "You're not stupid; you just have bad luck when thinking.",
            "I'm not saying I hate you, but I would unplug your life support to charge my phone.",
            "You bring everyone so much joy... when you leave the room.",
            "I'm not a proctologist, but I know an asshole when I see one.",
            "You have an entire life to be an idiot. Why not take today off?",
            "Two wrongs don't make a right, take your parents as an example.",
            "You're the reason the gene pool needs a lifeguard.",
            "If laughter is the best medicine, your face must be curing the world.",
            "You look like a before picture."
        ]
        
        embed = discord.Embed(
            title="Insult",
            description=f"{member.mention}, {random.choice(insults)}",
            color=0xff0000
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='compliment')
    async def compliment(self, ctx, member: discord.Member = None):
        """Generate a random compliment"""
        if member is None:
            member = ctx.author
        
        compliments = [
            "You're a smart cookie!",
            "Your smile is contagious.",
            "You're a ray of sunshine on a cloudy day.",
            "You're an awesome friend.",
            "You're a gift to those around you.",
            "You're a smart, funny, and a really nice person.",
            "Being around you makes everything better!",
            "You have the best laugh.",
            "You light up the room.",
            "You deserve a hug right now."
        ]
        
        embed = discord.Embed(
            title="Compliment",
            description=f"{member.mention}, {random.choice(compliments)}",
            color=0x00ff00
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Fun(bot))