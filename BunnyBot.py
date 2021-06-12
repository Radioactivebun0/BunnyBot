import discord
from discord.ext import commands, tasks
from discord import Embed
import time
import json
import asyncio
import youtube_dl
import shutil
import os
from discord.utils import get
from youtube_search import YoutubeSearch
from datetime import datetime
from mcstatus import MinecraftServer
import api
import uwuify
import sys
import threading
import socket

from typing import List

the_list_of_queues = []

global oldM
global botM

global enable_uwu

global ready_message

oldM = ' '
botM = ' '

enable_uwu = False

ready_message = 0

intents = discord.Intents().all()
client = commands.Bot(command_prefix='!Bb ', intents = intents)
client.remove_command('help')
counter = 0

def send_data_to_monitering_server():
    s = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM)
    if len(sys.argv[1:]) == 0:
        host = socket.gethostname()
    else:
        port = sys.argv[1]
    port = 12348
    s.connect((host, port))
    print(s.recv(1024).decode('utf-8'))
    s.send('on -BunnyBot'.encode('utf-8'))
    time.sleep(0.1)
    s.send('stoping'.encode('utf-8'))
    s.close()


@client.event
async def on_ready():
    global ready_message_id
    print('BunnyBot has started :)')
    await client.change_presence(status=discord.Status.online, activity=discord.Game('BunnyBot(Beta)'))
    channel = client.get_channel(828615308217417748)
    embed = discord.Embed(title='BunnyBot is online!', colour=discord.Colour.blue())
    msg = await channel.send(embed=embed)
    ready_message = msg



@client.event
async def on_message(message):
    await client.process_commands(message)
    global counter
    global enable_uwu
    bannedwords = ['fuck', 'fucker', 'fucking', 'cunt', 'shit', 'nigger']
    for x in bannedwords:
        try:
            if x in message.content:
                print('This message contained a banned word')
                print(f'Message: {message.content}')
                print(f'User: {message.author}')
                ## delete the message
                print('deleting...')
                await message.delete()
                return
        except:
            return
    if message.content.startswith('$ai '):
        global oldM
        global botM
        msg = message.content
        msg = msg.split('$ai ')
        msg = msg[1]
        if message.author == client.user:
            botM = msg
            return
        print("Got message: {}".format(msg))
        print('{},{},{}'.format(oldM, botM, msg))
        await message.channel.send(api.get_response([oldM, botM, msg], "joy")[
                                       "response"])  # One of {'neutral', 'anger', 'joy', 'fear', 'sadness'}. An emotion to condition the response on. Optional param, if not specified, 'neutral' is used
        oldM = msg
    if message.author != client.user:
        d = open("levels.json")
        levels_data = json.load(d)
        print(str(message.author) + ' Sent message: ' + str(message.content))
        try:
            new_xp = 0
            xp = (levels_data[str(message.author)]["xp"])
            new_xp = int(xp) + 1
            level = (levels_data[str(message.author)]["level"])
        except:
            new_xp = 0
            level = 0
        levels_data[str(message.author)] = {'xp': str(new_xp), 'level': str(level)}
        with open("levels.json", 'w') as e:
            json.dump(levels_data, e)
        if (levels_data[str(message.author)]["xp"]) == '50':
            print(str(message.author) + ' leveled up!')
            embedVar = discord.Embed(colour=discord.Colour.blue(), title=f"{message.author.name}",
                                     description=f"Leveled Up!\nLevel: {int(level) + 1}", )  # add color=
            await message.channel.send(embed=embedVar)
            a = open('levels.json')
            levels_data = json.load(a)
            new_xp = 0
            level = 0
            new_level = 0
            level = (levels_data[str(message.author)]['level'])
            new_level = int(level) + 1
            levels_data[str(message.author)] = {'xp': str(new_xp), 'level': str(new_level)}
            with open('levels.json', 'w') as k:
                json.dump(levels_data, k)
    if enable_uwu == True:
        if message.author == client.user:
            return
        await message.delete()
        flags = uwuify.SMILEY | uwuify.YU
        # await message.channel.send(f'{message.author}: {uwuify.uwu(message.content)}')
        embed = discord.Embed(colour=message.author.colour, timestamp=message.created_at, title=f"{message.author}",
                              description=(uwuify.uwu(message.content, flags=flags)))
        embed.set_thumbnail(url=message.author.avatar_url)
        await message.channel.send(embed=embed)


