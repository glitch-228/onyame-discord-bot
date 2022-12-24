import discord
from config import settings
import requests
from bs4 import BeautifulSoup
from random import randint
import asyncio








def parse(all = []):
        url = f"https://www.anime-planet.com/anime/all?page={randint(1,50)}" #49
        r = requests.get(url=url)
        soup = BeautifulSoup(r.content,'html.parser')
        divs = soup.findAll("ul", {"class":"cardDeck cardGrid"})
        for div in divs:
                link = "https://www.anime-planet.com"+div.find("a",{"class":"tooltip"}).get('href')
                title = BeautifulSoup(div.find("a",{"class":"tooltip"}).get("title"),'html.parser').find("h5",{"class":"theme-font"}).text
                year = BeautifulSoup(div.find("a",{"class":"tooltip"}).get("title"),'html.parser').find("li",{"class":"iconYear"}).text
                img = div.find("div",{"class":"crop"}).img.get("src")
                sd = BeautifulSoup(div.find("a",{"class":"tooltip"}).get("title"),'html.parser').find("p").text
                all.append([link, title, year, img, sd])
        return all


bot = discord.Bot()

@bot.event
async def on_ready():
    print("start hey")

    

@bot.slash_command(name = "r", description = "nice cock")
async def r(ctx):
    a=[]
    parse(a)
    p=randint(0,len(a)-1)
    embed = discord.Embed(color = 0xB00B69, title = a[p][1], description=a[p][2]+f" year\n"+a[p][4]+f'\n'+"link: "+a[p][0])
    embed.set_image(url = a[p][3]) 
    await ctx.respond(embed=embed) 


bot.run(settings['token'])
