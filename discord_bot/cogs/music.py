import discord
from discord.ext import commands
import asyncio
import yt_dlp
from async_timeout import timeout
import functools

class MusicPlayer:
    def __init__(self, ctx):
        self.ctx = ctx
        self.bot = ctx.bot
        self._guild = ctx.guild
        self._channel = ctx.channel
        self.source = None
        self.next = asyncio.Event()
        self.songs = asyncio.Queue()
        self.audio_player = self.bot.loop.create_task(self.audio_player_task())
    
    def __del__(self):
        self.audio_player.cancel()
    
    async def audio_player_task(self):
        while True:
            self.next.clear()
            self.source = await self.songs.get()
            if not self.source:
                return
            self._guild.voice_client.play(self.source, after=self.toggle_next)
            await self.next.wait()
    
    def toggle_next(self, error=None):
        if error:
            print(f"Player error: {error}")
        self.next.set()
    
    def destroy(self, guild):
        return self.bot.loop.create_task(self._destroy(guild))
    
    async def _destroy(self, guild):
        await self.songs.put(None)
        await guild.voice_client.disconnect()

class Music(commands.Cog, name="Music"):
    def __init__(self, bot):
        self.bot = bot
        self.players = {}
    
    def get_player(self, ctx):
        if ctx.guild.id not in self.players:
            self.players[ctx.guild.id] = MusicPlayer(ctx)
        return self.players[ctx.guild.id]
    
    @staticmethod
    def parse_duration(duration: int):
        minutes, seconds = divmod(duration, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        
        duration = []
        if days > 0:
            duration.append(f'{days}d')
        if hours > 0:
            duration.append(f'{hours}h')
        if minutes > 0:
            duration.append(f'{minutes}m')
        if seconds > 0:
            duration.append(f'{seconds}s')
        
        return ' '.join(duration)
    
    @staticmethod
    def get_embed(source):
        embed = discord.Embed(
            title=source.title,
            description=f"Duration: {Music.parse_duration(source.duration)}",
            url=source.url,
            color=0x00ff00
        )
        return embed
    
    @commands.command(name='join', aliases=['connect'])
    async def join_(self, ctx):
        """Joins your voice channel"""
        destination = ctx.author.voice.channel if ctx.author.voice else None
        if destination is None:
            await ctx.send("You need to be in a voice channel first!")
            return
        
        if ctx.voice_client is None:
            await destination.connect()
            await ctx.send(f"Joined {destination.name}!")
        else:
            await ctx.voice_client.move_to(destination)
            await ctx.send(f"Moved to {destination.name}!")
    
    @commands.command(name='leave', aliases=['disconnect'])
    async def leave_(self, ctx):
        """Leaves the voice channel"""
        if ctx.voice_client is None:
            await ctx.send("I'm not in a voice channel!")
            return
        
        player = self.get_player(ctx)
        await player.destroy(ctx.guild)
        del self.players[ctx.guild.id]
        await ctx.send("Disconnected!")
    
    @commands.command(name='play', aliases=['p'])
    async def play_(self, ctx, *, query: str):
        """Plays a song from YouTube"""
        if ctx.voice_client is None:
            await ctx.invoke(self.join_)
        
        async with ctx.typing():
            player = self.get_player(ctx)
            
            # Search for the song
            ydl_opts = {
                'format': 'bestaudio/best',
                'default_search': 'auto',
                'noplaylist': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(f"ytsearch:{query}", download=False)
                if 'entries' in info:
                    info = info['entries'][0]
                
                source = {
                    'webpage_url': info['webpage_url'],
                    'title': info['title'],
                    'duration': info.get('duration', 0),
                    'uploader': info.get('uploader', 'Unknown'),
                    'thumbnail': info.get('thumbnail', '')
                }
                
                # Create audio source
                source = discord.PCMVolumeTransformer(
                    discord.FFmpegPCMAudio(source['webpage_url'])
                )
                
                await player.songs.put(source)
                await ctx.send(embed=self.get_embed(source))
    
    @commands.command(name='pause')
    async def pause_(self, ctx):
        """Pauses the current song"""
        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("Paused ⏸️")
        else:
            await ctx.send("Nothing is playing!")
    
    @commands.command(name='resume')
    async def resume_(self, ctx):
        """Resumes the current song"""
        if ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send("Resumed ▶️")
        else:
            await ctx.send("The player is not paused!")
    
    @commands.command(name='stop')
    async def stop_(self, ctx):
        """Stops the current song and clears the queue"""
        if ctx.voice_client.is_playing() or ctx.voice_client.is_paused():
            ctx.voice_client.stop()
            await ctx.send("Stopped ⏹️")
        else:
            await ctx.send("Nothing is playing!")
    
    @commands.command(name='skip', aliases=['next'])
    async def skip_(self, ctx):
        """Skips the current song"""
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send("Skipped ⏭️")
        else:
            await ctx.send("Nothing is playing!")
    
    @commands.command(name='queue', aliases=['q'])
    async def queue_(self, ctx):
        """Shows the current queue"""
        player = self.get_player(ctx)
        if player.songs.empty():
            await ctx.send("The queue is empty!")
            return
        
        upcoming = []
        for i, song in enumerate(player.songs._queue, start=1):
            if i > 10:  # Only show first 10 songs
                break
            upcoming.append(f"{i}. {song.title}")
        
        if upcoming:
            embed = discord.Embed(
                title="Queue",
                description="\n".join(upcoming),
                color=0x00ff00
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("The queue is empty!")

async def setup(bot):
    await bot.add_cog(Music(bot))