@client.command()
async def uwu(ctx):
    global enable_uwu
    if enable_uwu == True:
        enable_uwu = False
        embeded = discord.Embed(colour=discord.Colour.blue(), title='Disabled uwu mode')
        await ctx.send(embed=embeded)
    else:
        enable_uwu = True
        embeded = discord.Embed(colour=discord.Colour.blue(), title='Enabled uwu mode')
        await ctx.send(embed=embeded)


@client.command()
async def off(ctx):
    global ready_message
    embed = discord.Embed(title='BunnyBot offline :(', colour=discord.Colour.blue())
    channel = client.get_channel(828615308217417748)
    await channel.send(embed=embed)
    s = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM)
    host = socket.gethostname()
    port = 12348
    s.connect((host, port))
    print(s.recv(1024).decode('utf-8'))
    s.send('off -BunnyBot'.encode('utf-8'))
    time.sleep(0.1)
    s.send('stoping'.encode('utf-8'))
    s.close()
    sys.exit()


@client.command()
async def members(ctx):
    embedVar = discord.Embed()
    embedVar.add_field(name="Total Members: ", value=len(ctx.guild.members), inline=False)
    await ctx.send(embed=embedVar)


@client.command()
async def suggest(ctx, *, suggestion):
    print(f'{ctx.message.author} suggested: {suggestion}')
    channel = client.get_channel(759861580228984894)
    embedVar = discord.Embed(colour=discord.Colour.blue(), title=f"{ctx.message.author.name} suggests:", description=f"{suggestion}", )  # add color=
    await channel.send(embed=embedVar)


@client.command()
async def report_bug(ctx, *, bug):
    print(f'{ctx.message.author} reported the bug: {bug}')
    channel = client.get_channel(759860033936293898)
    embedVar = discord.Embed(colour=discord.Colour.blue(), title=f"{ctx.message.author.name} reported the bug:", description=f"{bug}", )  # add color=
    await channel.send(embed=embedVar)


@client.command()
async def yeet(ctx):
    await ctx.send('(╯°□°）╯︵ ┻━┻')


@client.command()
async def test(ctx, args):
    await ctx.send(args)


@client.command()
async def bun(ctx, size = 64):
    await ctx.send(f'https://cdn.discordapp.com/avatars/831282065915117588/99caa58f5102d35f95c0ed3ba9836362.png?size={size}')


@client.command()
async def name(ctx):
    embedVar = discord.Embed(colour=discord.Colour.blue(), title='This is the guild name: ' + str(ctx.guild.name))  # add color=
    await ctx.send(embed=embedVar)
    #message = await ctx.send('This is the guild name: ' + str(ctx.guild.name))
    message_id = message.id
    print(message_id)


@client.command()
async def help(ctx):
    embedVar = discord.Embed(colour=discord.Colour.blue(), title="Help:",
                             description="!Bb members: Shows the current amount of members in the server\n\n!Bb level: Shows you your current level.\n\n!Bb join: Joins BunnyBot to the voice channel you are in.\n\n!Bb leave: Makes BunnyBot leave the voice channel.\n\n!Bb play (search terms): Play a song in your voice chat. If you attempt to play a song when a song is playing, it will add it to the queue. Ex. !Bb play look want you made me do\n\n!Bb queue (search terms): Add a song to the queue. Ex. !Vb queue look what you made me do\n\n!Bb pause: Pauses a song is playing, if there is a paused song, this will resume it.\n\n!Bb resume: Will resume the song if a song is paused.\n\n!Bb skip: Skips the song bassed on a vote.\n\n!Bb volume: change the volume. You need to use a number that is inbetween 0 and and 100\n\n$ai: Talk to the ai\n\n!Bb uwu: Toggles uwu mode")
    await ctx.send(embed=embedVar)


@client.command(pass_context=True)
@commands.has_role('Discord Admin')
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=None)
    embedVar = discord.Embed(colour=discord.Colour.blue(), title=f'Kicked `{member.display_name}`')
    await ctx.send(embed=embedVar)


