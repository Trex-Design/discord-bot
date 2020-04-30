import os

import discord
from dotenv import load_dotenv
from bs4 import BeautifulSoup,element
import requests
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
URL = 'https://en.wikipedia.org/wiki/Template:2019%E2%80%9320_coronavirus_pandemic_data'

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='cases')
async def scrape_cases(ctx):

    res = ''
    res += '```'

    source = requests.get(URL).text

    soup = BeautifulSoup(source,'lxml')

    table = soup.find('table',id="thetable")

    headers = []

    for elem in table.find('tr'):
        if isinstance(elem,element.NavigableString):
            pass
        else:
            headers.append(elem.text.strip())

    del headers[-1]

    rows = table.find_all('tr')[2:12]

    raw_data = []
    raw_countries = []

    for tr in rows:
        raw_countries.append(tr.find_all('a')[:-1])
        raw_data.append(tr.find_all('td'))

    countries = []

    for i in raw_countries:
        countries.append(i[0].text)

    data = []

    for row in raw_data:
        temp = []
        for td in row[:-1]:
            temp.append(td.text.strip())
        data.append(temp)

    res += "FORMAT:"

    res += '\n' + headers[0]


    for i in headers[1:]:
        res += '\t' + i

    res += '\n\n'

    for count,i in enumerate(countries,0):
        res += i

        for j in data[count]:
            res += '\t' + j
        res += '\n'

    res += '```'

    await ctx.send(res)

bot.run(TOKEN)
