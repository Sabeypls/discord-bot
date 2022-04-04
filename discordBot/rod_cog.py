import discord
from discord.ext import commands
from discord.utils import get
import subprocess
import asyncio

class rod(commands.Cog):
    def __init__(self, client):
        self.client = client
        
        self.flag = 0
        self.check = 0

    # .startsven will open svends on my desktop
    @commands.command(name='startsven')
    @commands.has_role('When\'s Sven @rod#0581')
    async def start_sven_server(self, ctx):
        # check if the flag is down, signifying svends is off
        if self.flag == 0:
            # flag up
            self.flag = 1

            await ctx.message.delete()
            await ctx.send('Starting Sven...', delete_after=15)
            
            # in a subprocess, open svends
            subprocess.Popen('D:\SteamServer\sven\\start.bat')

            # important message for rod
            rodmessage = discord.Embed(title='@Rod', description='***PLEASE*** close the server\
                \n__**.stopsven**__ to close the server\n__**.restartsven**__ to restart the server\n\n\
                **(.stopsven is a vote command that requires 2 people if __*Rod*__ does __*NOT*__ do his job)**', color=0xff00c8)
            
            await ctx.send(embed=rodmessage)

        else:
            await ctx.send('The server is up')

    # .stopsven will taskkill svends
    @commands.command(name='stopsven')
    async def stop_sven_server(self, ctx):
        # check if the flag is up, signifying svends is up
        if self.flag == 1:
            self.flag = 0
            role = get(ctx.guild.roles, name='When\'s Sven @rod#0581')
            
            # those with higher permission (role) can close svends
            if role in ctx.author.roles:
                subprocess.call('taskkill /IM svends.exe /F')
                await ctx.message.delete()
                await ctx.send('Fuck Rod', delete_after=15)
            
            # those without permission (role) will have to band together
            # mostly for people without to do the job of those higher up
            elif self.check == 1:
                self.check = 0
                subprocess.call('taskkill /IM svends.exe /F')
                await ctx.send('Ending Sven...', delete_after=15)
                await ctx.send('Thank you, ' + ctx.author.mention + ', for using .stopsven. Vote passed .stopsven vote (2/2)')
            
            else:
                self.check += 1
                await ctx.message.delete()
                await ctx.send('Thank you, ' + ctx.author.mention + ', for using .stopsven. Need 1 more .stopsven vote (1/2)')
        
        else:
            await ctx.send('The server is not up')

    # .restart sven will taskkill svends and reopen it again
    @commands.command(name='restartsven')
    @commands.has_role('When\'s Sven @rod#0581')
    async def restart_sven_server(self, ctx):
        # check flag if up, signifying svends is up
        if self.flag == 1:
            await ctx.message.delete()
            subprocess.call('taskkill /IM svends.exe /F')
            asyncio.sleep(5)
            subprocess.Popen('D:\SteamServer\sven\\start.bat')
        else:
            await ctx.send('The server is not up')

# on bot start up
# add this cog
# used to reload this cog so the bot doesn't have to go down to update
def setup(client):
    client.add_cog(rod(client))