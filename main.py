from http import client
#import discord  
import os
from tokenize import Token
import aiohttp
import pandas as pd 
import hikari
import datetime
import time
import asyncio
import lightbulb
from lightbulb.ext import tasks
from dotenv import load_dotenv
load_dotenv()


df=pd.read_excel('/home/anakin513/Desktop/Menu_Bot/new_menu.xlsx') 

def processEXCEL(df):
    df.drop(df.index[0], inplace = True)
    days_index = []
    cnt= 0
    for i in df['Day']:
        if(not pd.isnull(i)):
            days_index.append(cnt)
        cnt+=1
    days_index.append(df.index[-1])

    menu = {}
    for day in range(len(days_index)-1):
        roju = []
        for meal in df.columns[1:]:
            puta= []
            for food in df[meal].iloc[days_index[day]:days_index[day+1]]:
                if(not pd.isnull(food)):
                    puta.append(food)
            roju.append(puta)
        menu[day] = roju
    return menu

days={
    "Monday": 0,
    "Tuesday": 1,
    "Wednesday": 2,
    "Thursday": 3,
    "Friday": 4,
    "Saturday": 5,
    "Sunday": 6,
}

meals={
    "BREAKFAST": 0,
    "LUNCH": 1,
    "DINNER": 2,
    "SNACKS": 3,
}

menu = processEXCEL(df) 
DAY = datetime.datetime.today().strftime('%A')
TOKEN=os.getenv("TOKEN")
# bot = hikari.GatewayBot(TOKEN)
bot = lightbulb.BotApp(TOKEN)
tasks.load(bot)
channel_id = "952512991717384303"

@bot.listen()
async def on_message(event: hikari.MessageCreateEvent) -> None:
    """Listen for messages being created."""
    if not event.is_human:
        # Do not respond to bots or webhooks!
        return

    HOUR = (datetime.datetime.now().hour)*100 + (datetime.datetime.now().minute)
    # if event.content=="!tag":
    #    await bot.rest.create_message(channel_id,"@everyone")

    if event.content=="!ping":
        await bot.rest.create_message(channel_id,"ping")

    elif event.content == "!food":
        MEAL = "BREAKFAST"
        if HOUR < 951 and HOUR > 1450:
            MEAL = "LUNCH"
        elif HOUR < 1451 and HOUR > 1805:
            MEAL = "SNACKS"
        elif HOUR < 1806 and HOUR > 2359:
            MEAL = "DINNER"
        answer = "```\n"
        for item in menu[ days[DAY] ][meals[MEAL]]:
            answer = answer +  item+ "\n"
        answer+= "```"
        await bot.rest.create_message(channel_id,answer+"@everyone",mentions_everyone=True)

    elif(event.content[0] == "!"):
        MEAL = (event.content)[1:].upper()
        if(MEAL=="BREAKFAST" or MEAL=="LUNCH" or MEAL=="DINNER" or MEAL=="SNACKS"):
            answer = ""
            for item in menu[ days[DAY] ][meals[MEAL]]:
                answer = answer +  item+ "\n"
            await bot.rest.create_message(channel_id,answer+"@everyone",mentions_everyone=True)
        else:
            await bot.rest.create_message(channel_id,"Did you ping me?! I don't understand the command tho.")


@bot.command
@lightbulb.command("ping", description="Whether the bot is working")
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx: lightbulb.Context) -> None:
    await ctx.respond(f"Pong! Latency: {bot.heartbeat_latency*1000:.2f}ms")


@bot.command
@lightbulb.command("food", description="returns menu for the next break")
@lightbulb.implements(lightbulb.SlashCommand)
async def food(ctx: lightbulb.Context) -> None:
    HOUR = (datetime.datetime.now().hour)*100 + (datetime.datetime.now().minute)
    MEAL = "BREAKFAST"
    if HOUR < 951 and HOUR > 1450:
        MEAL = "LUNCH"
    elif HOUR < 1451 and HOUR > 1805:
        MEAL = "SNACKS"
    elif HOUR < 1806 and HOUR > 2359:
        MEAL = "DINNER"
    answer = MEAL+"```\n"
    for item in menu[ days[DAY] ][meals[MEAL]]:
        answer = answer +  item+ "\n"
    answer+= "```"
    await ctx.respond(answer,mentions_everyone=True)

@bot.command
@lightbulb.option("menu","choose the menu",required=True,choices=["BREAKFAST","LUNCH","SNACKS","DINNER"])
@lightbulb.command("menu", "menu")
@lightbulb.implements(lightbulb.SlashCommand)
async def funcmenu(ctx: lightbulb.Context) -> None:
    MEAL=ctx.options.menu
    answer = MEAL+"```\n"
    for item in menu[ days[DAY] ][meals[MEAL]]:
        answer = answer +  item+ "\n"
    answer+= "```"
    await ctx.respond(answer,mentions_everyone=True)


# @tasks.task(tasks.CronTrigger('0 7 * * *'), auto_start=True)
# async def everyday():
#     print("HEllo")
#     await  bot.rest.create_message(channel_id,"hello") 
# everyday.start()

def MakeString(lis):
    ans  = ""
    for i in lis:
        ans += i + "\n"
    return ans 

@tasks.task(tasks.CronTrigger('* 3 * * *'), auto_start=True)
async def BreakFast():
    HOUR = (datetime.datetime.now().hour)*100 + (datetime.datetime.now().minute)
    # print(HOUR)
    # if HOUR <= 700 and HOUR >= 300:
    MEAL = "BREAKFAST"
    await bot.rest.create_message(channel_id, f'** {MEAL} **\n```  {MakeString(menu[ days[DAY] ][meals[MEAL]])} \n```\n <@everyone>',mentions_everyone=True )

@tasks.task(tasks.CronTrigger('30 12 * * *'), auto_start=True)
async def Lunch():
    HOUR = (datetime.datetime.now().hour)*100 + (datetime.datetime.now().minute)

    # if HOUR <= 1230 and HOUR >= 1200:
    MEAL = "LUNCH"
    await bot.rest.create_message(channel_id, f'** {MEAL} **\n```  {MakeString(menu[ days[DAY] ][meals[MEAL]])} ```\n <@everyone>',mentions_everyone=True )

@tasks.task(tasks.CronTrigger('0 16 * * *'), auto_start=True)
async def Lunch():
    HOUR = (datetime.datetime.now().hour)*100 + (datetime.datetime.now().minute)

    # if HOUR <= 1600 and HOUR >= 1530:
    MEAL = "SNACKS"
    await bot.rest.create_message(channel_id, f'** {MEAL} **\n```  {MakeString(menu[ days[DAY] ][meals[MEAL]])} ```\n <@everyone>',mentions_everyone=True)

@tasks.task(tasks.CronTrigger('0 19 * * *'), auto_start=True)
async def Lunch():
    HOUR = (datetime.datetime.now().hour)*100 + (datetime.datetime.now().minute)
    # if HOUR <= 1900 and HOUR >= 1830:
    MEAL = "DINNER"
    await bot.rest.create_message(channel_id, f'** {MEAL} **\n```  {MakeString(menu[ days[DAY] ][meals[MEAL]])} ```\n @everyone',mentions_everyone=True)

# scheduler.start() 


@bot.listen()
async def on_starting(event: hikari.StartingEvent) -> None:
    bot.d.aio_session = aiohttp.ClientSession()

@bot.listen()
async def on_stopping(event: hikari.StoppingEvent) -> None:
    await bot.d.aio_session.close()



if __name__ == "__main__":
    if os.name != "nt":
        import uvloop

        uvloop.install()

    bot.run()


