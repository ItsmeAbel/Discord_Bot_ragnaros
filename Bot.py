# Client.py
#This is a client class that represents the connection to discord
import os

import discord
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():   #Event handler that is executed when the client has established connection to Discord
    print(f'{client.user} has connected to Discord!')

client.run(TOKEN)