import discord
from discord.ext import commands
from config import settings
import requests
from bs4 import BeautifulSoup
from faker import Factory
from random import randint
import asyncio

a=[]
fake = Factory.create()

def parse():

        url = f"https://animego.org/anime?sort=a.createdAt&direction=desc&type=animes&page={randint(1,97)}" #96
        r = requests.get(url=url)
        soup = BeautifulSoup(r.content,'html.parser')
        divs = soup.findAll("div", {"class":"animes-list-item media"})
        for div in divs:
            link = div.find("a",{"class":"d-block"}).get('href')
            title = div.find("div",{"class":"h5 font-weight-normal mb-1"}).text
            year = div.find("span",{"class":"anime-year mb-2"}).find('a',{"class":"text-link-gray text-underline"}).text
            img = div.find("div",{"class":"anime-list-lazy lazy"}).get('data-original')
            sd = div.find("div",{"class":"description d-none d-sm-block"}).text
            all = []
            all.append([link, title, year, img, sd])
        return all


async def send_anime(channel_id: int):
    channel = bot.get_channel(channel_id)
    a=parse()
    p=randint(0,len(a)-1)
    embed = discord.Embed(color = 0xB00B69, title = a[p][1], description=a[p][2]+f" года выпуска\n"+a[p][4]+f'\n'+"ссылка: "+a[p][0])
    embed.set_image(url = a[p][3]) 
    await channel.send(embed=embed)


bot = commands.Bot(command_prefix = settings['prefix'])

@bot.event
async def on_ready():
    print("start hey")
    while True:
        asyncio.run_coroutine_threadsafe(send_anime(969655683156959322), bot.loop)
        await asyncio.sleep(300)
    

@bot.command()
async def r(ctx):
    
    a=parse()
    p=randint(0,len(a)-1)
    embed = discord.Embed(color = 0xB00B69, title = a[p][1], description=a[p][2]+f" года выпуска\n"+a[p][4]+f'\n'+"ссылка: "+a[p][0])
    embed.set_image(url = a[p][3]) 
    await ctx.reply(embed = embed) 



bot.run(settings['token'])