@client.command()
@commands.has_role('Discord Admin')
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    embedVar = discord.Embed(colour=discord.Colour.blue(), title=f'Banned `{member.display_name}`')
    await ctx.send(embed=embedVar)


@client.command()
@commands.has_role('Discord Admin')
async def unban(ctx, *, member):
    bannned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in bannned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            embedVar = discord.Embed(colour=discord.Colour.blue(), title=f'Unbanned {user.mention}')
            await ctx.send(embed=embedVar)
            return

@client.command(aliases=["whois"])
async def userinfo(ctx, member: discord.Member = None):
    if not member:  # if member is no mentioned
        member = ctx.message.author  # set member as the author
    roles = [role.mention for role in member.roles[1:]]

    embed = discord.Embed(colour=discord.Colour.blue(), timestamp=ctx.message.created_at,
                          title=f"User Info - {member}")
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f"Requested by {ctx.author}")

    embed.add_field(name="ID:", value=member.id)
    embed.add_field(name="Display Name:", value=member.display_name)
    
    time_in_days = 365 * (datetime.now().year - int(member.created_at.strftime("%Y"))) + 30 * int(member.created_at.strftime("%m")) + int(member.created_at.strftime("%d"))
    time_in_years = time_in_days / 365
    print(time_in_years)
    embed.add_field(name="Created Account On:", value=f'{member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC")}, Thats about {time_in_days} days from now ')
    embed.add_field(name="Joined Server On:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))

    embed.add_field(name="Roles:", value="".join(roles))
    embed.add_field(name="Highest Role:", value=member.top_role.mention)
    
    print(member.top_role.mention)
    await ctx.send(embed=embed)

@client.command()
@commands.has_role('Discord Admin')
async def mute(ctx, member: discord.Member):
    guild = ctx.guild

    for role in guild.roles:
        if role.name == "Muted":
            await member.add_roles(role)
            embedVar = discord.Embed(colour=discord.Colour.blue(), title=f'{member.mention} has been muted by {ctx.author.mention}')
            await ctx.send(embed=embedVar)
            return

            overwrite = discord.PermissionsOverwrite(send_messages=False)
            newRole = await guild.create_role(name="Muted")

            for channel in guild.text_channels:
                await channel.set_permissions(newRole, overwrite=overwrite)

            await members.add_roles(newRole)
            embedVar = discord.Embed(colour=discord.Colour.blue(), title=f'{member.mention} has been muted by {ctx.author.mention}')
            await ctx.send(embed=embedVar)


@client.command()
@commands.has_role('Discord Admin')
async def unmute(ctx, member: discord.Member):
    guild = ctx.guild

    for role in guild.roles:
        if role.name == "Muted":
            await member.remove_roles(role)
            embedVar = discord.Embed(colour=discord.Colour.blue(), title=f'{member.mention} has been unmuted by {ctx.author.mention}')
            await ctx.send(embed=embedVar)

@client.command()
@commands.has_role('Discord Admin')
async def purge(ctx, amount):
    try:
        true_amt = int(amount) + 1
    except:
        embedVar = discord.Embed(colour=discord.Colour.blue(),
                                 title=f'Please enter a number')
        await ctx.send(embed=embedVar)
        return
    await ctx.channel.purge(limit=true_amt)

@client.command()
async def level(ctx):
    a = open('levels.json')
    levels_data = json.load(a)
    xp = int((levels_data[str(ctx.message.author)]["xp"]))
    level = (levels_data[str(ctx.message.author)]["level"])
    level_xp = int(xp) * 2
    if level_xp == 0:
        embedVar = discord.Embed(colour=discord.Colour.blue(), title=f"{ctx.message.author.name}",
                                 description=f"Level {level}\n:black_large_square: :black_large_square: :black_large_square: :black_large_square: :black_large_square: :black_large_square: :black_large_square: :black_large_square: :black_large_square: :black_large_square: ({level_xp / 100 * 100}%)")
    if level_xp > 0 and level_xp < 10:
        embedVar = discord.Embed(colour=discord.Colour.blue(), title=f"{ctx.message.author.name}",
                                 description=f"Level {level}\n:blue_square: :black_large_square: :black_large_square: :black_large_square: :black_large_square: :black_large_square: :black_large_square: :black_large_square: :black_large_square: :black_large_square: ({level_xp / 100 * 100}%)")
    if level_xp >= 10 and level_xp < 20:
        embedVar = discord.Embed(colour=discord.Colour.blue(), title=f"{ctx.message.author.name}",
                                 description=f"Level {level}\n:blue_square: :blue_square: :black_large_square: :black_large_square: :black_large_square: :black_large_square: :black_large_square: :black_large_square: :black_large_square: :black_large_square: ({level_xp / 100 * 100}%)")
    if level_xp >= 20 and level_xp < 30:
        embedVar = discord.Embed(colour=discord.Colour.blue(), title=f"{ctx.message.author.name}",
                                 description=f"Level {level}\n:blue_square: :blue_square: :blue_square: :black_large_square: :black_large_square: :black_large_square: :black_large_square: :black_large_square: :black_large_square: :black_large_square: ({level_xp / 100 * 100}%)")
    if level_xp >= 30 and level_xp < 40:
        embedVar = discord.Embed(colour=discord.Colour.blue(), title=f"{ctx.message.author.name}",
                                 description=f"Level {level}\n:blue_square: :blue_square: :blue_square: :blue_square: :black_large_square: :black_large_square: :black_large_square: :black_large_square: :black_large_square: :black_large_square: ({level_xp / 100 * 100}%)")
    if level_xp >= 40 and level_xp < 100:
        embedVar = discord.Embed(colour=discord.Colour.blue(), title=f"{ctx.message.author.name}",
                                 description=f"Level {level}\n:blue_square: :blue_square: :blue_square: :blue_square: :blue_square: :black_large_square: :black_large_square: :black_large_square: :black_large_square: :black_large_square: ({level_xp / 100 * 100}%)")
    if level_xp > 100 and level_xp < 60:
        embedVar = discord.Embed(colour=discord.Colour.blue(), title=f"{ctx.message.author.name}",
                                 description=f"Level {level}\n:blue_square: :blue_square: :blue_square: :blue_square: :blue_square: :blue_square: :black_large_square: :black_large_square: :black_large_square: :black_large_square: ({level_xp / 100 * 100}%)")
    if level_xp >= 60 and level_xp < 70:
        embedVar = discord.Embed(colour=discord.Colour.blue(), title=f"{ctx.message.author.name}",
                                 description=f"Level {level}\n:blue_square: :blue_square: :blue_square: :blue_square: :blue_square: :blue_square: :blue_square: :black_large_square: :black_large_square: :black_large_square: ({level_xp / 100 * 100}%)")
    if level_xp >= 70 and level_xp < 80:
        embedVar = discord.Embed(colour=discord.Colour.blue(), title=f"{ctx.message.author.name}",
                                 description=f"Level {level}\n:blue_square: :blue_square: :blue_square: :blue_square: :blue_square: :blue_square: :blue_square: :blue_square: :black_large_square: :black_large_square: ({level_xp / 100 * 100}%)")
    if level_xp >= 80 and level_xp < 90:
        embedVar = discord.Embed(colour=discord.Colour.blue(), title=f"{ctx.message.author.name}",
                                 description=f"Level {level}\n:blue_square: :blue_square: :blue_square: :blue_square: :blue_square: :blue_square: :blue_square: :blue_square: :blue_square: :black_large_square: ({level_xp / 100 * 100}%)")
    if level_xp >= 90 and level_xp < 100:
        embedVar = discord.Embed(colour=discord.Colour.blue(), title=f"{ctx.message.author.name}",
                                 description=f"Level {level}\n:blue_square: :blue_square: :blue_square: :blue_square: :blue_square: :blue_square: :blue_square: :blue_square: :blue_square: :blue_square: ({level_xp / 100 * 100}%)")
    # else:
    #   print('error')
    #  embedVar = discord.Embed(title="Error", description="An Error has occored")
    try:
        await ctx.send(embed=embedVar)
    except:
        pass

@client.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    if message_id == 772611461536153601:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)
        if payload.emoji.name == 'Netherite_Sword':
            role = discord.utils.get(guild.roles, name='Anarchy')
        elif payload.emoji.name == 'Dirt':
            role = discord.utils.get(guild.roles, name='Vanilla Craft SMP')
        else:
            role = discord.utils.get(guild.roles, name=payload.emoji.name)

        if role is not None:
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            if member is not None:
                await member.add_roles(role)
            else:
                print('Member not found')
        else:
            print('Role not found')

