import discord
from discord.ext import commands

from random import randint
from random import shuffle

class pug(commands.Cog):
    def __init__(self, client):
        self.client = client

        self.player_list = []
        self.team1 = []
        self.team2 = []
    
    # this function will shuffle the player list
    def shuffle_random(self):
        self.player_list = shuffle(self.player_list)

    # this function will assign players into teams
    def team_assignment(self):
        i = 0

        for i in range(0, len(self.player_list)):
            # if 0 or even on the list join team 2
            if (i % 2) or i == 0:
                self.team2.append(self.player_list[i])
            
            # otherwise, odds are team 1
            else:
                self.team1.append(self.player_list[i])
    
            i += 1

    # this function will post team 1 and 2 in chat
    async def print_teams(self, ctx):
        num1 = 0
        num2 = 0

        # send message block for team 1
        ctx.send('>--Team 1-- \n')
        for num1 in range(0, len(self.team1)):
            ctx.send(self.team1[num1] + '\n')
            num1 += 1

        # send message block for team 2
        ctx.send('>--Team 2-- \n')
        for num2 in range(0, len(self.team2)):
            ctx.send(self.team2[num2] + '\n')
            num2 += 1
    
    ## TODO ###############################
    ## store both display name and id #####
    ## id is unique, display name is not ##

    # .join will add the messager's display name into the player list
    @commands.command(name = 'join')
    async def join_queue(self, ctx):
        self.player_list.append(ctx.author.display_name)
        ctx.send(ctx.author.mention + ' you have joined the queue')
    
    # .start will initiate the functions in this cog
    @commands.command(name = 'start')
    async def matchmake(self, ctx):
        self.shuffle_random
        self.team_assignment
        self.print_teams
        self.player_list.clear()

    # .queued will display the player list
    @commands.command(name = 'queued')
    async def display_queue(self, ctx):
        i = 0

        for i in range(0, len(self.player_list)):
            ctx.send('1) ' + self.player_list[i] + '\n')
            i += 1

    # .quit will remove the messager's display name out the player list
    @commands.command(name = 'quit')
    async def leave_queue(self, ctx):
        self.player_list.remove(ctx.author.display_name)
        ctx.send(ctx.author.mention + ' you have left the queue')