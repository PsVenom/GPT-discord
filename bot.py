
from main import ask, askCrack, scraper, getImg
import discord
from discord.utils import get
from discord.ext import commands, tasks
import json
import random
global model
import nextcord
#discord api token
TOKEN = 'OTcyODczNTA2Mzg5OTE3NzY3.GHNR-Z.oGM6m6dd4Pf_A38hiCnHeBJpwKYYLq0A6CmQ0g'
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
#vanilla chat (activated by 'sext s')
class sext(commands.Cog):
    bots = commands.Bot(command_prefix=['s ', 'sext'], help_command=None)

    def __init__(self, bot):
        self.bot = bot


    @bots.command(name= 's')
    async def s(self, ctx):
        thread = await ctx.channel.create_thread(name = f'chat with {ctx.author} UwU',  message=None, auto_archive_duration=60, type= nextcord.ChannelType.public_thread, reason=None)
        answer = 0
        msg_cont1 = ""
        await thread.send('sup hottie')
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
                await thread.send('bbye baby <3 UwU')
                break

            if answer != 0:
                json_obj = json.dumps({"prompt": msg_cont1, "completion": msg_cont})

                with open("train.json", "w") as outfile:
                    outfile.write(json_obj)
            try:
                answer = ask(msg_cont)
            except:
                answer = "YOUR MOTHER"
                continue
            ms_cont1 = msg_cont
            await thread.send(answer)
        await thread.delete()
#cracked chat (activated by 'sext sc')
class sextC(commands.Cog):
    bots = commands.Bot(command_prefix=['sc ', 'sextC'], help_command=None)

    def __init__(self, bot):
        self.bot = bot


    @bots.command(name= 'sc')
    async def sc(self, ctx):
        thread = await ctx.channel.create_thread(name = f'chat with {ctx.author} UwU',  message=None, auto_archive_duration=60, type= nextcord.ChannelType.public_thread, reason=None)
        answer = 0
        msg_cont1 = ""
        await thread.send('sup hottie')
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
                await thread.send('bbye baby <3 UwU')
                break

            if answer != 0:
                json_obj = json.dumps({"prompt": msg_cont1, "completion": msg_cont})

                with open("train.json", "w") as outfile:
                    outfile.write(json_obj)
            try:
                answer = askCrack(msg_cont)
            except:
                answer = "YOUR MOTHER"
                continue
            ms_cont1 = msg_cont
            await thread.send(answer)
        await thread.delete()

#ahegao fetching (activated by sext ap)
class AhegaoPic(commands.Cog):
    bots = commands.Bot(command_prefix=['ap', 'AhegaoPic'], help_command=None)
    def __init__(self, bots):
        self.bot = bots

    @bots.command(name='ap')
    async def record(self, ctx):
         channel = ctx.message.channel
         def check(m):
            return m.author == ctx.author
         a = scraper()
         print(a)
         embed = discord.Embed()
         file = discord.File(fp = await getImg(), filename = 'Ahegao.jpg')
         await ctx.reply(file = file)
#self-explainatory (activated by sext sauce)
class sauce(commands.Cog):
    bots = commands.Bot(command_prefix=['sauce', 'sc'], help_command=None)
    def __init__(self, bot):
        self.bot = bot
    @bots.command(name = 'sauce')
    async def sauce(self, ctx):
       file = open('codes.csv', 'r').read()
       a = list(file.split(", "))
       await ctx.send("https://nhentai.net/g/"+ a[random.randint(0, len(a)+1)])
#additional porn command
class p(commands.Cog):
    bots = commands.Bot(command_prefix=['p', 'porn'], help_command=None)

    def __init__(self, bot):
        self.bot = bot

    @bots.command(name='p')
    async def p(self, ctx):
        hyperlink = scraper(url_link = 'https://realbooru.com/index.php?page=post&s=list&tags=brazzers', remove = 5)
        ctx.send(hyperlink)


bots.add_cog(help(bots))
bots.add_cog(sext(bots))
bots.add_cog(sextC(bots))
bots.add_cog(AhegaoPic(bots))
bots.add_cog(sauce(bots))
bots.add_cog(p(bots))
bots.run(TOKEN)