@client.event
async def on_raw_reaction_remove(payload):
    message_id = payload.message_id
    if message_id == 772611461536153601:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
        if payload.emoji.name == 'Netherite_Sword':
            role = discord.utils.get(guild.roles, name='Anarchy')
        elif payload.emoji.name == 'Dirt':
            role = discord.utils.get(guild.roles, name='Vanilla Craft SMP')
        else:
            role = discord.utils.get(guild.roles, name=payload.emoji.name)

        if role is not None:
            member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
            if member is not None:
                await member.remove_roles(role)
            else:
                print('Member not found')
        else:
            print('Role not found')

#@client.event
#async def on_member_join(member):
 #   guild = member.guild
  #  print(str(member.mention) + ' joined')
   # channel = client.get_channel(752649321601695879)
    #await channel.send('Hello ' + str(
     #   member.mention) + ', make sure to cheak out <#720073337644122172> for the rules, <#742794245903089685> contains the ip. Have Fun!')
    #for role in guild.roles:
     #   if role.name == "Member":
      #      await member.add_roles(role)


#@client.event
#async def on_member_remove(member):
 #   print(str(member.mention) + ' left')
  #  channel = client.get_channel(752649321601695879)
   # await channel.send('Bye ' + str(member.mention))


@client.command(pass_context=True)
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    embed = discord.Embed(title=f"Joined {channel}")
    await ctx.send(embed=embed)


