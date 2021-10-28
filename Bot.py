# Client.py
#This is a client class that represents the connection to discord
import os

import discord
from discord import message, guild
from discord.ext import commands
from dotenv import load_dotenv
import asyncio  #used for concurency programming. Similar to multi threading
#for music
import youtube_dl #an open-source download manager for youtube videos and audios 
#pip list to see a list of versions of installed packages
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
SERVER = os.getenv('DISCORD_SERVER')



client = discord.Client()

intents = discord.Intents().all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='Rag',intents=intents) #needed to imported commands from discord

#downloads the audio file from yt
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

#takes url as paremeter and returns the audio file name, which gets downloaded
    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename

@bot.command(name='come', help='Tells the bot to join the voice channel')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()

@bot.command(name='gtfo', help='To make the bot leave the voice channel')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

@bot.command(name='sing', help='To play song')
async def play(ctx,url):
    try :
        server = ctx.message.guild
        voice_channel = server.voice_client

        async with ctx.typing():
            filename = await YTDLSource.from_url(url, loop=bot.loop)
            voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
        await ctx.send('**As you wish** {}'.format(filename))
    except:
        await ctx.send("The bot is not connected to a voice channel.")

@bot.command(name='pause', help='This command pauses the song')
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()
    else:
        await ctx.send("The bot is not playing anything at the moment.")

@bot.command(name='resume', help='Resumes the song')
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume()
    else:
        await ctx.send("The bot was not playing anything before this. Use play_song command")

@bot.command(name='stfu', help='Stops the song')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.stop()
    else:
        await ctx.send("The bot is not playing anything at the moment.")


@client.event
async def on_ready():   #Event handler that is executed when the client has established connection to Discord
    for guild in client.guilds: #loops the through the list of servers the bot is connected to and matches it 
        if guild.name == SERVER:        #--with the one we wanted
            break
    
    members = '\n - '.join([member.name for member in guild.members])

    print(
        
        f'{client.user} is connected to the following server:\n'
        f'{guild.name} id: {guild.id}\n'

        
        )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild members: \n {members}')

with open('wordlist.txt', 'r') as f:
    global badwords # You want to be able to access this throughout the code
    words = f.read()
    badwords = words.split('\n')


@client.event
async def on_message(message):

    if(message.author == client.user):  #if message is coming from the bot itself
        return

    
    if(message.author.id == 203201228035981312 and message.content == 'Yo'):
            await message.channel.send('Hello {} My Liege. I am at your service!'.format(message.author.name))
            

    if(message.content == 'toss a coin'):
        from random import randrange
        HOT = randrange(2)
        if HOT == 0:
            await message.channel.send("Heads!")
        elif HOT == 1:
            await message.channel.send("Tails!")
        else:
            await message.channel.send("Error!")
            
    msg = message.content
    for word in badwords:
        if word in msg:
            #await message.delete()
            await message.channel.send("Language! ⍟")

    await client.process_commands(message)
    #await message.channel.send(message.content)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

@classmethod
async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename

client.run(TOKEN)