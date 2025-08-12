import discord
from discord.ui import Button, View
import requests
from bs4 import BeautifulSoup
from random import randint
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()








def parse_recent(all = []):
        url = "https://animekai.to/home"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        r = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(r.content,'html.parser')
        divs = soup.find_all("div", {"class":"aitem"})
        for div in divs:
                link = "https://animekai.to"+div.find("a",{"class":"poster"}).get('href')
                title = div.find("a",{"class":"title"}).get("title")
                img = div.find("a",{"class":"poster"}).img.get("data-src")
                latest_episode = link.split("#ep=")[1]
                all.append([link, title, img, latest_episode])
        return all


def parse_random(all = []):
        url = "https://animekai.to/recent?page="+str(randint(1,420))
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        r = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(r.content,'html.parser')
        divs = soup.find_all("div", {"class":"aitem"})
        for div in divs:
                link = "https://animekai.to"+div.find("a",{"class":"poster"}).get('href')
                title = div.find("a",{"class":"title"}).get("title")
                img = div.find("a",{"class":"poster"}).img.get("data-src")
                all.append([link, title, img])
        return all

bot = discord.Bot(debug_guilds=[661598033842143234])

@bot.event
async def on_ready():
    print("Bot is ready")

    

class AnimeView(View):
    def __init__(self, anime_list, is_random=False):
        super().__init__(timeout=None)
        self.anime_list = anime_list
        self.current_index = 0
        self.is_random = is_random
        self.update_buttons()

    def update_buttons(self):
        self.children[0].disabled = self.current_index == 0
        self.children[1].disabled = self.current_index == len(self.anime_list) - 1

    async def update_embed(self, interaction):
        self.update_buttons()
        anime = self.anime_list[self.current_index]
        if self.is_random:
            description = f"link: {anime[0]}"
        else:
            description = f"latest episode: {anime[3]}\nlink: {anime[0]}"
        embed = discord.Embed(color=0xB00B69, title=anime[1], description=description)
        embed.set_image(url=anime[2])
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Previous", style=discord.ButtonStyle.blurple)
    async def previous_button(self, button: Button, interaction: discord.Interaction):
        self.current_index -= 1
        await self.update_embed(interaction)

    @discord.ui.button(label="Next", style=discord.ButtonStyle.blurple)
    async def next_button(self, button: Button, interaction: discord.Interaction):
        self.current_index += 1
        await self.update_embed(interaction)

@bot.slash_command(name = "new", description = "Shows 12 anime from latest updates")
async def new(ctx):
    a=[]
    parse_recent(a)
    view = AnimeView(a)
    anime = view.anime_list[view.current_index]
    embed = discord.Embed(color = 0xB00B69, title = anime[1], description="Latest episode: "+anime[3]+"\n"+"link: "+anime[0])
    embed.set_image(url = anime[2])
    await ctx.respond(embed=embed, view=view)


@bot.slash_command(name = "random", description = "Shows random anime(s)")
@discord.commands.option(
    "amount",
    description="Enter amount of anime titles to show.",
    required=False,
    type=int,
    min_value=1,
    max_value=30
)
async def random(ctx, amount: int = 1):
    a=[]
    parse_random(a)
    
    if amount > len(a):
        amount = len(a)

    anime_selection = [a[randint(0, len(a)-1)] for _ in range(amount)]

    view = AnimeView(anime_selection, is_random=True)
    anime = view.anime_list[view.current_index]
    embed = discord.Embed(color = 0xB00B69, title = anime[1], description="link: "+anime[0])
    embed.set_image(url = anime[2])
    await ctx.respond(embed=embed, view=view)


bot.run(os.getenv('TOKEN'))