@client.command(pass_context=True)
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        embed = discord.Embed(title=f"Left {channel}")
        await ctx.send(embed=embed)


@client.command(pass_context=True, aliases=['p', 'pla'])
async def play(ctx, *, arg):
    def check_queue():
        Queue_infile = os.path.isdir("./Queue")
        if Queue_infile is True:
            DIR = os.path.abspath(os.path.realpath("Queue"))
            length = len(os.listdir(DIR))
            still_q = length - 1
            try:
                first_file = os.listdir(DIR)[0]
            except:
                print("No more queued song(s)\n")
                queues.clear()
                return
            main_location = os.path.dirname(os.path.realpath(__file__))
            song_path = os.path.abspath(
                os.path.realpath("Queue") + "\\" + first_file)
            if length != 0:
                print("Song done, playing next queued\n")
                print(f"Songs still in queue: {still_q}")
                song_there = os.path.isfile("song.mp3")
                if song_there:
                    os.remove("song.mp3")
                shutil.move(song_path, main_location)
                for file in os.listdir("./"):
                    if file.endswith(".mp3"):
                        os.rename(file, 'song.mp3')

                voice.play(
                    discord.FFmpegPCMAudio("song.mp3"),
                    after=lambda e: check_queue())
                voice.source = discord.PCMVolumeTransformer(voice.source)
                voice.source.volume = 0.50
                #for x in range(len(the_list_of_queues)): 
                 #   print(the_list_of_queues[x])
                  #  if the_list_of_queues[x] == title:
                   #     the_list_of_queues.remove(title)

            else:
                queues.clear()
                return

        else:
            queues.clear()
            print("No songs were queued before the ending of the last song\n")

    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            queues.clear()
            print("Removed old song file")
    except PermissionError:
        print("Trying to delete song file, but its being played")
        #await ctx.send("Music is playing, adding song to queue...")
        Queue_infile = os.path.isdir("./Queue")
        if Queue_infile is False:
            os.mkdir("Queue")
        DIR = os.path.abspath(os.path.realpath("Queue"))
        q_num = len(os.listdir(DIR))
        q_num += 1
        add_queue = True
        while add_queue:
            if q_num in queues:
                q_num += 1
            else:
                add_queue = False
                queues[q_num] = q_num

        queue_path = os.path.abspath(
            os.path.realpath("Queue") + f"\song{q_num}.%(ext)s")

        ydl_opts = {
            'format':
                'bestaudio/best',
            'quiet':
                True,
            'outtmpl':
                queue_path,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192'
            }],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Downloading audio now\n")
            results = YoutubeSearch(arg, max_results=1).to_dict()
            try:
                end_url = results[0]['url_suffix']
                title = results[0]['title']
                thumbnails = results[0]['thumbnails']
                thumbnail = thumbnails[0]
            except:
                print(f'There was no results of the search {arg}. Skipping this song')
                return
            music_url = f'https://youtube.com{end_url}'
            ydl.download([music_url])
        #await ctx.send("Added song " + title + " to the queue")
        embed = discord.Embed(colour=discord.Colour.blue(), title = 'Added song to the queue:', description=title)
        embed.set_thumbnail(url=thumbnail)
        await ctx.send(embed=embed)
        the_list_of_queues.append(title)
        print(f"Song: {title} added to queue\n")
        return

    Queue_infile = os.path.isdir("./Queue")
    try:
        Queue_folder = "./Queue"
        if Queue_infile is True:
            print("Removed old queue folder")
            shutil.rmtree(Queue_folder)
    except:
        print("No old Queue folder")

    #await ctx.send("Getting everything ready now")

    voice = get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format':
            'bestaudio/best',
        'quiet':
            True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now\n")
        results = YoutubeSearch(arg, max_results=1).to_dict()
        print(f'Searching for: {arg}')
        try:
            end_url = results[0]['url_suffix']
            title = results[0]['title']
            thumbnails = results[0]['thumbnails']
            thumbnail = thumbnails[0]
        except:
            await ctx.send(f'There was no results of the search {url}. Skipping this song')
            return
        music_url = f'https://youtube.com{end_url}'
        ydl.download([music_url])

    for file in os.listdir("./"):
        print(f"File: {file}\n")
        if file.endswith(".mp3"):
            name = file
            print(f"Renamed File: {file}\n")
            os.rename(file, "song.mp3")
            try:
                voice.play(
                    discord.FFmpegPCMAudio("song.mp3"),
                    after=lambda e: check_queue())
                voice.source = discord.PCMVolumeTransformer(voice.source)
                voice.source.volume = 0.50
            except:
                channel = ctx.message.author.voice.channel
                voice = get(client.voice_clients, guild=ctx.guild)
                if voice and voice.is_connected():
                    await voice.move_to(channel)
                else:
                    voice = await channel.connect()
                #await ctx.send(f"Joined {channel}")
                voice.play(
                    discord.FFmpegPCMAudio("song.mp3"),
                    after=lambda e: check_queue())
                voice.source = discord.PCMVolumeTransformer(voice.source)
                voice.source.volume = 1.00
            nname = name.rsplit("-", 2)
            #await ctx.send(f"Playing: {title}")
            embed = discord.Embed(colour=discord.Colour.blue(), title = 'Playing:', description=title)
            embed.set_thumbnail(url=thumbnail)
            await ctx.send(embed=embed)
            print(f"playing {title}\n")
            the_list_of_queues.append(title)
            #for x in range(len(the_list_of_queues)): 
            #    print(the_list_of_queues[x])
            #    if the_list_of_queues[x] == title:
            #        the_list_of_queues.remove(title)


