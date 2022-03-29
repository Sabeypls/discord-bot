from operator import index
import discord
from discord.ext import commands
from discord.utils import get

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

    # .join will add the sender's member object into the player_list
    @commands.command(name = 'join')
    async def join_queue(self, ctx):
        # if sender's member object is not found in player_list, add them to player_list
        if ctx.message.author not in self.player_list:
            # get role "in queue..."
            role = get(ctx.guild.roles, name='in queue...')

            # add role "in queue..." to message.author and then add their member object into player_list
            await ctx.message.author.add_roles(role)
            self.player_list.append(ctx.message.author)

            # print message
            await ctx.send(ctx.author.mention + ' you\'ve joined the queue', delete_after=3)

            # debugging
            print(self.player_list)

        # sender's member object is found, do not add them to player_list
        else:
            await ctx.send(ctx.author.mention + ' you\'ve already joined the queue', delete_after=3)
    
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
            if len(self.player_list) >= 2:
                # 2 shuffles
                shuffle(self.player_list)
                shuffle(self.player_list)
                
                # split in halves
                split = numpy.array_split(self.player_list, 2)
                
                # storage
                self.team1 = list(split[0])
                self.team2 = list(split[1])

                # get roles: "Team 1", "Team 2", and "in queue..."
                role1 = get(ctx.guild.roles, name='Team 1')
                role2 = get(ctx.guild.roles, name='Team 2')
                roleq = get(ctx.guild.roles, name='in queue...')
                
                # debugging
                print(split[0])
                print(split[1])

                # uneven player_list will be handled by split
                # half into team 1
                for member in split[0]:
                    await member.add_roles(role1)
                    await member.remove_roles(roleq)

                # other half into team 2
                for member in split[1]:
                    await member.add_roles(role2)
                    await member.remove_roles(roleq)

                # print message
                await ctx.send('__**Team 1**__\n```' + '\n'.join(list(map(lambda x:x.name, split[0]))) + ' ```\n__**Team 2**__\n```' + '\n'.join(list(map(lambda x:x.name, split[1]))) + '\n```', delete_after=30)

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
            await ctx.send('\n'.join(list(map(lambda x:x.name, self.player_list))) + '\nTotal Players: ' + str(len(self.player_list)), delete_after=10)

    # .quit will remove the messager's display name out the player list
    @commands.command(name = 'quit')
    async def leave_queue(self, ctx):
        # if the sender wants to leave but is found in team1 or team2
        if ctx.message.author in self.team1 or ctx.message.author in self.team2:
            # notify the PUG Leader so they can remove them
            role = get(ctx.guild.roles, name='PUG Leader')
            await ctx.send(role.mention + ', ' + ctx.author.mention + ' wants to leave')

        # else they sender was only found in player_list, remove them from player_list
        else:
            if ctx.message.author in self.player_list:
                role = get(ctx.guild.roles, name='in queue...')

                self.player_list.remove(ctx.message.author)
                await ctx.message.author.remove_roles(role)
                await ctx.send(ctx.author.mention + ' you\'ve left the queue', delete_after=3)
            
            # they were never in queue to begin with!
            else:
                await ctx.send('You, ' + ctx.author.mention + ', we\'re never in queue')

    # .add will force a user to join
    @commands.command(name = 'add')
    @commands.has_role('PUG Leader')
    async def add_player(self, ctx, *args):
        input = ''.join(args)
        
        ## transforming input to fit our needs
        # @user -> <@!###user###> -> ###user###
        input = input.replace('<@!', '')
        input = input.replace('>', '')

        # -> int user
        if input.isdigit() == True:
            input = int(input)
        # username#discriminator -> Username
        # or just username -> Username
        else:
            input = input.split('#', 1)[0]
            input = input.capitalize()

        role = get(ctx.guild.roles, name='in queue...')

        # removed for now
        # or input in list(map(lambda x: x.name.lower() + '#' + x.discriminator, ctx.guild.members))
        #

        if input in list(map(lambda x: x.name, ctx.guild.members)) or input in list(map(lambda x: x.id, ctx.guild.members)):
            # if input is an int use get_member as it passes only int
            if isinstance(input, int):
                member = ctx.guild.get_member(input)
            # else use get_member_named as it passes only str
            else:
                member = ctx.guild.get_member_named(input)

            if member not in self.player_list:
                await member.add_roles(role)
                self.player_list.append(member)
                await ctx.send(member.mention + ' you\'ve been added to the queue')
            else:
                await ctx.send(member.display_name + ' is already in queue', delete_after=10)

        else:
            await ctx.send(str(input) + ' was not found in this discord or is an invalid format (i.e. capitalization)', delete_after=10)         

    # .remove will remove
    @commands.command(name = 'remove')
    @commands.has_role('PUG Leader')
    async def remove_player(self, ctx, *args):
        input = ''.join(args)

        # @user -> <@!###user###> -> ###user###
        input = input.replace('<@!', '')
        input = input.replace('>', '')

        # -> int user
        if input.isdigit() == True:
            input = int(input)
        # username#discriminator -> Username
        # or just username -> Username
        else:
            input = input.split('#', 1)[0]
            input = input.capitalize()

        # get roles: "Team 1", "Team 2", and "in queue..."
        role1 = get(ctx.guild.roles, name='Team 1')
        role2 = get(ctx.guild.roles, name='Team 2')
        roleq = get(ctx.guild.roles, name='in queue...')

        if input in list(map(lambda x: x.name, ctx.guild.members)) or input in list(map(lambda x: x.id, ctx.guild.members)):
            # if input is an int use get_member as it passes only int
            if isinstance(input, int):
                member = ctx.guild.get_member(input)
            # else use get_member_named as it passes only str
            else:
                member = ctx.guild.get_member_named(input)

            # if member is found in player_list, team1, or team2
            if member in self.player_list or member in self.team1 or member in self.team2:
                # if we entered here cause of player_list
                # remove member's role, in queue..., and delete them off player_list 
                if member in self.player_list:   
                    await member.remove_roles(roleq)
                    self.player_list.remove(member)
                
                # if we entered here cause of team1
                # remove member's role, team 1, and delete them off team1
                if member in self.team1:
                    await member.remove_roles(role1)
                    self.team1.remove(member)

                # if we entered her cause of team2
                # remove member's role, team 2, and delete them off team2
                if member in self.team2:
                    await member.remove_roles(role2)
                    self.team2.remove(member)

                await ctx.send(member.mention + ' you\'ve been removed', delete_after=5)

            else:
                await ctx.send(str(input) + ' was not found in queue, team 1, or team 2 list', delete_after=10)

        else:
            await ctx.send(str(input) + ' was not found in this discord or is an invalid format (i.e. capitalization)', delete_after=10)

    # .team will print team1 list
    @commands.command(name = 'team1')
    async def check_team1(self, ctx):
        if not self.team1:
            await ctx.send('__**Team** 1__\n> **Empty**', delete_after=10)
        else:
            await ctx.send('__**Team 1**__\n```\n' + '\n'.join(list(map(lambda x:x.name, self.team1))) + '\n```', delete_after=15)

    # .team2 will print team2 list
    @commands.command(name = 'team2')
    async def print_team2(self, ctx):
        if not self.team2:
            await ctx.send('__**Team 2**__\n> **Empty**', delete_after=10)
        else:
            await ctx.send('__**Team 2**__\n```\n' + '\n'.join(list(map(lambda x:x.name, self.team2))) + '\n```', delete_after=15)

    # .clear will empty both teams and the player list
    @commands.command(name = 'clearall')
    @commands.has_role('PUG Leader')
    async def clear_all(self, ctx):
        # get roles: "Team 1", "Team 2", and "in queue..."
        role1 = get(ctx.guild.roles, name='Team 1')
        role2 = get(ctx.guild.roles, name='Team 2')
        roleq = get(ctx.guild.roles, name='in queue...')

        for member in self.player_list:
            await member.remove_roles(role1, role2, roleq)

        self.player_list.clear()
        self.team1.clear()
        self.team2.clear()

        await ctx.send('All cleared', delete_after=5)

    # .clearteams will empty both teams but not the player list
    @commands.command(name = 'clearteams')
    @commands.has_role('PUG Leader')
    async def clear_team1(self, ctx):
        # get roles: "Team 1", "Team 2", and "in queue..."
        role1 = get(ctx.guild.roles, name='Team 1')
        role2 = get(ctx.guild.roles, name='Team 2')
        roleq = get(ctx.guild.roles, name='in queue...')

        for member in self.player_list:    
            await member.remove_roles(role1, role2, roleq)

        self.team1.clear()
        self.team2.clear()
        await ctx.send('Teams cleared', delete_after=5)

    # .clearqueue will empty the player list
    @commands.command(name = 'clearqueue')
    @commands.has_role('PUG Leader')
    async def clear_player_list(self, ctx):
        # get roles "in queue..."
        roleq = get(ctx.guild.roles, name='in queue...')

        for member in self.player_list:
            await member.remove_roles(roleq)

        self.player_list.clear()
        await ctx.send('Queue cleared', delete_after=5)
    
    @commands.command(name = 'cleanup')
    @commands.has_role('PUG Leader')
    async def clean_up(self, ctx):
        role1 = get(ctx.guild.roles, name='Team 1')
        role2 = get(ctx.guild.roles, name='Team 2')
        roleq = get(ctx.guild.roles, name='in queue...')
        ctx.send('This process can take a while\nCleaning...')

        for member in ctx.guild.members:
            await member.remove_roles(role1, role2, roleq)

        ctx.send('Cleaning completed')
    
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

    @commands.command(name = 'check')
    async def debug(self, ctx):
        print('\n\n')
        print('player_list = '+str(self.player_list)+'\n')
        print('team1 = '+str(self.team1)+'\n')
        print('team2 = '+str(self.team2)+'\n')
        print('\n')
        await ctx.send('Checking')
    
    ## TODO ####
    ## expand ##

    # all the error handling for commands that require a role
    @matchmake.error
    async def matchmake_error(self, ctx, error):
        role = get(ctx.guild.roles, name='PUG Leader')
        if isinstance(error, commands.MissingRole):
            if error.missing_role.id == role.id:
                await ctx.send('Denied: missing **[PUG Leader]** role', delete_after=5)
        else:
            raise error