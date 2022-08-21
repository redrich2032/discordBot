from keep_bot_online import keep_bot_online
import requests
import json
import pendulum
import discord
from datetime import datetime
import asyncio
from discord.ext import commands
import youtube_dl
import os

pst = pendulum.timezone('America/Los_Angeles')

intents = discord.Intents.all()
client = commands.Bot(command_prefix="!", intents=intents)
gChannel = 925209208394240043
user = 181577041982783491

resultURLs = []


@client.event
async def on_ready():
    print('logged in as {0.user}'.format(client))

@client.event
async def on_member_join(member):
  gChannel = client.get_channel(925209208394240043)
  await gChannel.send(f"HELLO <@{member.id}>(MAMA) ITS ME PEANUT :). PAPA MADE ME A ROBOT SO WE CAN ALL BE IN DISCORD TOGETHER!!\n"
                        "THIS IS ONLY THE FIRST PART OF YOUR SURPRISE!! DAD TAUGHT ME A LOT MORE TRICKS AND I CANT WAIT TO SHOW THEM OFF TO YOU TOMORROW!! \nHAPPY EARLY ANIVERSARY MAMA AND PAPA!!! \n"
                        "P.S. BE SURE TO CHECK DISCORD AGAIN AT 9AM FOR A SURPRISE WINK WINK MEEEEOOOWW")

#   --- autoMessages ---
async def sched_auto_message():
    while(True):
        now = datetime.now(pst)
        currentTime = now.strftime("%H:%M:%S")
        # print(currentTime + " background")
        if(currentTime == "09:00:00"):
            await morning_message()
        await asyncio.sleep(1)

async def morning_message():
    channel = client.get_channel(gChannel)
    await client.wait_until_ready()
    await channel.send(f"MEOW...GOOD MORNING!! <@{user}> KIBBLE TIME!!\n"
    "THANK YOU FOR REMEMBERING TO CHECK DISCORD MEEOW. HAPPY ANIVERSARY!!")


#   --- sephora commands ---
sephProductName = []
sephListPrice = []
sephSalePrice = []
sephProductURL = []
sephImageURL = []
sephBaseURL = "https://sephora.com"
@client.command()
async def sephora(ctx, * , arg):
    embed = discord.Embed()
    search_seph_item(arg)
    for i in range(len(sephProductName)):
        embed.set_image(url=sephImageURL[i])
        await ctx.send(sephProductName[i] + "\n" + "OG PRICE: " + sephListPrice[i] +
                       "     SALE PRICE: " + sephSalePrice[i] + "\n" + sephProductURL[i]
                       + "\n", embed=embed)
    sephProductName.clear()
    sephListPrice.clear()
    sephSalePrice.clear()
    sephProductURL.clear()
    sephImageURL.clear()


def search_seph_item(search):
    url = "https://sephora.p.rapidapi.com/products/search"

    querystring = {"q": search, "pageSize": "60", "currentPage": "1", "sortBy": "P_BEST_SELLING:1"}

    headers = {
        'x-rapidapi-host': "sephora.p.rapidapi.com",
        'x-rapidapi-key': "d3e453e5bdmsh9d8a9ed2148dd88p10ae4bjsn0cf69fcbfeff"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    jsonData = json.loads(response.text)
    for i in range(0, 3):
        sephProductName.append(jsonData["products"][i]['displayName'])
        sephListPrice.append(jsonData["products"][i]['currentSku']['listPrice'])
        if jsonData["products"][i]['currentSku']['salePrice'] == "":
            sephSalePrice.append("NOT ON SALE!")
        else:
            sephSalePrice.append(jsonData["products"][i]['currentSku']['salePrice'])
        sephProductURL.append(sephBaseURL + jsonData["products"][i]["targetUrl"])
        sephImageURL.append(jsonData["products"][i]["image250"])


#   --- amazon commands ---
@client.command()
async def amazon(ctx, * ,arg):
    search_amaz_item(arg)
    for i in range(len(resultURLs)):
        await ctx.send(resultURLs[i])
    resultURLs.clear()


def search_amaz_item(item):
    url = "https://amazon-price1.p.rapidapi.com/search"
    querystring = {"keywords": item, "marketplace": "US"}
    headers = {
        'x-rapidapi-host': "amazon-price1.p.rapidapi.com",
        'x-rapidapi-key': "d3e453e5bdmsh9d8a9ed2148dd88p10ae4bjsn0cf69fcbfeff"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    jsonData = json.loads(response.text)
    i = 0
    for i in range(0, 3):
        resultURLs.append(jsonData[i]['detailPageURL'])


#   --- music commands ---
@client.command()
async def join(ctx):
    if ctx.author.voice is None:
        await ctx.send("Peanut isn't in a voce channel :(")
    voice_channel = ctx.author.voice.channel
    if ctx.voice_client is None:
        await voice_channel.connect()
    else:
        await ctx.voice_client.move_to(voice_channel)


@client.command()
async def sing(ctx, url: str):
    ctx.voice_client.stop()
    FFMPEG_OPT = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    YDL_OPT = {'format': "best"}
    voice = ctx.voice_client

    with youtube_dl.YoutubeDL(YDL_OPT) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']
        source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPT)
        voice.play(source)


@client.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()


@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()


@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()


@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()


keep_bot_online()
client.run(os.environ['TOKEN'])