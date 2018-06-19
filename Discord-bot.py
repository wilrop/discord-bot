############################################
#                                          #
#               Willem Röpke               #
#                20-06-2018                #
#                                          #
############################################


import config                   # Importing the config file
import discord                  # Importing the discord library
import asyncio                  # Importing functionality for coroutines
import random                   # For when we need random things
import os                       # For when we need things revolving around the OS
from requests import get        # Getting the quote
from json import loads          # Getting info from json file

token = config.token    # Secret token for the bot

## The discord client itself
client = discord.Client()  

# This procedure handles the hello message
def handleHello(message):
    msg = 'Hello {0.author.mention}'.format(message) # Reply with the name of the author of the message
    return msg

# This procedure handles the quote message
def handleQuote():
    response = get('http://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=en')  # Get a quote from an api
    msg = '{quoteText} - {quoteAuthor}'.format(**loads(response.text))  # Fomat the quote
    return msg

# This procedure handles the meme message
def handleMeme():
    path = config.meme_path  
    random_filename = random.choice([x for x in os.listdir(path)    # Get a random file from the directory
                                            if os.path.isfile(os.path.join(path, x))])
    return os.path.join(path, random_filename)      # Return the path, joined with the final destination

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

    # Hello command
    if message.content.startswith('!hello'):
        msg = handleHello(message)
        await client.send_message(message.channel, msg)

    # Quote command
    elif message.content.startswith('!quote'):
        msg = handleQuote()
        await client.send_message(message.channel, msg)

    # Meme command
    elif message.content.startswith('!meme'):
        fp = handleMeme()  # A file pointer is returned to the actual image
        print(fp)
        await client.send_file(message.channel, fp)

client.run(token)