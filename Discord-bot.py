"""
Discord bot by Willem Röpke

"""

import discord                  # Importing the discord library
import asyncio                  # I need coroutines
import random                   # For when we need random things
import os                       # For when we need things revolving around the OS.
from requests import get        # Getting the quote
from json import loads          # Getting info from json file

token = 'NDU3MjkxODkxMjQ4MjAxNzM4.DgXC7g.iXM4gMDPGujH8eppMAkxLvVOSZE'    # Secret token for the bot

## The discord client itself
client = discord.Client()  


def handleHello(message):
    msg = 'Hello {0.author.mention}'.format(message)
    return msg

def handleQuote():
    response = get('http://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=en')
    msg = '{quoteText} - {quoteAuthor}'.format(**loads(response.text))
    return msg

def handleMeme():
    path = r'D:\Documenten\Programmeren\Discord bot\Memes'
    random_filename = random.choice([x for x in os.listdir(path)
                                            if os.path.isfile(os.path.join(path, x))])
    return os.path.join(path, random_filename)

# On startup, print this info
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

# If we see a message (a command)
@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = handleHello(message)
        await client.send_message(message.channel, msg)

    elif message.content.startswith('!quote'):
        msg = handleQuote()
        await client.send_message(message.channel, msg)

    elif message.content.startswith('!meme'):
        fp = handleMeme()
        print(fp)
        await client.send_file(message.channel, fp)

client.run(token)