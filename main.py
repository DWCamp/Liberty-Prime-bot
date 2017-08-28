import discord
import sys
from random import randint
import urllib.request
from discord.ext import commands
from Map_Functions import *


# Defines Bot, Bot prefix, bot description, and the server
bot = commands.Bot(command_prefix = '%', description = 'Deliverer of Freedom and Democracy. Also serving discord channels near you!')
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'

@bot.event
async def on_ready():
    discord.opus.load_opus('libopus-0.x64.dll')
    await bot.change_presence(game=discord.Game(name='Freedom and Democracy'))
     #await bot.send_message(bot.get_channel('335560493454327808'),
     #                       'Liberty Prime is online. All systems nominal. Weapons hot. Mission: the destruction of any and all Chinese communists')

@bot.event
async def on_error():
    await bot.send_message(bot.get_channel('336262010033405952'), sys.exc_info())

@bot.event
async def on_member_join(member):
    general = bot.get_channel('335560493454327808')
    welcome = bot.get_channel('341749474164473856')
    rules = bot.get_channel('341749548110053377')
    await bot.send_message(general, 'Welcome ' + member.mention+', please read ' + welcome.mention +
                           ' and the pinned message in ' + rules.mention)

@bot.event
async def on_member_remove(member):
    await bot.send_message(bot.get_channel('335560493454327808'), 'Bye bye, ' + member.name + '#' + member.discriminator)


@bot.command()
async def hello():
	await bot.say("Hello, citizen.")

@bot.command(pass_context = True)
async def givecookie(ctx):
    recipients = ctx.message.mentions
    for recipient in recipients:
        await bot.say(recipient.mention + ', here\'s a cookie ' + '\U0001F36A')

@bot.command(pass_context = True)
async def sendfreedom(ctx):
    recipients = ctx.message.mentions
    for recipient in recipients:
        await bot.say('\U0001F4A5'+' '+'\U0001F1FA'+'\U0001F1F8'+' '+recipient.mention+
                      ', HAVE SOME FREEDOM, COMMUNIST SCUM! '+'\U0001F1FA'+'\U0001F1F8'+' '+'\U0001F4A5')

@bot.command(pass_context = True)
async def prime(ctx):
    quotes = []
    with open('C:\\Users\\Brandon\\Desktop\\Python\\discord bots\\quotes\\quotes.txt', 'r') as quotefile:
        for line in quotefile:
            quotes.append(line.strip())
    number = randint(0, len(quotes)-1)
    await bot.say(quotes[number])
    if bot.is_voice_connected(bot.get_server('335560493454327808')):
        for x in bot.voice_clients:
            if x.server == ctx.message.server:
                voice = x
        player = voice.create_ffmpeg_player('C:\\Users\\Brandon\\Desktop\\Python\\discord bots\\quotes\\quote #{}.wav').format(str(number+1))
        player.start()

@bot.command()
async def join():
    if not bot.is_voice_connected(bot.get_server('335560493454327808')):
        voice = await bot.join_voice_channel(bot.get_channel('335560493458522112'))
        player = voice.create_ffmpeg_player('C:\\Users\\Brandon\\Desktop\\Python\\discord bots\\quotes\\join.wav')
        player.start()
    else:
        await bot.say('I am already in a voice channel.')

@bot.command(pass_context = True)
async def leave(ctx):
    if bot.is_voice_connected(bot.get_server('335560493454327808')):
        for x in bot.voice_clients:
            if x.server == ctx.message.server:
                return await x.disconnect()
        something_playing = False
        return await bot.say('I am not connected to any voice channel on this server.')
    else:
        return await bot.say('I am not connected to any voice channel on this server.')

@bot.command(pass_context = True)
async def addroll(ctx):
    server = bot.get_server('335560493454327808')
    possible_roles = []
    for role in server.roles:
        if role.name not in ['Peasants', 'Mod', 'Tinkerer', 'Bot']:
            possible_roles.append(role)
    roles = []
    msg = ctx.message.content.split('addroll ')[1]
    try:
        for role in possible_roles:
            if role.name == msg:
                roles.append(role)
        if len(roles) > 0:
            await bot.add_roles(ctx.message.author, roles)
        else:
            await bot.say('No eligible roles')
    except:
        await bot.say('Problem with the input, please try again.')

