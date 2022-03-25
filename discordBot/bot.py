import discord
from discord.ext import commands
from random import randint

client = commands.Bot(command_prefix = '.')

# connection establish
@client.event
async def on_ready():
    print('{0.user} is ready'.format(client))
    games = ['nothing', 'nothing', 'Lost Ark', 'Final Fantasy XIV', 'Counter-Strike: Global Offensive', 'Valorant', 'League of Legends']
    number = randint(0, 6)
    await client.change_presence(activity=discord.Game(games[number]))

# reading messages
@client.event
async def on_message(message):
    # prevents self looping
    if message.author == client.user:
        return
    
    # test
    if 'hello' in message.content.lower():
        await message.channel.send('Hello World')

    # test Discord.py abc
    if 'testid' in message.content.lower():
        await message.channel.send(message.author.id)
        await message.channel.send(message.author.display_name)
        await message.channel.send(message.author.mention)
        await message.channel.send(message.author.avatar)
        await message.channel.send(message.author.discriminator)

    # test
    if 'tvar' in message.content.lower():
        sender = message.author.display_name
        await message.channel.send ('Yes, hello ' + sender + ' \nHello World')

    # check the message has "bf4" anywhere
    if 'bf4' in message.content.lower():

        # check the message has "sven" as well
        if 'sven' in message.content.lower():

            # check the message that it was from 408532966080512000 which is rod
            if message.author.id == 408532966080512000:
                await message.channel.send('when is sc2 tho <@408532966080512000>') # a twist reply
                ## todo
                ## make the twist reply a random game

        # check the message that it was from 408532966080512000 which is rod, again
        elif message.author.id == 408532966080512000:
            await message.channel.send('when is sven tho <@408532966080512000>')
        
        # the sender was not rod and did not contain both "bf4" and "sven"
        else:
            await message.channel.send('ask <@408532966080512000>')

    # check the message has "sven" anywhere
    if 'sven' in message.content.lower():
        # removed as it's redundant
        ##if 'bf4' in message.content.lower():
            ##if message.author.id == 408532966080512000:
            ##    await message.channel.send('when is ze tho <@408532966080512000>')

        # check the message that it was from 408532966080512000 which is rod, again
        if message.author.id == 408532966080512000:
            await message.channel.send('when is bf4 tho <@408532966080512000>')

        # the sender was not rod and did not contain both "sven" and "bf4"    
        else:
            await message.channel.send('ask <@408532966080512000>')

client.run('TOKEN')