import discord
from discord.ext import commands, tasks
from random import randint

client = commands.Bot(command_prefix = '.')
client.load_extension('pug_cog')
client.load_extension('music_cog')
client.load_extension('rod_cog')
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

@client.command()
@commands.is_owner()
async def reload(ctx, extension):
    extension = extension+'_cog'
    client.reload_extension(extension)
    embed = discord.Embed(title='Reload', description=f'{extension} successfully reloaded', color=0xff00c8)
    await ctx.send(embed=embed)

client.run('MjMzNzAxNzQxMTk4MDQ5Mjgx.V_bBtQ.W0L7eiFGPUP20ja_bel5Oe2ipGo')