@bot.command(pass_context = True)
async def removeroll(ctx):
    server = bot.get_server('335560493454327808')
    possible_roles = []
    for role in server.roles:
        if role.name not in ['Peasants', 'Mod', 'Tinkerer', 'Bot']:
            possible_roles.append(role)
    roles = []
    msg = ctx.message.content.split('removeroll ')[1]
    try:
        for role in possible_roles:
            if role.name == msg:
                roles.append(role)
        if len(roles) > 0:
            await bot.remove_roles(ctx.message.author, roles)
        else:
            await bot.say('No eligible roles')
    except:
        await bot.say('Problem with the input, please try again.')

@bot.command(pass_context = True)
async def roll(ctx):
    valid_dice = ['d2', 'd4', 'd6', 'd8', 'd10', 'd12', 'd20', 'd100']
    dice_input = ctx.message.content.split(' ')[1]
    for dice in valid_dice:
        if dice in ctx.message.content:
            num_dice = dice_input.split('d')[0]
            size_die = dice_input.split('d')[1]
    try:
        num_dice = int(num_dice)
        size_die = int(size_die)
    except:
        await bot.say('Problem with the input, please try again.')
    result = 0
    for n in range(num_dice):
        result += randint(1, size_die)
    await bot.say(result)

@bot.command()
async def flipcoin():
    result = randint(0, 1)
    if result == 0:
        result = 'Heads'
    elif result == 1:
        result = 'Tails'
    await bot.say(result)

@bot.command(pass_context = True)
async def poll(ctx):
    await bot.add_reaction(ctx.message, '\N{THUMBS UP SIGN}')
    await bot.add_reaction(ctx.message, '\N{THUMBS DOWN SIGN}')
    await bot.add_reaction(ctx.message, '\U0001F937')

@bot.command(pass_context = True)
async def file(ctx):
    URL = ctx.message.attachments[0]['url']
    req = urllib.request.Request(URL, headers={'User-Agent': user_agent})
    with urllib.request.urlopen(req) as url:
        with open('player_country_list.txt', 'wb') as f:
            f.write(url.read())
    await bot.say('Got the file')

@bot.command(pass_context = True)
async def list(ctx):
    await bot.say('Coming soon')

@bot.command()
async def getlist():
    countryList = collectCountries()
    message = ''
    for country in countryList:
        if country.name not in ['ocean','uncolonized','wasteland']:
            name = country.name
            if country.isVassal:
                name = '-'+country.name
            message = message + (name) +'\n'
    await bot.send_message(bot.get_channel('336262010033405952'), message)

@bot.command(pass_context = True)
async def create(ctx):
    inputImage = 'original.png'
    outputImage = 'final.png'
    if len(ctx.message.attachments) > 0:
        await bot.say('Processing')
        URL = ctx.message.attachments[0]['url']
        req = urllib.request.Request(URL, headers={'User-Agent': user_agent})
        with urllib.request.urlopen(req) as url:
            with open(inputImage, 'wb') as f:
                f.write(url.read())
        changeColors(inputImage).save(outputImage)
        return await bot.send_file(bot.get_channel('336262010033405952'), open(outputImage, 'rb'))
    else:
        return await bot.say('Invalid command entry, upload an image and type "%create" in the "add a comment" part')

@bot.command(pass_context = True)
async def shutdown(ctx):
    if ctx.message.author.id == '196866248984887296':
        await bot.send_message(bot.get_channel('335560493454327808'), 'Initiate shutdown protocal')
        await bot.close()
    else:
        hacker = ctx.message.author
        await bot.say('Communist hacking detected, initiating freedom protocol!')
        await bot.say('\U0001F4A5'+' '+'\U0001F1FA'+'\U0001F1F8'+' '+hacker.mention+
                      ', HAVE SOME FREEDOM, COMMUNIST SCUM! '+'\U0001F1FA'+'\U0001F1F8'+' '+'\U0001F4A5')


bot.run('MzUxMTUzMzI4Mzg4MDQ2ODU5.DIOclw.pyZAa0BWpblMimYlpvLZcoOiEXo')