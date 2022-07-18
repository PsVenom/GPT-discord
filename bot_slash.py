#Importing Modules
import interactions
import random
import os
from dotenv import load_dotenv

#Importing useful functions from main.py
from main import scraper

#Declaring token variable for discord bot
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

#Initialise bot object
bot=interactions.Client(token=TOKEN)

#Help Command
@bot.command(name = "help", description = "displays a help message containing instructions about bot usage.")
async def help_slash(ctx: interactions.CommandContext):

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
        embed = interactions.Embed(title=title, description=description, color=z )
        embed.set_image(url='https://imgur.com/Mzukcha.jpg')
        await ctx.send(embeds=[embed])

#random doujin command
@bot.command(name="sauce", description= "sends a random curated doujin link from nhentai")
async def sauce_slash(ctx: interactions.CommandContext):

        file = open('codes.csv', 'r').read()
        a = list(file.split(", "))
        await ctx.send("https://nhentai.net/g/"+ a[random.randint(0, len(a)+1)])

#random porn gifs command
@bot.command(name='rlporn', description= "sends a random porn gif from realbooru")
async def porn_slash(ctx: interactions.CommandContext):

        hyperlink = scraper(url_link = 'https://realbooru.com/index.php?page=post&s=list&tags=gif+', remove = 5)

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

bot.start()