@client.command(pass_context=True, aliases=['pa', 'pau'])
async def pause(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print("Music paused")
        voice.pause()
        embed = discord.Embed(colour=discord.Colour.blue(), title="Music paused")
        await ctx.send(embed=embed)
    else:
        print("Music not playing, resuming")
        #await ctx.send("Music not playing, resuming")
        if voice and voice.is_paused():
            print("Resumed music")
            voice.resume()
            embed = discord.Embed(colour=discord.Colour.blue(), title="Resumed music")
            await ctx.send(embed=embed)
        else:
            print("Music is not paused, doing nothing")
            embed = discord.Embed(colour=discord.Colour.blue(), title="Music is not paused, doing nothing")
            await ctx.send(embed=embed)
            #await ctx.send("Music is not paused, doing nothing")


@client.command(pass_context=True, aliases=['r', 'res'])
async def resume(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_paused():
        print("Resumed music")
        voice.resume()
        embed = discord.Embed(colour=discord.Colour.blue(), title="Resumed music")
        await ctx.send(embed=embed)
    else:
        print("Music is not paused")
        embed = discord.Embed(colour=discord.Colour.blue(), title="Music is not paused")
        await ctx.send(embed=embed)


@client.command(pass_context=True)
@commands.has_role('Discord Admin')
async def force_skip(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    queues.clear()

    if voice and voice.is_playing():
        print("Music skipped")
        voice.stop()
        embed = discord.Embed(colour=discord.Colour.blue(), title="Music skipped")
        await ctx.send(embed=embed)
    else:
        print("No music playing failed to skip")
        embed = discord.Embed(colour=discord.Colour.blue(), title="No music playing failed to skip")
        await ctx.send(embed=embed)


@client.command(brief="returns a list of the people in the voice channels in the server", )
async def vcmembers(ctx):
    # First getting the voice channels
    voice_channel_list = ctx.guild.voice_channels

    # getting the members in the voice channel
    for voice_channels in voice_channel_list:
        # list the members if there are any in the voice channel
        if len(voice_channels.members) != 0:
            if len(voice_channels.members) == 1:
                await ctx.send("{} member in {}".format(len(voice_channels.members), voice_channels.name))
            else:
                await ctx.send("{} members in {}".format(len(voice_channels.members), voice_channels.name))
            for members in voice_channels.members:
                # if user does not have a nickname in the guild, send thier discord name. Otherwise, send thier guild nickname
                if members.nick == None:
                    await ctx.send(members.name)
                else:
                    await ctx.send(members.nick)
    return await ctx.send(embed=embed)


@client.command(pass_context=True, aliases=['s', 'ski'])
async def skip(ctx):
    global memb
    global memb_vote
    global mem_need_vote
    voice_channel_list = ctx.guild.voice_channels
    channel = ctx.channel
    memb_vote = 0
    in_vc = False
    for voice_channels in voice_channel_list:
        # list the members if there are any in the voice channel
        if len(voice_channels.members) != 0:
            print("{} member in {}".format(len(voice_channels.members), voice_channels.name))
            for member in voice_channels.members:
                print(f'{ctx.author} {member}')
                if ctx.author == member:
                    in_vc = True
                    break
                else:
                    in_vc = False
            memb = len(voice_channels.members)
        else:
            in_vc = False
    if in_vc == False:
        print('Not in vc')
        embed = discord.Embed(title='You are not in a voice chat, there is no music to skip.', color=discord.Colour.blue())
        await ctx.send(embed=embed)
        return
    real_meb = memb - 1
    mem_need_vote = round(real_meb / 2)
    if mem_need_vote == 0:
        voice = get(client.voice_clients, guild=ctx.guild)
        queues.clear()
        if voice and voice.is_playing():
            print("Music skipped")
            voice.stop()
            embed = discord.Embed(colour=discord.Colour.blue(), title="Music skipped")
            await ctx.send(embed=embed)
            return
        else:
            print("No music playing failed to skip")
            embed = discord.Embed(colour=discord.Colour.blue(), title="No music playing failed to skip")
            await ctx.send(embed=embed)
            return
    print(f'To skip, {mem_need_vote} votes are needed')
    #await ctx.send(f'Do you want to skip this song? 0/{mem_need_vote} (react with 👍)')
    embed = discord.Embed(colour=discord.Colour.blue(), title=f'Do you want to skip this song? 0/{mem_need_vote} (react with 👍)')
    msg = await ctx.send(embed=embed)
    #await ctx.message.channel.send
    await msg.add_reaction('👍')

    def check(reaction, user):
        return str(reaction.emoji) == '👍'

    # return str(reaction.emoji) == '👍'

    async def loop():
        global memb_vote
        global memb
        try:
            print('waiting')
            await client.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            print('Ending the vote')
        else:
            print('Someone voted')
            memb_vote += 1
            #await ctx.send(f'Votes: {memb_vote}/{mem_need_vote}')
            embed = discord.Embed(colour=discord.Colour.blue(), title=f'Do you want to skip this song? {memb_vote - 1}/{mem_need_vote} (react with 👍)')
            await msg.edit(embed=embed)
            if memb_vote - 1 == mem_need_vote:
                voice = get(client.voice_clients, guild=ctx.guild)
                queues.clear()
                if voice and voice.is_playing():
                    print("Music skipped")
                    voice.stop()
                    embed = discord.Embed(colour=discord.Colour.blue(), title="Music skipped")
                    await msg.edit(embed=embed)
                    return
                else:
                    print("No music playing failed to skip")
                    embed = discord.Embed(colour=discord.Colour.blue(), title="No music playing failed to skip")
                    await ctx.send(embed=embed)
                    return
            else:
                await loop()

    await loop()
    print('done')


queues = {}


@client.command(aliases=['v', 'vol'])
async def volume(ctx, vol):
    # global voice
    try:
        int_vol = int(vol)
    except:
        embed = discord.Embed(colour=discord.Colour.blue(), title="Please enter a number between 0 and 100")
        await ctx.send(embed=embed)
        return
    if int_vol > 0 and int_vol <= 100:
        #await ctx.send(f'Volume: {vol}%')
        embed = discord.Embed(colour=discord.Colour.blue(), title=f'Volume: {vol}%')
        await ctx.send(embed=embed)
        true_vol = int_vol / 100
        voice = get(client.voice_clients, guild=ctx.guild)
        voice.source.volume = true_vol

@client.command()
async def q(ctx):
    num = 0
    for x in range(len(the_list_of_queues)): 
        print(the_list_of_queues[x])

@client.command(pass_context=True)
async def server_status(ctx, serverip=None, port=25565):
    if serverip == None:
        server = MinecraftServer.lookup("vanilla-craft.ml:25566")
        server1 = MinecraftServer.lookup("192.168.1.77:25567")
        server2 = MinecraftServer.lookup("192.168.1.77:25568")
        status = server.status()
        status1 = server1.status()
        status2 = server2.status()
        #await ctx.send(f'The total players online are: {int(status.players.online)+int(status1.players.online)+int(status2.players.online)}')
        embed = discord.Embed(colour=discord.Colour.blue(), timestamp=ctx.message.created_at, title=f"Vanilla Craft 2.0")
        embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/760471538523701278/2f08439571ba8e5960d48becbf35ca3c.png?size=256')
        embed.set_footer(text=f"vanilla-craft.ml")
        embed.add_field(name="Players Online:                    .", value=int(status.players.online)+int(status1.players.online)+int(status2.players.online))
        embed.add_field(name="Latency:", value=status1.latency)
        await ctx.send(embed=embed)
    else:
        server = MinecraftServer.lookup(f"{serverip}:{port}")
        status = server.status()
        #await ctx.send(f'The total players online are: {int(status.players.online)+int(status1.players.online)+int(status2.players.online)}')
        embed = discord.Embed(colour=discord.Colour.blue(), timestamp=ctx.message.created_at, title=f"Server status")
        #embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/760471538523701278/2f08439571ba8e5960d48becbf35ca3c.png?size=256')
        embed.set_footer(text=serverip)
        embed.add_field(name="Players Online:", value=int(status.players.online))
        embed.add_field(name="Latency:", value=status.latency)
        await ctx.send(embed=embed)

@client.command(pass_context=True)
async def queue(ctx, url: str):
    Queue_infile = os.path.isdir("./Queue")
    if Queue_infile is False:
        os.mkdir("Queue")
    DIR = os.path.abspath(os.path.realpath("Queue"))
    q_num = len(os.listdir(DIR))
    q_num += 1
    the_true_q += 1
    add_queue = True
    while add_queue:
        if q_num in queues:
            q_num += 1
            the_true_q += 1
        else:
            add_queue = False
            queues[q_num] = q_num

    queue_path = os.path.abspath(
        os.path.realpath("Queue") + f"\song{q_num}.%(ext)s")

    ydl_opts = {
        'format':
            'bestaudio/best',
        'quiet':
            True,
        'outtmpl':
            queue_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now\n")
        results = YoutubeSearch(url, max_results=1).to_dict()
        try:
            end_url = results[0]['url_suffix']
        except:
            await ctx.send(f'There was no results of the search {url}. Skipping this song')
            return
        music_url = f'https://youtube.com{end_url}'
        ydl.download([music_url])
    for file in os.listdir("./"):
        name = file
    print(name)
    await ctx.send("Adding song " + str(q_num) + " to the queue")

    print("Song added to queue\n")

send_data_to_monitering_server()

client.run('YOUR TOKEN HERE')