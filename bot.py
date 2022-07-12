
from main import ask,  scraper, getImg
import discord
from discord.utils import get
from discord.ext import commands, tasks
import json
import random
global model
import nextcord
#discord api token
TOKEN = '<token>'
#initialise api object
client = discord.Client()
#initialise bot
bots = commands.Bot(command_prefix=['sext ', 's!'], help_command=None)

global msg_cont
class help(commands.Cog):
    bots = commands.Bot(command_prefix=['sext ', 's'], help_command=None)

    def __init__(self, bot):
        self.bot = bot

    @bots.command(name='help')
    async def help(self, ctx):
        title = ''
        description = ''
        z = int('', 16)

        embed = discord.Embed(title=title, description=description, colour=discord.Colour(z))
class text(commands.Cog):
    bots = commands.Bot(command_prefix=['t ', 'text'], help_command=None)

    def __init__(self, bot):
        self.bot = bot


    @bots.command(name= 't')
    async def t(self, ctx):
        thread = await ctx.channel.create_thread(name = f'chat with {ctx.author}',  message=None, auto_archive_duration=60, type= nextcord.ChannelType.public_thread, reason=None)
        answer = 0
        msg_cont1 = ""
        await thread.send('sup')
        while True:

            f = 0

            def check(m):
                return m.author == ctx.author

            try:
                msg = await bots.wait_for('message', timeout=120.0, check=check)
                msg_cont = msg.content
            except:
                f = 1

            a = msg_cont == 'end'
            b = f == 1

            if a or b:
                await thread.send('bbye!')
                break

            if answer != 0:
                json_obj = json.dumps({"prompt": msg_cont1, "completion": msg_cont})

                with open("train.json", "w") as outfile:
                    outfile.write(json_obj)
            try:
                answer = ask(msg_cont)
            except:
                answer = "Exception occured- logging error"
                continue
            ms_cont1 = msg_cont
            await thread.send(answer)
        await thread.delete()
        
class tts(commands.Cog):
    bots = commands.Bot(command_prefix=['tts'], help_command=None)
    def __init__(self, bot):
        self.bot = bot

    @bots.command(name = 'tts')
    async def tts(self,ctx):
        global vc
        channel = ctx.message.channel
        answer = 0
        msg_cont1 = ""
        voicechannel = discord.utils.get(ctx.guild.channels, name='General')
        try:
         vc = await voicechannel.connect()
        except:
            vc
        while True:

            f = 0

            def check(m):
                return m.author == ctx.author

            try:
                msg = await bots.wait_for('message', timeout=120.0, check=check)
                msg_cont = msg.content
            except:
                f = 1

            a = msg_cont == 'end'
            b = f == 1

            if a or b:
                await channel.send('tts disconnedted due to inactivity')
                break

            try:
                output = gTTS(text=msg_cont, lang="en", tld="co.in")
                output.save(f"tts.mp3")
                vc.play(discord.FFmpegPCMAudio(source="tts.mp3", executable='C:/ffmpeg/bin/ffmpeg.exe'))
            except:
                answer = "Exception occured, recording in log"

class vc(commands.Cog):
    bots = commands.Bot(command_prefix=['vc '], help_command=None)

    def __init__(self, bot):
        self.bot = bot


    @bots.command(name= 'vc')
    async def vc(self, ctx):
        global vc
        channel=ctx.message.channel
        answer = 0
        msg_cont1 = ""
        voicechannel = discord.utils.get(ctx.guild.channels, name='General')
        try:
            vc = await voicechannel.connect()
        except:
            vc
        output = gTTS(text='sup', lang="en", tld="co.in")
        output.save(f"tts.mp3")
        vc.play(discord.FFmpegPCMAudio(source="tts.mp3", executable='C:/ffmpeg/bin/ffmpeg.exe'))
        while True:

            f = 0

            def check(m):
                return m.author == ctx.author

            try:
                msg = await bots.wait_for('message', timeout=120.0, check=check)
                msg_cont = msg.content
            except:
                f = 1

            a = msg_cont == 'end'
            b = f == 1

            if a or b:
                await channel.send('bbye baby <3 UwU')
                break

            try:
                answer = ask(msg_cont)
                output = gTTS(text=answer, lang="en", tld="co.in")
                output.save(f"tts.mp3")
                vc.play(discord.FFmpegPCMAudio(source="tts.mp3", executable='C:/ffmpeg/bin/ffmpeg.exe'))
            except:
                answer = "Exception occured, logging error"
                continue
            ms_cont1 = msg_cont
            #await channel.delete()
 
bots.add_cog(help(bots))
bots.add_cog(text(bots))
bots.add_cog(tts(bots))
bots.add_cog(vc(bots))
bots.run(TOKEN)
