import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
import random

client = commands.Bot(command_prefix='.')

@client.event
async def on_ready():
    print('{0.user} is on'.format(client))
    await client.change_presence(activity= discord.Game(name='cock'))

@client.command()
async def ping(ctx):
    await ctx.send(f'{round(client.latency * 1000)}ms')


@client.command()
async def clear(ctx, amount=100):
    await ctx.channel.purge(limit=amount)
    await ctx.send("Deleted " + str(amount) + " messages.")


@client.command()
async def pfp(ctx, member: discord.Member = None):
    show_avatar = discord.Embed(
        colour=discord.Colour.green()
    )

    if member is None:
        show_avatar.set_image(url='{}'.format(ctx.author.avatar_url))
        await ctx.send(embed=show_avatar)
    else:
        show_avatar.set_image(url='{}'.format(member.avatar_url))
        await ctx.send(embed=show_avatar)


@client.command()
async def weather(ctx,*,message):
    api_address = 'http://api.openweathermap.org/data/2.5/weather?appid=624c9238faccbd31504730cffbbc3267&q=' + message + '&units=metric'
    json_data = requests.get(api_address).json()
    degrees = json_data['main']['temp']
    description = json_data['weather'][0]['description']
    city = json_data['name']
    country = json_data['sys']['country']
    await ctx.send(city + ', ' + country + '\n' + description.title() + '\n' + str(round(degrees)) + "°C")


@client.command()
async def swedish(ctx,*,message):
    API_KEY = 'trnsl.1.1.20191023T160143Z.7324a06dc7ee4fca.8bc20e1bcd07740dba19af00829016c0876f53d4'
    url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
    params = dict(key=API_KEY, text=message, lang='en-sv')
    res = requests.get(url, params=params)
    json = res.json()
    await ctx.send(json['text'][0])


@client.command()
async def english(ctx,*,message):
    API_KEY = 'trnsl.1.1.20191023T160143Z.7324a06dc7ee4fca.8bc20e1bcd07740dba19af00829016c0876f53d4'
    url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
    params = dict(key=API_KEY, text=message, lang='sv-en')
    res = requests.get(url, params=params)
    json = res.json()
    await ctx.send(json['text'][0])

@client.command()
async def time(ctx,*,city):
    URL = 'https://time.is/' + city
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ''Chrome/80.0.3987.132 Safari/537.36'}
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    time_ = soup.find('time', attrs={'id': 'clock'}).get_text()
    place = soup.find('div', attrs={'class': 'w1'}).findNext('span').get_text()

    await ctx.send("Local time in " + place + ": " + time_)

@client.command()
async def followage(ctx, channel, user):
    url = "http://beta.decapi.me/twitch/followage/" + channel + '/' + user
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ''Chrome/80.0.3987.132 Safari/537.36'}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    await ctx.send(user + " has been following " + channel + " for " + str(soup))

@client.command()
async def penis(ctx, member: discord.Member = None):
    if member is None:
        await ctx.send(f"{ctx.author}" + " has a " + str(random.randint(1, 20)) + " inch cock")
    else:
        await ctx.send(f"{ctx.author}" + member.display_name + " has a " + str(random.randint(1, 20)) + " inch cock")

@client.command()
async def userinfo(ctx, member: discord.Member=None):
    member  = member or ctx.author
    user_info = discord.Embed(colour=discord.Colour.green())

    user_info.set_footer(text=".", icon_url=member.avatar_url)

    user_info.add_field(name="Username", value=member.display_name)
    user_info.add_field(name="ID", value=member.id)
    user_info.add_field(name="Server join date", value=str(member.joined_at))
    user_info.add_field(name="Account created at", value=str(member.created_at))

    await ctx.send(embed=user_info)

@client.command()
async def spotify(ctx, user: discord.Member = None):
    user = user or ctx.author
    spoti_info = discord.Embed(color=discord.Color.purple())

    for activity in user.activities:
        if isinstance(activity, discord.Spotify):
            spoti_info.set_image(url='{}'.format(activity.album_cover_url))
            spoti_info.add_field(name="Artist", value=activity.artist)
            spoti_info.add_field(name="Song", value=activity.title)
            await ctx.send(embed=spoti_info)

@client.command()
async def exchange(ctx, amount, base_currency, target_currency):
    url = 'https://api.exchangeratesapi.io/latest?base=' + base_currency.upper() + '&symbols=' + target_currency.upper()
    answer = requests.get(url).json()['rates'][target_currency.upper()]
    await ctx.send(amount + ' ' + base_currency.upper() + ' equals ' + str(float(amount) * round(answer, 2)) + ' ' + target_currency.upper())
  
client.run('NjMyNjQwMDkzNTUwODA1MDIz.XaIWdg.15CQzosS3qKeTL2zG2GkD9olkRY')
