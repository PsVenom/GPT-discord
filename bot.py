
from main import ask, fit, scraper
import discord
from discord.utils import get
from discord.ext import commands, tasks
import json
global model

TOKEN = 'OTcyODczNTA2Mzg5OTE3NzY3.GYgm4S.fqzm4JJSC6bpyYX8DGGu3HL34m4XqrltTuBmOA'

client = discord.Client()

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

class sext(commands.Cog):
    bots = commands.Bot(command_prefix=['sext ', 's!'], help_command=None)

    def __init__(self, bot):
        self.bot = bot


    @bots.command(name='sext')
    async def sext(self, ctx):

        await ctx.send('Ram ram cutie UwU <3')

        answer = 0
        msg_cont1 = ""
        channel = ctx.message.channel

        while True:

            f = 0

            def check(m):
                return m.author == ctx.author

            try:
                msg = await bots.wait_for('message', timeout=20.0, check=check)
                msg_cont = msg.content
            except:
                f = 1

            a = msg_cont == 'end'
            b = f == 1

            if a or b:
                await channel.send('bbye baby <3 UwU')
                break

            if answer != 0:
                json_obj = json.dumps({"prompt": msg_cont1, "completion": msg_cont})

                with open("train.json", "w") as outfile:
                    outfile.write(json_obj)
            try:
                answer = await ask(msg_cont, a)
            except discord.ext.commands.errors.CommandInvokeError as e:
                answer = "YOUR MOTHER"
                continue
            ms_cont1 = msg_cont
            await channel.send(answer)
            try:
                model = fit("train.json")
                print("fit sucessful")
            except RuntimeError as e:
                continue


class AhegaoPic(commands.Cog):
    bots = commands.Bot(command_prefix=['AhegaoPic', 'ap'], help_command=None)
    def __init__(self, bot):
        self.bot = bot

    @bots.command(name='AhegaoPic')
    async def record(self, ctx):
         channel = ctx.message.channel
         def check(m):
            return m.author == ctx.author
         a = scraper()
         print(a)
         embed = discord.Embed()
         try:
          img = embed.set_image(url= str(a))
         except discord.ext.commands.errors.CommandInvokeError as e:
          img = embed.set_image(url="https://qph.fs.quoracdn.net/main-qimg-965b11ec95106e64d37f5c380802c305-lq")
         file = discord.File(fp= open("", "rb"), filename="image.png")
         await ctx.send(file=file, embed=embed)







bots.add_cog(help(bots))
bots.add_cog(sext(bots))
bots.add_cog(AhegaoPic(bots))
bots.run(TOKEN)
