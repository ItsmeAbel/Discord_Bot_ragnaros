# Client.py
#This is a client class that represents the connection to discord
import os

import discord
from discord import message
from discord import guild
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
SERVER = os.getenv('DISCORD_SERVER')

client = discord.Client()

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

    
    if(message.author.id == 203201228035981312 and message.content.startswith == 'Yo'):
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
            await message.channel.send(message.author.id)

    await client.process_commands(message)
    #await message.channel.send(message.content)

client.run(TOKEN)