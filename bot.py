
from main import ask, fit
import discord
from discord.utils import get
from discord.ext import commands, tasks
import json


TOKEN = ''

client = discord.Client()

bots = commands.Bot(command_prefix=['sext ', 's!'], help_command=None)

global msg_cont
class help(commands.Cog):
    bots = commands.Bot(command_prefix=['sext ', 's!'], help_command=None)

    def __init__(self, bot):
        self.bot = bot

    @bots.command(name='help')
    async def help(self, ctx):
        title = ''
        description = ''
        z = int('', 16)

        embed = discord.Embed(title=title, description=description, colour=discord.Colour(z))


bots.add_cog(help(bots))


class sext(commands.Cog):
    bots = commands.Bot(command_prefix=['sext ', 's!'], help_command=None)

    def __init__(self, bot):
        self.bot = bot

    @bots.command(name='sext')
    async def sext(self, ctx):

        await ctx.send('Ram ram cutie UwU <3')

        answer = 0

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
                json_obj = json.dumps({"prompt": answer, "completion": msg_cont})

                with open("train.json", "w") as outfile:
                    outfile.write(json_obj)
            try:
                answer = ask(msg_cont)
            except discord.ext.commands.errors.CommandInvokeError as e:
                answer = "YOUR MOTHER"
                continue

            await channel.send(answer)
            try:
                fit("scratch.json")
                print("fit sucessful")
            except RuntimeError as e:
                continue



bots.add_cog(sext(bots))

bots.run(TOKEN)