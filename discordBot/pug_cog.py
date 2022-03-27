import discord
from discord.ext import commands

import asyncio
from random import randint
from random import shuffle

class pug(commands.Cog):
    def __init__(self, client):
        self.client = client

        self.player_list = []
        self.team1 = []
        self.team2 = []
    
    ## TODO ###############################
    ## store both display name and id #####
    ## id is unique, display name is not ##
    #######################################

    # .join will add the messager's display name into the player list
    @commands.command(name = 'join')
    async def join_queue(self, ctx):
        if ctx.author.display_name in self.player_list: # if the player is already on the list
            await ctx.send(ctx.author.mention + ' you are already in the queue')   
        else:
            self.player_list.append(ctx.author.display_name) # otherwise add them to the list
            await ctx.send(ctx.author.mention + ' you have joined the queue as [' + str(len(self.player_list)) + ']')
    
    # .start will initiate the functions in this cog
    @commands.command(name = 'start')
    async def matchmake(self, ctx):
        shuffle(self.player_list)
        shuffle(self.player_list)
        shuffle(self.player_list)

        i = 0

        # team assignment
        for i in range(0, len(self.player_list)):
            # evens on the list join team 2
            if (i % 2) == 0:
                self.team2.append(self.player_list[i])
            
            # odds are team 1
            else:
                self.team1.append(self.player_list[i])
    
            i += 1
            if i >= len(self.player_list): break

        await ctx.send('*Starting matchmake...*')
        await asyncio.sleep(1)
        await ctx.send('*...*')
        await asyncio.sleep(1)

        # send message block for team 1
        await ctx.send('> --Team 1--\n' + '\n'.join(self.team1) + '\n> --Team 2--\n' + '\n'.join(self.team2))

    # .queued will display the player list
    @commands.command(name = 'queued')
    async def display_queue(self, ctx):
        if not self.player_list:
            await ctx.send('The queue is empty')
        else:
            await ctx.send('\n'.join(self.player_list + '\nTotal Players: ' + str(len(self.player_list))))

    # .quit will remove the messager's display name out the player list
    @commands.command(name = 'quit')
    async def leave_queue(self, ctx):
        self.player_list.remove(ctx.author.display_name)
        await ctx.send(ctx.author.mention + ' you have left the queue')

    # .add will add a custom name into the player list
    # mostly for testing purposes but can be used to generate a player
    @commands.command(name = 'add')
    async def add_player(self, ctx, *args):
        player = ''.join(args)
        self.player_list.append(player)
        await ctx.send(player + ' has been added as [' + str(len(self.player_list)) + ']')

    ## TODO ##
    ## a better remove command ##
    #############################

    # .remove will remove whoever is in said position
    @commands.command(name = 'remove')
    async def remove_player(self, ctx, *args):
        slot_position = ''.join(args)
        if not self.player_list:
            await ctx.send('The queue is empty')
        else:
            if isinstance(slot_position, int) == True:
                ctx.send(self.player_list[slot_position] + ' has been removed')
                self.player_list.remove(slot_position+1)
            else:
                ctx.send('Not an integer. Try again.')

    @commands.command(name = 'team1')
    async def check_team1(self, ctx):
        if not self.team1:
            await ctx.send('> --Team 1--\n**Empty**')
        else:
            await ctx.send('> --Team 1--\n' + '\n'.join(self.team1))

    @commands.command(name = 'team2')
    async def print_team2(self, ctx):
        if not self.team2:
            await ctx.send('> --Team 2--\n**EMPTY**')
        else:
            await ctx.send('> --Team 2--\n' + '\n'.join(self.team2))

    @commands.command(name = 'clear')
    async def clear_all(self, ctx):
        self.player_list.clear()
        self.team1.clear()
        self.team2.clear()
        await ctx.send('All cleared')

    @commands.command(name = 'clearteams')
    async def clear_team1(self, ctx):
        self.team1.clear()
        self.team2.clear()
        await ctx.send('Teams cleared')

    @commands.command(name = 'clearqueue')
    async def clear_player_list(self, ctx):
        self.player_list.clear()
        await ctx.send('Queue cleared')