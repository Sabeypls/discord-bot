from discord.ext import commands
from random import randint
import discord

class func(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='coinflip')
    async def coinflip(self, ctx, guess=None):
        results = randint(0, 1)
        if guess == None:
            if results == 0:
                embed = discord.Embed(title='Results', description='Heads')
                embed.set_thumbnail(url='https://www.pngitem.com/pimgs/m/129-1296175_washington-quarter-silver-1944s-obverse-us-coin-heads.png')
            else:
                embed = discord.Embed(title='Results', description='Tails')
                embed.set_thumbnail(url='https://www.pngitem.com/pimgs/m/695-6953354_quarter-tails-clipart-hd-png-download.png')

        else:
            if isinstance(guess, str):
                if len(guess) == 4 or len(guess) == 5:
                    if guess.lower() == 'heads' or guess.lower() == 'head':
                        if results == 0:
                            embed = discord.Embed(title='Results', description='Heads. ' + ctx.author.mention + ' guessed it correctly.')
                        else:
                            embed = discord.Embed(title='Results', description='Tails. ' + ctx.author.mention + ' guessed it wrong.')

                        embed.set_thumbnail(url='https://www.pngitem.com/pimgs/m/129-1296175_washington-quarter-silver-1944s-obverse-us-coin-heads.png')

                    elif guess.lower() == 'tails' or guess.lower() == 'tail':
                        if results == 0:
                            embed = discord.Embed(title='Results', description='Tails. ' + ctx.author.mention + ' guessed it wrong.')
                        else:
                            embed = discord.Embed(title='Results', description='Tails. ' + ctx.author.mention + ' guessed it correctly')

                        embed.set_thumbnail(url='https://www.pngitem.com/pimgs/m/695-6953354_quarter-tails-clipart-hd-png-download.png')

                    else: # it was 4 or 5 letters but not head, heads, tail, or tails
                        embed = discord.Embed(title='Error', description='Invalid input.')  

                else: # it was not 4 or 5 letters
                    embed = discord.Embed(title='Error', description='Invalid input.')

            else: # it was not a string
                embed = discord.Embed(title='Error', description='Invalid input.')
        
        await ctx.send(embed=embed)

    @commands.command(name='dice')
    async def dice_roll(self, ctx, max=None):
        if max == None:
                embed = discord.Embed(title='Results', description=ctx.author.mention + ' rolled a d6 die.\nIt landed on ' + str(randint(1, 6)))

        elif max.isdigit():
            if int(max) > 1:
                embed = discord.Embed(title='Results', description=ctx.author.mention + ' rolled a d' + str(max) + ' die.\nIt landed on ' + str(randint(1, int(max))))
            
            elif int(max) < 0:
                embed = discord.Embed(title='Error', description='Invalid input.')

            elif int(max) == 0:
                embed = discord.Embed(title='Results', description='You rolled a ball.\nIt doesn\'t stop rolling.')

            elif int(max) == 1:
                embed = discord.Embed(title='Results', description='You rolled a Möbius strip.\nIt landed on 1.')

            else:
                embed = discord.Embed(title='Error', description='Invalid input.')

        else:
            embed = discord.Embed(title='Error', description='Invalid input.')

        await ctx.send(embed=embed)
        
    @commands.command(name='poll')
    @commands.cooldown(1, 15.0, commands.BucketType.guild)
    async def poll(self, ctx, question, *args):
        emoji = ['1️⃣','2️⃣','3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']

        await ctx.message.delete()
        embed = discord.Embed(title=ctx.author.display_name + ' asked...', description=question)

        if len(args) == 0:
            embed.add_field(name='1️⃣', value='Yes', inline=True)
            embed.add_field(name='2️⃣', value='No', inline=True)
            message = await ctx.send(embed=embed)
            await message.add_reaction('1️⃣')
            await message.add_reaction('2️⃣')

        elif len(args) < 2:
            embed = discord.Embed(title='Error', description='Cannot poll with only 1 prompt. Baka.')
            await ctx.send(embed=embed)

        elif len(args) > 9:
            embed = discord.Embed(title='Error', description='Keep it under 9 please.')
            await ctx.send(embed=embed)

        else:
            i = 0
            while i < len(args):
                embed.add_field(name=emoji[i], value=args[i], inline=True)
                i += 1
                
            message = await ctx.send(embed=embed)

            i = 0
            while i < len(args):
                await message.add_reaction(emoji[i])
                i += 1

    @commands.command(name='test')
    async def test_func(self, ctx):
        print('test')
        # empty for now

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        bot = 233701741198049281
        if user.id != bot:
            msg = discord.utils.get(self.client.cached_messages, id=reaction.message.id)

            for rct in msg.reactions:
                if user in await rct.users().flatten() and user.id != bot and str(rct) != str(rct.emoji):
                    if msg.author.id == bot:
                        await msg.remove_reaction(rct.emoji, user)

# on bot start up
# add this cog
# used to reload this cog so the bot doesn't have to go down to update
def setup(client):
    client.add_cog(func(client))