#Importing Modules
import discord
from discord.ext import commands
import random
import os
from dotenv import load_dotenv

#Importing useful functions from main.py
from main import ask, scraper, getImg

#Declaring token variable for discord bot
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

#Initialise bot object
bots = commands.Bot(case_insensitive=True, command_prefix=['ahegao ', 'a!', 'sext ', 'Sext '], help_command=None, )

#Help related commands
class help(commands.Cog):

    bots = commands.Bot(case_insensitive=True, command_prefix=['ahegao ', 'a!', 'sext ', 'Sext '], help_command=None, )

    def __init__(self, bot):
        self.bot = bot

    @bots.command(aliases=['help','h'])
    async def _help(self, ctx):
        title = '**__Bot Commands__**'
        description = '''
        **__Help__**
        **help/h** - displays this message

        **__Sexting__**
        **sext/s** - initialises sexting interaction with the bot. The bot will respond to every message you send in the chat. Use **end** to stop the interaction.

        **__Media__**
        **ahegaopic/ap** - sends a random high quality Ahegao Pic
        **sauce/doujin** - sends a random handpicked doujin link from nhentai

        '''
        z = int('fffeee', 16)
        print(type(discord.Colour(z)))
        embed = discord.Embed(title=title, description=description, colour=discord.Colour(z))
        embed.set_image(url='https://imgur.com/Mzukcha.jpg')
        await ctx.send(embed=embed)

#Sexting related commands using OpenAi
class sexting(commands.Cog):

    bots = commands.Bot(case_insensitive=True, command_prefix=['ahegao ', 'a!', 'sext ', 'Sext '], help_command=None, )

    def __init__(self, bot):
        self.bot = bot

    @bots.command(aliases=['sext','s'])
    async def _sext(self, ctx):

        channel=ctx.message.channel
        answer = 0
        msg_cont=""
        greetings=['Heyaa!', "Hi babyy!", "Hewoo!", "Hey hottie!"]
        greet=random.choice(greetings)
        await channel.send(greet)
        while True:

            f = 0

            def check(m):
                return m.author == ctx.author

            try:
                msg = await bots.wait_for('message', timeout=120.0, check=check)
                msg_cont = msg.content
            except:
                f = 1

            a = msg_cont.lower() == 'end'
            b = f == 1

            if a or b:
                byes=['bbye baby <3 UwU','bye! I will miss ya!','Take care! <3','Cya later ^^', 'Bye! love ya!']
                bye=random.choice(byes)
                await channel.send(bye)
                break

            try:
                answer = ask(msg_cont)
            except:
                answer = "YOUR MOTHER"
                continue
            await channel.send(answer)

#Media related commands 
class Media(commands.Cog):

    bots = commands.Bot(case_insensitive=True, command_prefix=['ahegao ', 'a!', 'sext ', 'Sext '], help_command=None, )

    def __init__(self, bots):
        self.bot = bots

    @bots.command(aliases=['ahegaopic','ap'])
    async def _ahegaopic(self, ctx):
        if ctx.channel.is_nsfw():
            file = discord.File(fp = await getImg(), filename = 'Ahegao.jpg')
            await ctx.send(file = file)
        else:
            await ctx.send("You can only use this command in NSFW channels!")

    @bots.command(aliases = ['sauce','doujin'])
    async def _sauce(self, ctx):
        if ctx.channel.is_nsfw():
            file = open('codes.csv', 'r').read()
            a = list(file.split(", "))
            await ctx.send("https://nhentai.net/g/"+ a[random.randint(0, len(a)+1)])
        else:
            await ctx.send("You can only use this command in NSFW channels!")

#porn command
class porn(commands.Cog):

    bots = commands.Bot(case_insensitive=True, command_prefix=['ahegao ', 'a!', 'sext ', 'Sext '], help_command=None, )

    def __init__(self, bot):
        self.bot = bot

    @bots.command(name='rlporn')
    async def porn(self, ctx):

        if ctx.channel.is_nsfw():

            a=ctx.message.content.split()
            n=1 

            if len(a)==3:
                try: 
                    n=int(a[-1])
                    if n>15:
                        n=15
                except:
                    n=1

            elif len(a)==2 and a[0]=="a!rlporn":
                try: 
                    n=int(a[-1])
                    if n>15:
                        n=15
                except:
                    n=1

            for i in range (n):

                link = f"https://realbooru.com/index.php?page=post&s=list&tags=gif&pid={random.randint(1,500)}"
                hyperlink = scraper(url_link = link, remove = 5)
                if hyperlink == "Error":
                    continue
                h=hyperlink.split('thumbnail_')
                h1=h[0].split('thumbnails/')
                h2=h[-1]
                hyperlink="https://realbooru.com//images/"+h1[-1]+h2
                hp=hyperlink.split('.')
                hp[-1]='gif'
                hyperlink=""
                for i in hp:         
                    if hp.index(i)!=2:
                        hyperlink += i+'.'
                    else:
                        hyperlink += i

                await ctx.send(hyperlink)
        else:
            await ctx.send("You can only use this command in NSFW channels!")


bots.add_cog(help(bots))
bots.add_cog(sexting(bots))
bots.add_cog(Media(bots))
bots.add_cog(porn(bots))
bots.run(TOKEN)
