# Client.py
#This is a client class that represents the connection to discord
import os

import discord
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
    
    

    print(
        
        f'{client.user} is connected to the following server:\n'
        f'{guild.name} id: {guild.id}\n'
        
        )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild members: \n {members}')


client.run(TOKEN)