from discord.ext import commands
from discord.utils import get
from random import randint, shuffle
import numpy

class pug(commands.Cog):
    def __init__(self, client):
        self.client = client

        self.player_list = []
        self.team1 = []
        self.team2 = []

    # .join will add the user's object into the player_list
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
            await ctx.message.delete()
            await ctx.send(ctx.author.mention + ' you\'ve joined the queue', delete_after=5)

        else:
            await ctx.send(ctx.author.mention + ' you\'ve already joined the queue', delete_after=5)

     # .quit will remove the user from the player_list
    @commands.command(name = 'quit')
    async def leave_queue(self, ctx):
        # if the sender wants to leave but is found in team1 or team2
        if ctx.message.author in self.team1 or ctx.message.author in self.team2:
            # notify the PUG Leader so they can remove them
            role = get(ctx.guild.roles, name='PUG Leader')
            await ctx.message.delete()
            await ctx.send(role.mention + ', ' + ctx.author.mention + ' wants to leave')

        # else the sender was only found in player_list, remove them from player_list
        else:
            if ctx.message.author in self.player_list:
                role = get(ctx.guild.roles, name='in queue...')

                self.player_list.remove(ctx.message.author)
                await ctx.message.author.remove_roles(role)
                await ctx.message.delete()
                await ctx.send(ctx.author.mention + ' you\'ve left the queue', delete_after=7)
            
            else:
                await ctx.message.delete()
                await ctx.send('You, ' + ctx.author.mention + ', we\'re never in queue')

    # .start begins matchmaking 
    # setting and removing the appropriate roles and adding them to team1 and team2
    @commands.command(name = 'start')
    @commands.has_role('PUG Leader')
    async def matchmake(self, ctx):
        # if player list is empty
        if not self.player_list:
            await ctx.message.delete()
            await ctx.send('0 Players detected')

        # player list has elements
        else:
            # check if there are at least 2 elements in player_list
            if len(self.player_list) >= 2:
                # 2 shuffles
                shuffle(self.player_list)
                shuffle(self.player_list)

                # uneven handling
                if (len(self.player_list) % 2) != 0:
                    oddman = self.player_list.pop(len(self.player_list)-1)
                else:
                    oddman = None

                # split in halves
                split = numpy.array_split(self.player_list, 2)
                
                # storage
                self.team1 = list(split[0])
                self.team2 = list(split[1])

                # if oddman is not None
                # put back the oddman out into a team
                if oddman != None:
                    i = randint(0, 1)
                    if i == 0:
                        self.team1.append(oddman)
                        self.player_list.append(oddman)
                    else:
                        self.team2.append(oddman)
                        self.player_list.append(oddman)

                # get roles: "Team 1", "Team 2", and "in queue..."
                role1 = get(ctx.guild.roles, name='Team 1')
                role2 = get(ctx.guild.roles, name='Team 2')
                roleq = get(ctx.guild.roles, name='in queue...')

                # uneven player_list will be handled by split
                # half into team 1
                for member in self.team1:
                    await member.add_roles(role1)
                    await member.remove_roles(roleq)

                # other half into team 2
                for member in self.team2:
                    await member.add_roles(role2)
                    await member.remove_roles(roleq)

                await ctx.message.delete()
                await ctx.send('__**Team 1**__\n```\n' + '\n'.join(list(map(lambda x:x.name, self.team1))) + ' ```\n__**Team 2**__\n```\n' + '\n'.join(list(map(lambda x:x.name, self.team2))) + '\n```', delete_after=120)
      
            else:
                await ctx.message.delete()
                await ctx.send('You can\'t matchmake with only 1 player!')

    # .add will force a user to join the player_list
    @commands.command(name = 'add')
    @commands.has_role('PUG Leader')
    async def add_player(self, ctx, arg):
        input = ''.join(arg)
        
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

        # if the user was found in this discord
        if input in list(map(lambda x: x.name, ctx.guild.members)) or input in list(map(lambda x: x.id, ctx.guild.members)):
            # if input is an int use get_member as it passes only int
            if isinstance(input, int):
                member = ctx.guild.get_member(input)
            # else use get_member_named as it passes only str
            else:
                member = ctx.guild.get_member_named(input)

            # if the user was not in queue or in either team
            if member not in self.player_list or member not in self.team1 or member not in self.team2:
                await member.add_roles(role)
                self.player_list.append(member)

                await ctx.message.delete()
                await ctx.send(member.mention + ' you\'ve been added to the queue')

            else:
                await ctx.message.delete()
                await ctx.send(member.display_name + ' is already in queue', delete_after=10)

        else:
            await ctx.message.delete()
            await ctx.send(str(input) + ' was not found in this discord or is an invalid format (i.e. capitalization)', delete_after=10)

    # .ring will force a user to team1 or team2
    @commands.command(name = 'ring')
    @commands.has_role('PUG Leader')
    async def ring_player(self, ctx, arg1, arg2):
        input = ''.join(arg1)
        
        ## transforming input to fit our needs
        # @user -> <@!###digits###> -> ###digits###
        input = input.replace('<@!', '')
        input = input.replace('>', '')

        # -> int ###digits###
        if input.isdigit() == True:
            input = int(input)
        # username#discriminator -> Username
        # or just username -> Username
        else:
            input = input.split('#', 1)[0]
            input = input.capitalize()

        # team input
        input2 = ''.join(arg2)

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

            # if user is not on any team
            if member not in self.team1 or self.team2:
                # put player into team 1
                if input2 == 'team1' or input2 == '1' or input2 == 'one':
                    await member.add_roles(role1)
                    await member.remove_roles(roleq)
                    self.player_list.append(member)
                    self.team1.append(member)
                    await ctx.message.delete()
                    await ctx.send(member.mention + ' you\'ve been added to team 1')

                # put player into team 2
                elif input2 == 'team2' or input2 == '2' or input2 == 'two':
                    await member.add_roles(role2)
                    await member.remove_roles(roleq)
                    self.player_list.append(member)
                    self.team2.append(member)
                    await ctx.message.delete()
                    await ctx.send(member.mention + ' you\'ve been added to team 2')
                
                else:
                    await ctx.message.delete()
                    await ctx.send(str(input2) + ' is not a valid input')
                    await ctx.send('``` \nteam1 or 1 or one\nteam2 or 2 or two\n ```', delete_after=5)

            else:
                await ctx.message.delete()
                await ctx.send(member.display_name + ' is already in a team', delete_after=10)

        else:
            await ctx.message.delete()
            await ctx.send(str(input) + ' was not found in this discord or is an invalid format (i.e. capitalization)', delete_after=10)        

    # .remove will remove user from player_list and team1 or team2
    # will also remove roles when applicable
    @commands.command(name = 'remove')
    @commands.has_role('PUG Leader')
    async def remove_player(self, ctx, arg):
        input = ''.join(arg)

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
                await member.remove_roles(roleq, role1, role2)

                self.player_list.remove(member)
                self.team1.remove(member)
                self.team2.remove(member)

                await ctx.send(member.mention + ' you\'ve been removed', delete_after=5)

            else:
                await ctx.send(str(input) + ' was not found in queue, team 1, or team 2 list', delete_after=10)

        else:
            await ctx.send(str(input) + ' was not found in this discord or is an invalid format (i.e. capitalization)', delete_after=10)

    # .shuffle will reform teams
    @commands.command(name = 'shuffle')
    @commands.has_role('PUG Leader')
    async def shuffle_teams(self, ctx):
        # 2 shuffles
        shuffle(self.player_list)
        shuffle(self.player_list)

        # uneven handling
        if (len(self.player_list) % 2) != 0:
            oddman = self.player_list.pop(len(self.player_list)-1)
        else:
            oddman = None

        # split in halves
        split = numpy.array_split(self.player_list, 2)
        
        # storage
        self.team1 = list(split[0])
        self.team2 = list(split[1])

        # if oddman is not None
        # put back the oddman out into a team
        if oddman != None:
            i = randint(0, 1)
            if i == 0:
                self.team1.append(oddman)
                self.player_list.append(oddman)
            else:
                self.team2.append(oddman)
                self.player_list.append(oddman)

        # get roles: "Team 1", "Team 2", and "in queue..."
        role1 = get(ctx.guild.roles, name='Team 1')
        role2 = get(ctx.guild.roles, name='Team 2')
        roleq = get(ctx.guild.roles, name='in queue...')

        # uneven player_list will be handled by split
        # half into team 1
        for member in self.team1:
            await member.add_roles(role1)
            await member.remove_roles(role2)

        # other half into team 2
        for member in self.team2:
            await member.add_roles(role2)
            await member.remove_roles(role1)

        await ctx.message.delete()
        await ctx.send('__**Team 1**__\n```\n' + '\n'.join(list(map(lambda x:x.name, self.team1))) + ' ```\n__**Team 2**__\n```\n' + '\n'.join(list(map(lambda x:x.name, self.team2))) + '\n```', delete_after=60)

    # .queue will display the player_list
    @commands.command(name = 'queue')
    async def display_queue(self, ctx):
        # if player list is empty
        if not self.player_list:
            await ctx.message.delete()
            await ctx.send('The queue is empty', delete_after=5)

        else:
            await ctx.message.delete()
            await ctx.send('\n'.join(list(map(lambda x:x.name, self.player_list))) + '\nTotal Players: ' + str(len(self.player_list)), delete_after=10)

    # .team will print team1 list
    @commands.command(name = 'team1')
    async def check_team1(self, ctx):
        if not self.team1:
            await ctx.message.delete()
            await ctx.send('__**Team** 1__\n> **Empty**', delete_after=10)
        else:
            await ctx.message.delete()
            await ctx.send('__**Team 1**__\n```\n' + '\n'.join(list(map(lambda x:x.name, self.team1))) + '\n```', delete_after=30)

    # .team2 will print team2 list
    @commands.command(name = 'team2')
    async def print_team2(self, ctx):
        if not self.team2:
            await ctx.message.delete()
            await ctx.send('__**Team 2**__\n> **Empty**', delete_after=10)
        else:
            await ctx.message.delete()
            await ctx.send('__**Team 2**__\n```\n' + '\n'.join(list(map(lambda x:x.name, self.team2))) + '\n```', delete_after=30)

    # .clearall will empty both teams and the player list
    @commands.command(name = 'clearall')
    @commands.has_role('PUG Leader')
    async def clear_all(self, ctx):
        role1 = get(ctx.guild.roles, name='Team 1')
        role2 = get(ctx.guild.roles, name='Team 2')
        roleq = get(ctx.guild.roles, name='in queue...')

        for member in self.player_list:
            await member.remove_roles(role1, role2, roleq)

        self.player_list.clear()
        self.team1.clear()
        self.team2.clear()

        await ctx.message.delete()
        await ctx.send('All cleared', delete_after=3)

    # .clearteams will empty both teams but not the player list
    @commands.command(name = 'clearteams')
    @commands.has_role('PUG Leader')
    async def clear_teams(self, ctx):
        # get roles: "Team 1", "Team 2", and "in queue..."
        role1 = get(ctx.guild.roles, name='Team 1')
        role2 = get(ctx.guild.roles, name='Team 2')
        roleq = get(ctx.guild.roles, name='in queue...')

        for member in self.player_list:    
            await member.remove_roles(role1, role2, roleq)

        self.team1.clear()
        self.team2.clear()

        await ctx.message.delete()
        await ctx.send('Teams cleared', delete_after=3)

    # .clearqueue will empty the player list
    @commands.command(name = 'clearqueue')
    @commands.has_role('PUG Leader')
    async def clear_player_list(self, ctx):
        roleq = get(ctx.guild.roles, name='in queue...')

        for member in self.player_list:
            await member.remove_roles(roleq)

        self.player_list.clear()

        await ctx.message.delete()
        await ctx.send('Queue cleared', delete_after=3)
    
    # .cleanup will clear roles from EVERYONE in the discord
    # mostly used when I messed up :P
    @commands.command(name = 'cleanup')
    @commands.has_role('PUG Leader')
    async def clean_up(self, ctx):
        role1 = get(ctx.guild.roles, name='Team 1')
        role2 = get(ctx.guild.roles, name='Team 2')
        roleq = get(ctx.guild.roles, name='in queue...')

        await ctx.message.delete()
        ctx.send('This process can take a while\nCleaning...', delete_after=10)

        for member in ctx.guild.members:
            await member.remove_roles(role1, role2, roleq)

        ctx.send('Cleaning completed', delete_after=10)

    # .vc will force users that are in voice channels already into the respective voice channels
    @commands.command(name = 'vc')
    @commands.has_role('PUG Leader')
    async def force_vc(self, ctx):
        channel1 = get(ctx.guild.voice_channels, name='Team 1')
        channel2 = get(ctx.guild.voice_channels, name='Team 2')

        for member in self.team1:
            await member.move_to(channel1)

        for member in self.team2:
            await member.move_to(channel2)
        
        await ctx.message.delete()
        await ctx.send('Forcing voice channels', delete_after=5)
    
    # .check is mostly for debugging
    @commands.command(name = 'check')
    @commands.has_role('PUG Leader')
    async def debuggin(self, ctx):
        print('\n\n')
        print('player_list = '+str(self.player_list)+'\n')
        print('team1 = '+str(self.team1)+'\n')
        print('team2 = '+str(self.team2)+'\n')
        print('\n')
        await ctx.message.delete()
        await ctx.send('Checking')

    # all the error handling for commands that require a role
    @matchmake.error
    async def matchmake_error(self, ctx, error):
        await ctx.message.delete()
        await ctx.send('Denied: missing **[PUG Leader]** role', delete_after=7)

    @add_player.error
    async def add_player_error(self, ctx, error):
        await ctx.message.delete()
        await ctx.send('Denied: missing **[PUG Leader]** role', delete_after=7)

    @ring_player.error
    async def ring_player_error(self, ctx, error):
        await ctx.message.delete()
        await ctx.send('Denied: missing **[PUG Leader]** role', delete_after=7)
    
    @remove_player.error
    async def remove_player_error(self, ctx, error):
        await ctx.message.delete()
        await ctx.send('Denied: missing **[PUG Leader]** role', delete_after=7)

    @shuffle_teams.error
    async def shuffle_teams_error(self, ctx, error):
        await ctx.message.delete()
        await ctx.send('Denied: missing **[PUG Leader]** role', delete_after=7)

    @clear_all.error
    async def clear_all_error(self, ctx, error):
        await ctx.message.delete()
        await ctx.send('Denied: missing **[PUG Leader]** role', delete_after=7)

    @clear_teams.error
    async def clear_teams_error(self, ctx, error):
        await ctx.message.delete()
        await ctx.send('Denied: missing **[PUG Leader]** role', delete_after=7)

    @clear_player_list.error
    async def clear_player_list_error(self, ctx, error):
        await ctx.message.delete()
        await ctx.send('Denied: missing **[PUG Leader]** role', delete_after=7)

    @clean_up.error
    async def clean_up_error(self, ctx, error):
        await ctx.message.delete()
        await ctx.send('Denied: missing **[PUG Leader]** role', delete_after=7)

    @force_vc.error
    async def force_vc_error(self, ctx, error):
        await ctx.message.delete()
        await ctx.send('Denied: missing **[PUG Leader]** role', delete_after=7)

    @debuggin.error
    async def debuggin_error(self, ctx, error):
        await ctx.message.delete()
        await ctx.send('Denied: missing **[PUG Leader]** role', delete_after=7)

# on bot start up
# add this cog
# used to reload this cog so the bot doesn't have to go down to update
def setup(client):
    client.add_cog(pug(client))