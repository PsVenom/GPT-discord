import os
from main import ask
import discord
from discord.utils import get
from discord.ext import commands, tasks
import json
from time import time

TOKEN = 'OTcyODczNTA2Mzg5OTE3NzY3.GYgm4S.fqzm4JJSC6bpyYX8DGGu3HL34m4XqrltTuBmOA'

client = discord.Client()

bots = commands.Bot(command_prefix=['sext ', 's!'], help_command=None)

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

        answer=0

        channel = ctx.message.channel

        while True:

            timeref = time()
            
            def check(m):
                return m.author == ctx.author

            msg = await bots.wait_for('message', check=check)
            msg_cont = msg.content

            a=msg_cont=='end'
            b=time()-timeref>=10

            if a or b:
                await channel.send('bbye baby <3 UwU')
                break

            if answer!=0:
                
                json_obj = json.dumps({"prompt": answer,"completion": msg_cont})

                with open ("train.json", "w") as outfile:
                    outfile.write(json_obj)

            answer = ask(msg_cont)
            await channel.send(answer)


bots.add_cog(sext(bots))

bots.run(TOKEN)
