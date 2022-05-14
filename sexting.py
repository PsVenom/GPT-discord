import os

import discord
from discord.utils import get
from discord.ext import commands, tasks

TOKEN = 'OTcyODczNTA2Mzg5OTE3NzY3.YnfZDw.jkVsaoaRXU5zIkAo-buALowPs3I'

client = discord.Client()

bots = commands.Bot(command_prefix=['sext ','s!'], help_command=None)

class help(commands.Cog):

    bots = commands.Bot(command_prefix=['sext ','s!'], help_command=None)

    def __init__(self, bot):
        self.bot = bot
        
    @bots.command(name='help')
    async def help(self, ctx):

        title=''
        description=''
        z=int('',16)

        embed = discord.Embed(title=title, description=description, colour=discord.Colour(z))

bots.add_cog(help(bots))

class sext(commands.Cog):

    bots = commands.Bot(command_prefix=['sext ','s!'], help_command=None)

    def __init__(self, bot):
        self.bot = bot
        
    @bots.command(name='sext')
    async def sext(self, ctx):

        await ctx.send('Ram ram cutie UwU <3')

        channel = ctx.message.channel

        while True:

            def check(m):
                return m.author == ctx.author

            msg = await bots.wait_for('message',check=check)
            msg_cont=msg.content

            if msg_cont=='end':
                
                await channel.send('bbye baby <3 UwU')
                break

            await channel.send('baby!!')

bots.add_cog(sext(bots))

bots.run(TOKEN)