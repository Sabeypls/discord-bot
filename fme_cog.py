from discord.ext import tasks, commands
from discord.utils import get
from discord.ext.commands.cooldowns import BucketType
from random import randint
import asyncio
import discord
import random

class fme(commands.Cog):
    def __init__(self, client):
        self.client = client

        # count function
        self.rod_count = 0
        self.sabey_count = 0
        self.ban_count = 0
        self.body_count = 0

        # pity counter
        self.revival_counter = 0

        # unban russian
        self.unban_counter = 0
        self.unban_list = []

        # anti russian spam
        self.cache_msg = None
        self.spam_counter = 0
        self.general_spam_counter = 0
        
        # TODO #
        # maybe global counter?
        # or fix the issue of roles not loading on start up
        self.start_counter = 0

        # testing
        self.test_counter = 0

        # start task
        self.clear_morb.start()
        self.auto_resupply.start()
        self.auto_resurrect_fatal.start()
        self.auto_resurrect_jihad.start()
        self.auto_mag.start()
        
        # TODO #
        # maybe global counter?
        # or fix the issue of roles not loading on start up
        self.unban_russian_timer.start()

    # target look up
    async def targeting(self, ctx, user):
        global target
        # Triming down input
        input = ''.join(user)
        print('\nUser Input: ' + input)
        
        # @user input is actually <@!###userID###>
        # after trimming the brackets <@ and >, you get ###userID###
        if '<@' in input and '>' in input:
            input = input.replace('<@', '')
            input = input.replace('>', '')
            print('\nInput after removing <@ and >: ' + input)

        # follow up or target input was all digits
        # if it's digits turn it to integer
        if input.isdigit() == True:
            input = int(input)
            print('\nInput is int? ' + str(isinstance(input, int)))

        elif '#' in input: # input was not digits and had a discriminator, split, input = split[0].lower() and discrimintator = split[1]
            input = input.split('#', 1)
            discriminator = input[1]
            print('\nDiscriminator: ' + discriminator)
            input = input[0].lower()
            print('\nInput after removing discriminator: ' + input)
        
        else: # input was not digits and had no discriminator, input.lower() and set discriminator to None
            input = input.lower()
            print('\nInput with no discriminator: ' + input)
            discriminator = None

        # intial member look up
        if input in list(map(lambda x: x.name.lower(), ctx.guild.members)) or input in list(map(lambda x: x.id, ctx.guild.members)):
            # if input is an int use get_member as it passes only int
            if isinstance(input, int):
                target = ctx.guild.get_member(input)
                
            # else use get_member_named as it passes only str
            else:
                member_list = ctx.guild.members
                if discriminator == None:
                    for member in member_list:
                        if member.name.lower() == input:
                            target = member      
                else:
                    for member in member_list:
                        if member.name.lower() == input and member.discriminator == discriminator:
                            target = member
            
        else: # format error
            embed = discord.Embed(title='Error', description='Your input: ' + user + '\nAfter trimming: ' + input + '\n Target was not found in this discord.')
            embed.set_footer(text='IDK. Just @ them.')
            await ctx.send(embed=embed)

    # anti russian spam
    async def anti_russian_spam(self, ctx):
        # get role
        roleRB = get(ctx.guild.roles, name='Russian is Banned')

        # if message was from russian
        if ctx.message.author.id == 175429175325229056:
            # increase counter
            self.spam_counter += 1

            # if the counter goes over then "ban" russian
            if self.spam_counter > 2:
                await ctx.message.author.add_roles(roleRB)
                self.ban_count += 1
    
    def get_roles(self, ctx):
        global roleD, roleB, roleF, roleJ, roleA, role1M, role2M, role3M, roleRB, roleMB
        roleD = get(ctx.guild.roles, name='Do Not Disturb')
        roleB = get(ctx.guild.roles, name='Bot')
        roleJ = get(ctx.guild.roles, name='Death by Jihad')
        roleF = get(ctx.guild.roles, name='Fatality Shot')
        role1M = get(ctx.guild.roles, name='1 Mag')
        role2M = get(ctx.guild.roles, name='2 Mags')
        role3M = get(ctx.guild.roles, name='3 Mags')
        roleA = get(ctx.guild.roles, name='Out of Ammo')
        roleRB = get(ctx.guild.roles, name='Russian is Banned')
        roleMB = get(ctx.guild.roles, name='Morbin')
    
    # restarting upkeep
    def cog_unload(self):
        self.clear_morb.cancel()
        self.auto_resupply.cancel()
        self.auto_resurrect_fatal.cancel()
        self.auto_resurrect_jihad.cancel()
        self.unban_russian_timer.cancel()
        self.auto_mag.cancel()
        
    @commands.command(name='unban')
    async def unban_russian(self, ctx):
        # get role
        role = get(ctx.guild.roles, name='Russian is Banned')

        if role.members: # if russian is banned
            if ctx.author not in self.unban_list: # user's first time voting to unban
                # add user to unban list to check for repeat and uptick by 1
                self.unban_list.append(ctx.author)
                self.unban_counter += 1

                if self.unban_counter >= 3: # successful vote
                    # new embed for successful vote
                    embed = discord.Embed(title='Gratz Russian', description='You\'re unbanned for now...')
                    embed.set_footer(text='You\'ll be back soon...')

                    for member in role.members: # target russian
                        await member.remove_roles(role)

                    self.unban_list.clear() # clear list

                else: # user wants to unban x/3
                    # new embed for unban x/3
                    embed = discord.Embed(title=str(self.unban_counter) + '/3 unban vote', description=ctx.author.mention + ' wants to unban <@175429175325229056>')
                    
                    # display who wanted to unban russian
                    for member in self.unban_list:
                        embed.add_field(title=member.display_name, description='voted to unban <@175429175325229056>', inline=True)
                
                # send message
                await ctx.send(embed=embed)

            else: # repeat unban attempt
                await ctx.send('You already voted to unban russian. (' + str(self.unban_counter) + '/3)')

        else: # not even banned
            await ctx.send('Not even banned bruv.')

    @commands.command(name='jihad')
    async def allah(self, ctx):
        # anti russian spam
        await self.anti_russian_spam(ctx)

        # get role
        self.get_roles(ctx)

        # user not in dnd, jihad cd, or fatality shot
        if ctx.author not in roleD.members and ctx.author not in roleJ.members and ctx.author not in roleF.members:
            # trim the members
            members = set(ctx.guild.members).difference(roleD.members)
            members = set(members).difference(roleB.members)
            members.remove(ctx.author)

            # make a list mapping only id
            members = list(map(lambda x:x.id, members))

            # randomly select
            damage_report = random.sample(members, randint(3, round(len(members)/(randint(1, 3)))))
            
            if randint(0,4) <= 3: # jihad
                # message
                embed = discord.Embed(title=ctx.author.display_name + ' blew up!', description=', '.join(f'<@{x}>' for x in damage_report[:-1]) + ', and <@' + str(damage_report[-1]) + '> were caught in the explosion.', color=0x7d3a00)
                embed.set_author(name='Allah Ackbar!')
                embed.set_thumbnail(url='https://i.imgur.com/mvPPjQI.jpeg')
                embed.add_field(name='Total Deaths', value=str(len(damage_report)+1))
                embed.set_footer(text='Mahvel\'s Jihad Forever')
                await ctx.send(embed=embed)

                #revival chance
                if randint(0,99) <= self.revival_counter:
                    embed = discord.Embed(title='It\'s a jihad miracle!', description=ctx.author.mention + ' survived his own jihad!')
                    embed.set_field(name='Chance', value=str(self.revival_counter+1) + '%')
                    embed.set_footer(text='POGGERS')
                    await ctx.send(embed=embed)
                    self.revival_counter = 0
                    self.body_count += (len(damage_report))

                else: # increase pity
                    await ctx.message.author.add_roles(roleJ)
                    self.revival_counter += randint(1,2)
                    self.body_count += (len(damage_report)+1)

            else: # plant option
                if randint(0,9) <= 1: # dud bomb
                    embed = discord.Embed(title='The bomb was a dud.', description='You were set up!')
                    embed.set_author(name='Nani?')
                    await ctx.send(embed=embed)
                    await ctx.message.author.add_roles(roleJ)

                else: # defuse path
                    timer = randint(15,30)

                    embed = discord.Embed(title='Someone defuse!', description=str(timer) + ' seconds!')
                    embed.set_author(name=ctx.author.display_name + ' has planted the bomb!')
                    embed.set_thumbnail(url='https://imgur.com/VfIcCA2')
                    pmsg = await ctx.send(embed=embed)

                    try:
                        await self.client.wait_for('message', timeout = timer, check=lambda message: message.author.id != ctx.author.id and 'defuse' in message.content.lower())

                    except asyncio.TimeoutError: # blew up
                        await pmsg.delete()
                        embed = discord.Embed(title='Terrorist Wins!', description=ctx.author.mention + '\'s bomb blew up ' + ', '.join(f'<@{x}>' for x in damage_report[:-1]) + ', and <@' + str(damage_report[-1]) + '>.', color=0x7d3a00)
                        embed.set_author(name='The bomb explodes!')
                        embed.set_thumbnail(url='https://imgur.com/McDgePG')
                        embed.add_field(name='Total Deaths', value=str(len(damage_report)))
                        embed.set_footer(text='RIP in peace.')
                        await ctx.send(embed=embed)

                    else: # defused
                        embed = discord.Embed(title='Counter-Terrorist Wins!', description=ctx.author.mention + '\s bomb was defused.')
                        embed.set_author(name='Bomb defused!')
                        embed.set_thumbnail(url='https://static.wikia.nocookie.net/cswikia/images/d/db/Csgo_defusing_new.png/revision/latest?cb=20150916094138')
                        await ctx.send(embed=embed)

                    await ctx.message.author.add_roles(roleJ)

        elif ctx.author in roleF.members or ctx.author in roleJ.members:
            embed = discord.Embed(title='You are already dead.')
            embed.set_image(url='https://c.tenor.com/XQr89d12uVgAAAAC/omaewamoushinderu.gif')
            if ctx.author in roleJ.members:
                embed.add_field(name='Cooldown', value=ctx.author.display_name + ' is on Jihad Cooldown')
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(title='Error', description='You are unable to do that.')
            await ctx.send(embed=embed)

    @commands.command(name='shoot')
    async def whim(self, ctx, arg):
        # anti russian spam
        await self.anti_russian_spam(ctx)

        # get role
        self.get_roles(ctx)
        
        # user was not DnD, fatality shot, or out of ammo
        if ctx.author not in roleD.members and ctx.author not in roleF.members and ctx.author not in roleA.members:
            # call function
            await self.targeting(ctx, arg)

            # targeting self
            if target == ctx.author:
                embed = discord.Embed(title='Stop it!', description='Get some help!\n' + ctx.author.mention + ' don\'t target yourself!')
            
            # targeting bot or dnd
            elif target in roleD.members or target in roleB.members:
                embed = discord.Embed(title='Error', description='You cannot target them.')

            else: # valid target
                # versus stats
                # weighted accuracy
                apercent = randint(0, 1)
                if apercent == 0:
                    accuracy = randint(60, 100)
                elif apercent == 1:
                    accuracy = randint(40, 90)

                # weighted evasion
                epercent = randint(0, 3)
                if epercent == 0:
                    evasion = randint(70, 100)
                elif epercent == 1:
                    evasion = randint(60, 90)
                elif epercent == 2:
                    evasion = randint(40, 80)
                else:
                    evasion = randint(0, 70)

                if (accuracy - evasion) >= 51: # head shot
                    embed = discord.Embed(description=target.mention + ' was shot by ' + ctx.author.mention, color=0x00c210)
                    embed.set_author(name='IN THE FACE!')
                    embed.set_thumbnail(url='https://static.wikia.nocookie.net/cswikia/images/d/d5/Icon_headshot.png/revision/latest?cb=20220117122653')
                    embed.add_field(name='Accuracy', value=str(accuracy) + '%', inline=True)
                    embed.add_field(name='Evasion', value=str(evasion) + '%', inline=True)
                    embed.set_footer(text='They ain\'t gonna be in next Rush Hour')
                    await target.add_roles(roleF)
                    self.body_count += 1

                # hit, non fatal
                elif (accuracy - evasion) >= 1 and (accuracy - evasion) <= 50:
                    embed = discord.Embed(description=target.mention + ' was shot by ' + ctx.author.mention, color=0x00c210)
                    embed.set_thumbnail(url='https://static.wikia.nocookie.net/cswikia/images/3/3d/Domination.png/revision/latest?cb=20220117123613')
                    embed.add_field(name='Accuracy', value=str(accuracy) + '%', inline=True)
                    embed.add_field(name='Evasion', value=str(evasion) + '%', inline=True)
                    embed.set_footer(text='EMOTIONAL DAMAGE!')

                else: # missed
                    embed = discord.Embed(description=ctx.author.mention + ' missed.', color=0xc42400)
                    embed.set_thumbnail(url='https://static.wikia.nocookie.net/cswikia/images/7/72/Smoke_kill_unused.png/revision/latest?cb=20220626160103')
                    embed.add_field(name='Accuracy', value=str(accuracy) + '%', inline=True)
                    embed.add_field(name='Evasion', value=str(evasion) + '%', inline=True)
                    embed.set_footer(text='L + ratio + you fell off')

                # empty?
                if randint(0,19) <= 6:
                    await ctx.message.author.add_roles(roleA)
                    embed.add_field(name='Emptied', value=ctx.author.mention + ' is out of ammo.')

            # send message
            await ctx.send(embed=embed)

        else: # error dnd
            embed = discord.Embed(title='Error', description='You are **[Do Not Disturb]**')
            await ctx.send(embed=embed)

    @commands.command(name='burst')
    async def whim_burst(self, ctx, arg):
        # anti russian spam
        await self.anti_russian_spam(ctx)

        # get role
        self.get_roles(ctx)
        
        # user was not DnD, fatality shot, or out of ammo
        if ctx.author not in roleD.members and ctx.author not in roleF.members and ctx.author not in roleA.members:
            # call function
            await self.targeting(ctx, arg)

            # targeting self
            if target == ctx.author:
                embed = discord.Embed(title='Stop it!', description='Get some help!\n' + ctx.author.mention + ' don\'t target yourself!')
            
            # targeting bot or dnd
            elif target in roleD.members or target in roleB.members:
                embed = discord.Embed(title='Error', description='You cannot target them.')
            
            else: # valid target
                i = 1
                health = 100
                embed = discord.Embed(title='Burst Fire Mode', description=target.mention + ' was shot by ' + ctx.author.mention, color=0x00c210)

                # 3 burst while user still has ammo
                while(i <= 3 and ctx.author not in roleA.members):
                    # versus stats
                    accuracy = randint(50, 100)

                    # weight evasion
                    epercent = randint(0, 2)
                    if epercent == 0:
                        evasion = randint(80, 100)
                    elif epercent == 1:
                        evasion = randint(60, 80)
                    else:
                        evasion = randint(1, 80)

                    if (accuracy - evasion) >= 71: # head shot
                        embed.add_field(name='Shot ' + str(i), value='Head', inline=True)
                        health -= 55
                    
                    # upper torso
                    elif (accuracy - evasion) >= 51 and (accuracy - evasion) <= 70:
                        embed.add_field(name='Shot ' + str(i), value='Upper Torso', inline=True)
                        health -= 35

                    # lower torso
                    elif (accuracy - evasion) >= 31 and (accuracy - evasion) <= 50:
                        embed.add_field(name='Shot ' + str(i), value='Lower Torso')
                        health -= 25

                    # limb
                    elif (accuracy - evasion) >= 1 and (accuracy - evasion) <= 30:
                        limbs = ['Leg', 'Hand', 'Feet', 'Feet', 'Hand', 'Leg', 'Dick']
                        x = randint(0,6)
                        embed.add_field(name='Shot ' + str(i), value=limbs[x])
                        health -= 10

                    else: # missed
                        embed.add_field(name='Shot ' + str(i), value='Missed', inline=True)

                    # empty?
                    if randint(0,9) <= 2:
                        await ctx.message.author.add_roles(roleA)
                        embed.add_field(name='Emptied', value=str(i) + '/3 were fired', inline=False)
                    
                    i += 1

                # health check
                if health <= 0: # kill
                    await target.add_roles(roleF)
                    embed.set_footer(text=target.display_name + ' was shot dead.')
                
                else: # fail
                    embed.set_footer(text=target.display_name + ' lived with ' + str(health) + '/100 Health')

            # send message
            await ctx.send(embed=embed)
                                    
        else: # error dnd
            embed = discord.Embed(title='Error', description='You are **[Do Not Disturb]**')
            await ctx.send(embed=embed)

    @commands.command(name='deag')
    async def whim_1tap(self, ctx, arg):
        # anti russian spam
        await self.anti_russian_spam(ctx)

        # get role
        self.get_roles(ctx)
        
        # user was not DnD, fatality shot, or out of ammo
        if ctx.author not in roleD.members and ctx.author not in roleF.members and ctx.author not in roleA.members:
            # call function
            await self.targeting(ctx, arg)

            # targeting self
            if target == ctx.author:
                embed = discord.Embed(title='Stop it!', description='Get some help!\n' + ctx.author.mention + ' don\'t target yourself!')
            
            # targeting bot or dnd
            elif target in roleD.members or target in roleB.members:
                embed = discord.Embed(title='Error', description='You cannot target them.')
            
            else: # valid target
                # versus stats
                accuracy = randint(1,100)
                evasion = randint(80,100)

                if (accuracy-evasion) >= 1: # hit
                    # set embed for hitting
                    embed = discord.Embed(title='HEADSHOT! ONE TAPPED!', description=target.mention + ' was one tapped by ' + ctx.author.mention + '\n#FaZeUp #GreenWall #EnvyUs #100T #420 #360 #noscope #MLG #OhBaby #TSMWONNERED #Juan #OneTep #TheyTalkAboutMyOneTaps #Screamy #Shroud #Niko #Asuna #TenZ #1g #Stake #Ad #Juicer #Youtube #Twitch', url='https://www.youtube.com/watch?v=212tu-dre6o')
                    embed.set_image(url='https://thumbs.gfycat.com/EnergeticCostlyAfricanpiedkingfisher-size_restricted.gif')
                    embed.add_field(name='Accuracy', value=str(accuracy) + '%', inline=True)
                    embed.add_field(name='Evasion', value=str(evasion) + '%', inline=True)
                    embed.set_footer(text='GET FUCKED NERD')
                    await target.add_roles(roleF)

                else: # missed
                    # set embed for missed
                    embed = discord.Embed(title='One in the Chamber', description=target.mention + ' was shot by ' + ctx.author.mention, color=0x00c210)
                    embed.add_field(name='You missed', value=ctx.author.mention + ' tried to flex.\n "Watch this," they said. Their deagle shot rang true but it missed ' + target.mention\
                        + '\'s head.\nRIP BOZO. Maybe next time.', inline=False)
                    embed.add_field(name='Accuracy', value=str(accuracy) + '%', inline=True)
                    embed.add_field(name='Evasion', value=str(evasion) + '%', inline=True)
                    embed.set_thumbnail(url='https://static.wikia.nocookie.net/cswikia/images/7/72/Smoke_kill_unused.png/revision/latest?cb=20220626160103')
                    embed.set_footer(text=ctx.author.display_name + ' has NA aim')

                # send message    
                await ctx.send(embed=embed)

                # role update
                await ctx.author.add_roles(roleA)

        else: # error dnd
            embed = discord.Embed(title='Error', description='You are **[Do Not Disturb]**')
            await ctx.send(embed=embed)

    @commands.command(name='laser')
    @commands.max_concurrency(1, per=BucketType.default, wait=True)
    async def schwing(self, ctx, arg):
        # anti russian spam
        await self.anti_russian_spam(ctx)

        # get role
        self.get_roles(ctx)

        if ctx.message.author not in roleD.members:
            await self.targeting(ctx, arg)

            if target == ctx.author:
                embed = discord.Embed(title='Look at this human', description=ctx.author.mention + ' tried to laser themselves S M H.')
                embed.set_image(url='https://c.tenor.com/IaSQ2CvyEAoAAAAC/pepepoint-pepe.gif')
                await ctx.reply(embed=embed, mention_author=False)

            elif target in roleD.members or target in roleB.members:
                embed = discord.Embed(title='Error', description='You cannot target them.')
                await ctx.message.delete()
                await ctx.send(embed=embed)

            else:
                i = 0 # laser variables and list used through out
                l_title = ['Slow!', 'AUUUUGGGGHHH!!!', 'KEKW', 'OMEGALUL', 'LUL U DIED', 'RIP BOZO', '-99999 Damage', 'RIP', 'Nice Try!']
                l_index = randint(0, len(l_title)-1)
                materia = ['Ice Materia.', 'Fire Materia.', 'Ultima.', 'Heal Materia.', 'Earth Materia.', 'Electro Materia.', 'Gravity Materia.',\
                    'Bio Materia.', 'Barrier.', 'Aqua Materia.']
                mat_index = randint(0, len(materia)-1)
                w_title = ['Fast!', 'WOW!', 'Nice Job!', 'Great Job!', 'Gaming!', 'Variety Gamer!', 'The Chosen One!', 'OMG SOLO', 'SUCCESS']
                w_index = randint(0, len(w_title)-1)
                clan = ['CSO|', '', 'GES|', '', 'IES|', '','CHAMPION|', 'ESK|', '', 'GOD GAYMER|']
                clan_index = randint(0, len(clan)-1)

                # embed start
                embed = discord.Embed(title='Laser! Schwing!', description=ctx.author.mention + ' sent a laser to ' + target.mention\
                    + '\n|------------------------------------------|')
                embed.set_image(url='https://c.tenor.com/4PRb7JeHCR8AAAAC/sephiroth-slash.gif')
            
                # random choice of laser
                laser = randint(0,2)
                
                # setting timer based on user status
                if str(target.status) == 'offline':
                    timer = 12
                elif str(target.status) == 'away' or str(target.status) == 'busy':
                    timer = 9
                else:
                    timer = 7

                if laser == 0: # high laser / crouch laser
                    # list
                    name_list = ['CROUCH', 'HOLY SHIT A LASER', 'THIS IS WHAT YOU NEED TO DO']
                    value_list = ['CROUCH\nCROUCH\nCROUCH\nCROUCH\nCROUCH\nCROUCH\n',\
                        'JUMP! JUMP! JUMP!\nJUMP! JUMP! JUMP!\nJUMP! JUMP! JUMP!\nJUMP! JUMP! JUMP!\nJUMP! JUMP! JUMP!\nJUMP! JUMP! JUMP!\n',\
                        'CROUCH JUMP! CROUCH JUMP!\nCROUCH JUMP! CROUCH JUMP!\nCROUCH JUMP! CROUCH JUMP!\nCROUCH JUMP! CROUCH JUMP!\nCROUCH JUMP! CROUCH JUMP!\nCROUCH JUMP! CROUCH JUMP!\n']

                    while i <= 2: # loop adding field to embed
                        x = randint(0, len(name_list)-1)
                        embed.add_field(name=name_list[x], value=value_list[x], inline=True)
                        name_list.pop(x)
                        value_list.pop(x)
                        i += 1

                    # send and store message
                    message = await ctx.send(embed=embed)

                    try: # wait for user message with 'crouch' exactly in letter counter length
                        await self.client.wait_for('message', timeout = timer, check=lambda message: message.author.id == target.id and 'crouch' in message.content.lower() and len(message.content) == 6)
                    
                    except asyncio.TimeoutError: # time out
                        # new embed for time out / losing
                        embed = discord.Embed(title=l_title[l_index], description=target.mention + ' was sliced by ' + ctx.author.mention + '\'s laser.', color=0xc42400)
                        embed.add_field(name='__Chat Log__', value='[entWatch]' + target.mention + '(' + str(target.id) + ') has died with ' + materia[mat_index])
                    
                    else: # success
                        # new embed for winning
                        embed = discord.Embed(title=w_title[w_index], description=clan[clan_index] + target.mention + ' ducked a laser!', color=0x00c210)

                    # delete previous bot message and send a new one
                    await message.delete()
                    await ctx.send(embed=embed)

                elif laser == 1: # low laser / jump laser
                    # list
                    name_list = ['JUMP', 'HOLY SHIT A LASER', 'THIS IS WHAT YOU NEED TO DO']
                    value_list = ['JUMP\nJUMP\nJUMP\nJUMP\nJUMP\nJUMP',\
                        'CROUCH! CROUCH!\nCROUCH! CROUCH!\nCROUCH! CROUCH!\nCROUCH! CROUCH!\nCROUCH! CROUCH!\nCROUCH! CROUCH!\n',\
                        'CROUCH JUMP! CROUCH JUMP!\nCROUCH JUMP! CROUCH JUMP!\nCROUCH JUMP! CROUCH JUMP!\nCROUCH JUMP! CROUCH JUMP!\nCROUCH JUMP! CROUCH JUMP!\nCROUCH JUMP! CROUCH JUMP!\n']

                    while i <= 2: # loop adding field to embed
                        x = randint(0, len(name_list)-1)
                        embed.add_field(name=name_list[x], value=value_list[x], inline=True)
                        name_list.pop(x)
                        value_list.pop(x)
                        i += 1

                    # send and store message
                    message = await ctx.send(embed=embed)

                    try: # wait for user message with 'jump' exactly in letter counter length
                        await self.client.wait_for('message', timeout = timer, check=lambda message: message.author.id == target.id and 'jump' in message.content.lower() and len(message.content) == 4)
                    
                    except asyncio.TimeoutError: # time out
                        # new embed for time out / losing
                        embed = discord.Embed(title=l_title[l_index], description=target.mention + ' was sliced by ' + ctx.author.mention + '\'s laser.', color=0xc42400)
                        embed.add_field(name='__Chat Log__', value='[entWatch]' + target.mention + '(' + str(target.id) + ') has died with ' + materia[x])

                    else: # success
                        # new embed for winning
                        embed = discord.Embed(title=w_title[w_index], description=clan[clan_index] + target.mention + ' jumped a laser!', color=0x00c210)
                    
                    # delete previous bot message and send a new one
                    await message.delete()
                    await ctx.send(embed=embed)

                elif laser == 2: # mid laser / crouch jump laser
                    # list
                    name_list = ['CROUCH JUMP', 'HOLY SHIT A LASER', 'THIS IS WHAT YOU NEED TO DO']
                    value_list = ['CROUCH JUMP\nCROUCH JUMP\nCROUCH JUMP\nCROUCH JUMP\nCROUCH JUMP\nCROUCH JUMP\n',\
                        'JUMP! JUMP! JUMP!\nJUMP! JUMP! JUMP!\nJUMP! JUMP! JUMP!\nJUMP! JUMP! JUMP!\nJUMP! JUMP! JUMP!\nJUMP! JUMP! JUMP!\n',\
                        'CROUCH! CROUCH! CROUCH!\nCROUCH! CROUCH! CROUCH!\nCROUCH! CROUCH! CROUCH!\nCROUCH! CROUCH! CROUCH!\nCROUCH! CROUCH! CROUCH!\nCROUCH! CROUCH! CROUCH!']

                    while i <= 2: # loop adding field to embed
                        x = randint(0, len(name_list)-1)
                        embed.add_field(name=name_list[x], value=value_list[x], inline=True)
                        name_list.pop(x)
                        value_list.pop(x)
                        i += 1

                    # send and store message
                    message = await ctx.send(embed=embed)
                    
                    try: # wait for user message with 'crouch jump' or 'jump crouch' exactly in letter counter length
                        await self.client.wait_for('message', timeout = timer, check=lambda message: message.author.id == target.id\
                            and ('crouch jump' in message.content.lower() or 'jump crouch' in message.content.lower()) and len(message.content) == 11)

                    except asyncio.TimeoutError: # time out
                        # new embed for time out / losing
                        embed = discord.Embed(title=l_title[l_index], description=target.mention + ' was sliced by ' + ctx.author.mention + '\'s laser.', color=0xc42400)
                        embed.add_field(name='__Chat Log__', value='[entWatch]' + target.mention + '(' + str(target.id) + ') has died with ' + materia[mat_index])

                    else:
                        # new embed for winning
                        embed = discord.Embed(title=w_title[w_index], description=clan[mat_index] + target.mention + ' crouch jumped a laser!', color=0x00c210)

                    # delete previous bot message and send a new one
                    await message.delete()
                    await ctx.send(embed=embed)
                            
        else: # user was dnd
            embed = discord.Embed(title='Error', description=ctx.author.mention + ' is [Do Not Disturb]')
            await ctx.send(embed=embed)

    @commands.command(name='fuckrod')
    async def fuck_rod(self, ctx):
        # anti russian spam
        await self.anti_russian_spam(ctx)

        if ctx.message.author.id == 408532966080512000:
            await ctx.send('go fuck yourself <@408532966080512000>, when\'s Sven')
            self.rod_count += 1

        else:
            await ctx.send(ctx.message.author.mention + ' says fuck <@408532966080512000>')
            self.rod_count += 1

    @commands.command(name='fucksabey')
    async def fuck_sabey(self, ctx):
        # anti russian spam
        await self.anti_russian_spam(ctx)

        if ctx.message.author.id == 90539785097076736:
            await ctx.send('Not like this.')
            self.sabey_count += 1

        else:
            await ctx.send(ctx.message.author.mention + ' says fuck <@90539785097076736>')
            self.sabey_count += 1

    @commands.command(name='banrussian')
    async def ban_russian(self, ctx):
        # anti russian spam
        await self.anti_russian_spam(ctx)

        if ctx.message.author.id == 175429175325229056:
            await ctx.send('shut up, when\'s Terraria')
            self.ban_count += 1

        else:
            await ctx.send('<@175429175325229056> is banned.')
            self.ban_count += 1

    @commands.command(name='morb')
    async def morbin_time(self, ctx):
        # anti russian spam
        await self.anti_russian_spam(ctx)

        # get role
        self.get_roles(ctx)

        # if they weren't morbin they morbin
        if ctx.message.author not in roleMB.members:
            # create embed
            embed = discord.Embed(title='MORBIN\' TIME', description=ctx.author.mention + ' IS MORBIN\'!!!')
            embed.set_image(url='https://c.tenor.com/YqNZ6E2uEbsAAAAd/morbius-morbin-time.gif')

            # message
            await ctx.author.add_roles(roleMB)
            await ctx.send(embed=embed)

        else: # just delete
            await ctx.message.delete()

    @commands.command(name='count')
    async def fuck_rod_counter(self, ctx):
        # anti russian spam
        await self.anti_russian_spam(ctx)

        # create embed
        embed = discord.Embed(title='Number Count', description='Here are the numbers!')
        embed.add_field(title='Fuck Rod', description=str(self.rod_count), inline=True)
        embed.add_field(title='Fuck Sabey', description=str(self.sabey_count), inline=True)
        embed.add_field(title='Russian Ban', description=str(self.ban_count), inline=True)
        embed.add_field(title='Body Count', description=str(self.body_count), inline=False)
        
        # send message
        await ctx.send(embed=embed)

    @commands.command(name='reload')
    async def reloading(self, ctx):
        # get role
        self.get_roles(ctx)

        # user is indeed out of ammo
        if ctx.author in roleA.members:
            if ctx.author in role1M.members: # 1 mag -> 0 mag
                await ctx.author.remove_roles(role1M, roleA)
                embed = discord.Embed(title='Reloaded', description=ctx.author.mention + ' reloaded.')
                embed.set_footer(text='No More')

            elif ctx.author in role2M.members: # 2 mag -> 1 mag
                await ctx.author.remove_roles(role2M, roleA)
                await ctx.author.add_roles(role1M)
                embed = discord.Embed(title='Reloaded', description=ctx.author.mention + ' reloaded.')
                embed.set_footer(text='Last Mag!')

            elif ctx.author in role3M.members: # 3 mag -> 2 mag
                await ctx.author.remove_roles(role3M, roleA)
                await ctx.author.add_roles(role2M)
                embed = discord.Embed(title='Reloaded', description=ctx.author.mention + ' reloaded.')
                embed.set_footer(text='2 Left')

            else: # 0 mag gang
                embed = discord.Embed(title='Out', description=ctx.author.mention + ' ran out of mags.')
                embed.set_footer(text='L + ratio + speed owns you')
            
        else: # user didn't need to reload
            embed = discord.Embed(title='Full Mag', description=ctx.author.mention + ' did not need to reload.')
            embed.set_footer(text='Baka!')

        # send message
        await ctx.send(embed=embed)
    
    @commands.command(name='refund')
    @commands.is_owner()
    async def clear_ammo_target(self, ctx, arg):
        # get role
        self.get_roles(ctx)

        # call function
        await self.targeting(ctx, arg)

        # message
        embed = discord.Embed(title='Refunded', description='Hey ' + target.mention + ' that last shot did\'t count.')
        embed.set_footer(text='Good Luck.')
        await target.remove_roles(roleF)
        await ctx.send(embed=embed)

    @commands.command(name='resupply')
    @commands.is_owner()
    async def clear_ammo(self, ctx):
        # get role
        self.get_roles(ctx)
        
        for member in roleF.members:  
            await member.remove_roles(roleF)
        
        embed = discord.Embed(title='American Stimulus', description='Ammo was handed out to everyone!')
        embed.set_footer(text='Good Luck. Don\'t spend it all on a deagle.')
        await ctx.send(embed=embed)
    
    @commands.command(name='stimulus')
    @commands.is_owner()
    async def stimulus_mags(self, ctx):
        # get role
        self.get_roles(ctx)

        members = set(ctx.guild.members).difference(roleD.members)
        members = set(members).difference(roleB.members)

        for member in role2M.members:
            await member.remove_roles(role2M, roleA)
            await member.add_roles(role3M)

        for member in role1M.members:
            await member.remove_roles(role1M, roleA)
            await member.add_roles(role2M)

        for member in members:
            await member.add_roles(role1M)

        embed = discord.Embed(title='American Stimulus', description='Free mag for everyone (including your sister)!')
        embed.set_footer(text='Take care and brush your hair.')
        await ctx.send(embed=embed)

    @commands.command(name='revive')
    @commands.is_owner()
    async def clear_death(self, ctx, arg):
        # get role
        self.get_roles(ctx)

        # call function
        await self.target(ctx, arg)

        # revive message
        embed = discord.Embed(title='A gracious god descends!', description=target.mention + ' you have been revived.')
        embed.set_footer(text='It was me btw... not the bot. Me as in Sabeypls.')
        await target.remove_roles(roleJ, roleF)
        await ctx.send(embed=embed)

    @commands.command(name='resurrect')
    @commands.is_owner()
    async def clear_all_death(self, ctx):
        # get role
        self.get_roles(ctx)
        
        for member in roleJ.members or member in roleF.members:  
            await member.remove_roles(roleJ, roleF)
        
        embed = discord.Embed(title='A gracious god descends!', description='Everyone has been revived!')
        embed.set_footer(text='It was me btw... not the bot. Me as in Sabeypls.')
        await ctx.send(embed=embed)

    @commands.command(name='fme')
    @commands.has_role('BTS')
    async def testing(self, ctx):
        print('\n\nClear')
                    
    @commands.command(name='purge')
    @commands.is_owner()
    async def purge_message(self, ctx, limit=0):
        if isinstance(limit, int):
            await ctx.message.delete()
            await ctx.channel.purge(limit=limit)
        else:
            print('\n\nYou messed up\n\n')

    ########################################################
    ########################################################
    ########################################################
    @commands.Cog.listener()
    async def on_message(self, message):
        server = self.client.get_guild(939798514865668126)
        role = get(server.roles, name='Russian is Banned')

        if '<@233701741198049281>' in message.content:
            await message.channel.send('Don\'t @ Me')

        if 'rod shot gregson' in message.content.lower():
            embed = discord.Embed(title='Rod shot and killed Inspector Tobias Gregson!', description='<@408532966080512000> kills London\'s finest yardsman, Inspector Tobias Gregson, with a gun in the Vigil household!')
            embed.set_thumbnail(url='https://static.wikia.nocookie.net/aceattorney/images/9/95/Tobias_Gregson_mugshot.png/revision/latest?cb=20210818022452')
            embed.set_footer(text='October 31st, 1899')

            await message.channel.send(embed=embed)
        
        if 'rod\'s trial' in message.content.lower():
            embed = discord.Embed(title='Rod to stand trial!', description='<@408532966080512000> will stand trial for the murder of London\'s finest yardsman, Inspect Tobias Gregson! \
                     <@408532966080512000>\'s defendant will be the nipponese fellow, <@255549735786643456>, who has pulled miracles in the court room. Will <@408532966080512000> be found guilty \
                        or not guilty?')
            embed.set_thumbnail(url='https://static.wikia.nocookie.net/aceattorney/images/6/61/Ry%C5%ABnosuke_portrait.png/revision/latest?cb=20210603003336')
            embed.set_footer(text='November 1st, 1899')

            await message.channel.send(embed=embed)
        
        # general russian spam
        if message.author.id == 175429175325229056:
            if self.cache_msg == None:
                self.cache_msg = message

            if self.cache_msg.id != message.id and self.cache_msg.content == message.content:
                self.general_spam_counter += 1

                if self.general_spam_counter > 3:
                    await message.author.add_roles(role)
                    self.ban_count += 1
            
            if self.cache_msg.id != message.id and self.cache_msg.content != message.content:
                self.cache_msg = message

    ########################################################
    ########################################################
    ########################################################
    @tasks.loop(minutes=30.0)
    async def unban_russian_timer(self):
        if self.start_counter == 1:
            server = self.client.get_guild(939798514865668126)
            role = get(server.roles, name='Russian is Banned')
            
            self.spam_counter = 0
            self.unban_counter = 0
            self.unban_list.clear()

            for member in role.members:
                await member.remove_roles(role)
        else:
            self.start_counter = 1

    @tasks.loop(minutes=10.0)
    async def clear_morb(self):
        server = self.client.get_guild(939798514865668126)
        role = get(server.roles, name='Morbin')

        for member in role.members:
            await member.remove_roles(role)

    @tasks.loop(hours=1.0)
    async def auto_resupply(self):
        if self.start_counter == 1:
            server = self.client.get_guild(939798514865668126)
            role = get(server.roles, name='Out of Ammo')

            for member in role.members:
                await member.remove_roles(role)

    @tasks.loop(hours=6.0)
    async def auto_resurrect_jihad(self):
        if self.start_counter == 1:
            server = self.client.get_guild(939798514865668126)
            role = get(server.roles, name='Death by Jihad')

            for member in role.members:
                await member.remove_roles(role)

    @tasks.loop(hours=1.0)
    async def auto_resurrect_fatal(self):
        server = self.client.get_guild(939798514865668126)
        role = get(server.roles, name='Fatality Shot')

        for member in role.members:
            await member.remove_roles(role)

    @tasks.loop(hours=24.0)
    async def auto_mag(self):
        if self.start_counter == 1:
            server = self.client.get_guild(939798514865668126)
            roleD = get(server.roles, name='Do Not Disturb')
            roleB = get(server.roles, name='Bot')
            role1M = get(server.roles, name='1 Mag')
            role2M = get(server.roles, name='2 Mags')
            role3M = get(server.roles, name='3 Mags')

            for member in role2M.members:
                await member.remove_roles(role2M)
                await member.add_roles(role3M)

            for member in role1M.members:
                await member.remove_roles(role1M)
                await member.add_roles(role2M)

            members = set(server.members).difference(roleD.members)
            members = set(members).difference(roleB.members)

            for member in members:
                if member not in role1M.members and member not in role2M.members and member not in role3M.members:
                    await member.add_roles(role1M)
        
# on bot start up
# add this cog
# used to reload this cog so the bot doesn't have to go down to update
def setup(client):
    client.add_cog(fme(client))