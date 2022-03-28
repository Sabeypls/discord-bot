import discord
from discord.ext import commands
from discord.utils import get
from discord.message import Message
from discord.member import Member

###################
## TODO ###########
## ^^^^^^^^^^^^^ ##
## sort this out ##
###################

import numpy
import asyncio
from random import shuffle

class pug(commands.Cog):
    def __init__(self, client):
        self.client = client

        self.player_list = []
        self.team1 = []
        self.team2 = []

        self.channel1 = 939799812822409226
        self.channel2 = 939799877720879125

    # .join will add the messager's display name into the player list
    @commands.command(name = 'join')
    async def join_queue(self, ctx):
        role = get(ctx.guild.roles, name='in queue...')

        await ctx.send(ctx.author.mention + ' you have joined the queue')

        await ctx.message.author.add_roles(role)
        self.player_list.append(ctx.message.author)
        
        print(self.player_list)
    
    # .start will initiate the functions in this cog
    @commands.command(name = 'start')
    @commands.has_role('PUG Leader')
    async def matchmake(self, ctx):
        # if player list is empty
        if not self.player_list:
            await ctx.send('0 Players detected')
        # player list has elements
        else:
            # check if there are at least 2 elements in player list
            if len(self.player_list >= 2):
                # 2 shuffles
                shuffle(self.player_list)
                shuffle(self.player_list)
                
                # split in halves
                split = numpy.array_split(self.player_list, 2)

                role1 = get(ctx.guild.roles, name='Team 1')
                role2 = get(ctx.guild.roles, name='Team 2')
                roleq = get(ctx.guild.roles, name='in queue...')
                
                # debugging
                print(split[0])
                print(split[1])

                for member in split[0]:
                    await member.add_roles(role1)
                    await member.remove_roles(roleq)

                for member in split[1]:
                    await member.add_roles(role2)
                    await member.remove_roles(roleq)

                await ctx.send('> --Team 1--\n' + '\n'.join(list(map(lambda x:x.name, split[0]))) + '\n> --Team 2--\n' + '\n'.join(list(map(lambda x:x.name, split[1]))), delete_after=30)

            # error there's only 1 player        
            else:
                await ctx.send('You can\'t matchmake with only 1 player!')

    # .queued will display the player list
    @commands.command(name = 'queue')
    async def display_queue(self, ctx):
        # if player list is empty
        if not self.player_list:
            await ctx.send('The queue is empty', delete_after=5)
        # player list has elements
        else:
            await ctx.send('\n'.join(self.player_list + '\nTotal Players: ' + str(len(self.player_list))), delete_after=10)

    ##############
    ## TODO ######
    ## fix this ##
    ## VVVVVVVV ##
    ##############

    # .quit will remove the messager's display name out the player list
    @commands.command(name = 'quit')
    async def leave_queue(self, ctx):
        self.player_list.remove(ctx.author.display_name)
        await ctx.send(ctx.author.mention + ' you have left the queue', delete_after=10)

    ##############
    ## TODO ######
    ## fix this ##
    ## VVVVVVVV ##
    ##############

    # .add will add a custom name into the player list
    # mostly for testing purposes but can be used to generate a player
    @commands.command(name = 'add')
    @commands.has_role('PUG Leader')
    async def add_player(self, ctx, *args):
        player = ''.join(args)
        self.player_list.append(player)
        await ctx.send(player + ' has been added as [' + str(len(self.player_list)) + ']', delete_after=10)

    ##############
    ## TODO ######
    ## fix this ##
    ## VVVVVVVV ##
    ##############

    # .remove will remove whoever is in said position
    @commands.command(name = 'remove')
    @commands.has_role('PUG Leader')
    async def remove_player(self, ctx, *args):
        slot_position = ''.join(args)

        # if player list is empty
        if not self.player_list:
            await ctx.send('The queue is empty', delete_after=5)
        # player list has elements
        else:
            # if argument is a integer
            if isinstance(slot_position, int) == True:
                # if argument is within the list range, remove player_list[arg-1]
                if slot_position-1 <= len(self.player_list and slot_position-1 >= 0):
                    await ctx.send(self.player_list[slot_position] + ' has been removed', delete_after=10)
                    self.player_list.remove(slot_position-1)
                # argument was outside of the range
                else:
                    await ctx.send('Position ' + slot_position + ' does not exist')
            # argument was not an integer
            else:
                ctx.send('Not an integer. Try again.')

    ##############
    ## TODO ######
    ## fix this ##
    ## VVVVVVVV ##
    ##############

    # .team will print team1 list
    @commands.command(name = 'team1')
    async def check_team1(self, ctx):
        if not self.team1:
            await ctx.send('> --Team 1--\n**Empty**', delete_after=10)
        else:
            await ctx.send('> --Team 1--\n' + '\n'.join(self.team1[0]), delete_after=15)

    ##############
    ## TODO ######
    ## fix this ##
    ## VVVVVVVV ##
    ##############

    # .team2 will print team2 list
    @commands.command(name = 'team2')
    async def print_team2(self, ctx):
        if not self.team2:
            await ctx.send('> --Team 2--\n**EMPTY**', delete_after=10)
        else:
            await ctx.send('> --Team 2--\n' + '\n'.join(self.team2[0]), delete_after=15)

    ##############
    ## TODO ######
    ## fix this ##
    ## VVVVVVVV ##
    ##############

    # .clear will empty both teams and the player list
    @commands.command(name = 'clear')
    @commands.has_role('PUG Leader')
    async def clear_all(self, ctx):
        self.player_list.clear()
        self.team1.clear()
        self.team2.clear()
        await ctx.send('All cleared', delete_after=5)

    ##############
    ## TODO ######
    ## fix this ##
    ## VVVVVVVV ##
    ##############

    # .clearteams will empty both teams but not the player list
    @commands.command(name = 'clearteams')
    @commands.has_role('PUG Leader')
    async def clear_team1(self, ctx):
        self.team1.clear()
        self.team2.clear()
        await ctx.send('Teams cleared', delete_after=5)

    ##############
    ## TODO ######
    ## fix this ##
    ## VVVVVVVV ##
    ##############

    # .clearqueue will empty the player list
    @commands.command(name = 'clearqueue')
    @commands.has_role('PUG Leader')
    async def clear_player_list(self, ctx):
        self.player_list.clear()
        await ctx.send('Queue cleared', delete_after=5)
    
    ###############
    ## TODO #######
    ## test this ##
    ## VVVVVVVVV ##
    ###############

    # .setvc1 will assign a channel for team 1 to connect to
    @commands.command(name = 'setvc1')
    @commands.has_role('PUG Leader')
    async def set_channel1(self, ctx, *args):
        channel_id = ''.join(args)

        # check argument is a int
        if isinstance(channel_id, str) == True:
            # attempt to connect to the voice channel id
            await self.connect(channel_id)
            
            # if connected, set channel
            if self.is_connected == True:
                self.vc1 = channel_id

                await ctx.send('*Checking...*', delete_after=1)
                asyncio.sleep(1)
                await ctx.send('Channel Set', delete_after=5)
                
                # disconnect after
                self.disconnect()
            # if failed to connect, channel id or int provided is invalid
            else:
                await ctx.send('Not a valid channel id')
        # argument was not an int
        else:
            await ctx.send('Not a valid input')

    ###############
    ## TODO #######
    ## test this ##
    ## VVVVVVVVV ##
    ###############

    @commands.command(name = 'setvc2')
    @commands.has_role('PUG Leader')
    async def set_channel2(self, ctx, *args):
        channel_id = ''.join(args)

        # check argument is a int
        if isinstance(channel_id, str) == True:
            # attempt to connect to the voice channel id
            await self.connect(channel_id)
            
            # if connected, set channel
            if self.is_connected == True:
                self.vc2 = channel_id

                await ctx.send('*Checking...*', delete_after=1)
                asyncio.sleep(1)
                await ctx.send('Channel Set', delete_after=5)
                
                # disconnect after
                self.disconnect()
            # if failed to connect, channel id or int provided is invalid
            else:
                await ctx.send('Not a valid channel id')
        # argument was not an int
        else:
            await ctx.send('Not a valid input')
    
    ##############
    ## TODO ######
    ## fix this ##
    ## VVVVVVVV ##
    ##############
    
    # all the error handling for commands that require a role
    #@matchmake.error
    #async def matchmake_error(ctx, error):
    #    if isinstance(error, commands.MissingRole):
    #        await ctx.send('Missing **[PUG Leader]** role', delete_after=5)