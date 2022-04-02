import discord
from discord.ext import commands, tasks
from random import randint

client = commands.Bot(command_prefix = '.')
client.load_extension('pug_cog')
client.load_extension('music_cog')
#client.load_extension('twitter_cog')
# soon?

# connection establish
@client.event
async def on_ready():
    print('{0.user} is ready'.format(client))
    await client.wait_until_ready()
    change_games.start()

@tasks.loop(minutes=2.0)
async def change_games():
    games = ['nothing', 'Nothing', 'Lost Ark', 'Final Fantasy XIV', 'Counter-Strike: Global Offensive', 'Valorant', 'League of Legends',\
         'Battlefield 4', 'Battlefield 3', 'Overwatch', 'Jackbox', 'Codenames', 'Youtube', 'Twitch', 'Twitter', 'Fortnite', 'Call of Duty: Warzone', 'Halo Infinite',\
             'Golf With Your Friends', 'Golf It!', 'Elden Ring', 'Fallout 4', 'Street Fighter V', 'Grand Theft Auto V', 'Dota 2', 'VRChat', 'Facebook', 'E-Mails',\
                'Yu-Gi-Oh!', 'Magic: The Gathering', 'Digimon', 'Pokemon', 'something', 'none of your business!']
    i = randint(0, len(games)-1)
    await client.change_presence(activity=discord.Game(games[i]))

# reading messages
@client.event
async def on_message(message):
    # prevents self looping
    if message.author == client.user:
        return

    # check the message has "bf4" anywhere
    if 'bf4' in message.content.lower():

        # check the message has "sven" as well
        if 'sven' in message.content.lower():

            # check the message that it was from 408532966080512000 which is rod
            if message.author.id == 408532966080512000:
                list = ['sc2', 'gtav', 'gta5', 'lost ark', 'ze', 'mg', 'poker night', 'codenames', 'minigames', 'starcraft 2', 'grand theft auto 5', 'grand theft auto five',
                                    'synergy', 'hl2dm', 'half-life 2: death match', 'counter-strike: global offensive', 'l4d2', 'left 4 dead 2', 'valorant', 'league of legends', 'lol']
                i = randint(0, len(list)-1)
                await message.channel.send('when is ' + list[i] + ' tho <@408532966080512000>') # a twist reply

        # check the message that it was from 408532966080512000 which is rod, again
        elif message.author.id == 408532966080512000:
            await message.channel.send('when is sven tho <@408532966080512000>')
        
        # the sender was not rod and did not contain both "bf4" and "sven"
        else:
            await message.channel.send('<@408532966080512000>')

    # check the message has "sven" anywhere
    if 'sven' in message.content.lower():
        # check the message that it was from 408532966080512000 which is rod, again
        if message.author.id == 408532966080512000:
            await message.channel.send('when is bf4 tho <@408532966080512000>')

        # the sender was not rod and did not contain both "sven" and "bf4"    
        else:
            await message.channel.send('ask <@408532966080512000>')
    
    await client.process_commands(message)

@client.command()
@commands.is_owner()
async def reload(ctx, extension):
    extension = extension+'_cog'
    client.reload_extension(extension)
    embed = discord.Embed(title='Reload', description=f'{extension} successfully reloaded', color=0xff00c8)
    await ctx.send(embed=embed)

client.run('TOKEN')