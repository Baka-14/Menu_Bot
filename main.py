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

import gspread as gs


def processEXCEL():
    gc = gs.service_account(filename='service_account.json')
    sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1h7k1JOX2zefqNP64izUIwwvmyofxw_PzO97c11YHUt0/edit?usp=sharing')

    ws = sh.worksheet('Table 1')
    df = pd.DataFrame(ws.get_all_records())

    # df.drop(df.index[0], inplace = True)
    days_index = []
    cnt= 0
    for i in df['Day']:
        if(i!=""):
            days_index.append(cnt)
        cnt+=1
    days_index.append(df.index[-1])

    print(days_index)


    menu = {}
    for day in range(len(days_index)-1):
        roju = []
        for meal in df.columns[1:]:
            puta= []
            for food in df[meal].iloc[days_index[day]:days_index[day+1]]:
                if(food!=""):
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

menu = processEXCEL() 
DAY = datetime.datetime.today().strftime('%A')
TOKEN=os.getenv("TOKEN")
# bot = hikari.GatewayBot(TOKEN)
bot = lightbulb.BotApp(TOKEN)
tasks.load(bot)
channel_id = "952512991717384303"

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
    await ctx.respond(answer)

@bot.command
@lightbulb.option("menu","choose the menu for today's-",required=True,choices=["BREAKFAST","LUNCH","SNACKS","DINNER"])
@lightbulb.command("today-menu", "today-menu")
@lightbulb.implements(lightbulb.SlashCommand)
async def todaymenu(ctx: lightbulb.Context) -> None:
    MEAL=ctx.options.menu
    answer = MEAL+"```\n"
    for item in menu[ days[DAY] ][meals[MEAL]]:
        answer = answer +  item+ "\n"
    answer+= "```"
    await ctx.respond(answer,flags=hikari.MessageFlag.EPHEMERAL)



@bot.command
@lightbulb.option("menu","choose the menu you want",required=True,choices=["BREAKFAST","LUNCH","SNACKS","DINNER"])
@lightbulb.option("day","choose the day",required=True,choices=["MONDAY","TUESDAY","WEDNESDAY","THURSDAY","FRIDAY","SATURDAY","SUNDAY"])
@lightbulb.command("menu", "menu")
@lightbulb.implements(lightbulb.SlashCommand)
async def funcmenu(ctx: lightbulb.Context) -> None:
    DAY=ctx.options.day
    MEAL=ctx.options.menu
    answer = DAY+"-"+MEAL+"```\n"
    for item in menu[ days[DAY] ][meals[MEAL]]: 
        answer = answer +  item+ "\n"
    answer+= "```"
    await ctx.respond(answer,flags=hikari.MessageFlag.EPHEMERAL)

@bot.command
@lightbulb.command("refresh","call this command to change menu")
@lightbulb.implements(lightbulb.SlashCommand)
async def funcmenu(ctx: lightbulb.Context) -> None:
    menu = processEXCEL() 
    await ctx.respond("Done",flags=hikari.MessageFlag.EPHEMERAL)


def MakeString(lis):
    ans  = ""
    for i in lis:
        ans += i + "\n"
    return ans 

@tasks.task(tasks.CronTrigger('30 1 * * *'), auto_start=True) #7am ist
async def BreakFast():
    HOUR = (datetime.datetime.now().hour)*100 + (datetime.datetime.now().minute)
    # print(HOUR)
    # if HOUR <= 700 and HOUR >= 300:
    MEAL = "BREAKFAST"
    await bot.rest.create_message(channel_id, f'** {MEAL} **\n```  {MakeString(menu[ days[DAY] ][meals[MEAL]])} \n```\n <@everyone>',mentions_everyone=True )

@tasks.task(tasks.CronTrigger('30 6 * * *'), auto_start=True)#12pm ist
async def Lunch():
    HOUR = (datetime.datetime.now().hour)*100 + (datetime.datetime.now().minute)

    # if HOUR <= 1230 and HOUR >= 1200:
    MEAL = "LUNCH"
    await bot.rest.create_message(channel_id, f'** {MEAL} **\n```  {MakeString(menu[ days[DAY] ][meals[MEAL]])} ```\n <@everyone>',mentions_everyone=True )

@tasks.task(tasks.CronTrigger('30 10 * * *'), auto_start=True)#4pm ist
async def Snacks():
    HOUR = (datetime.datetime.now().hour)*100 + (datetime.datetime.now().minute)

    # if HOUR <= 1600 and HOUR >= 1530:
    MEAL = "SNACKS"
    await bot.rest.create_message(channel_id, f'** {MEAL} **\n```  {MakeString(menu[ days[DAY] ][meals[MEAL]])} ```\n <@everyone>',mentions_everyone=True)

@tasks.task(tasks.CronTrigger('30 13 * * *'), auto_start=True)#7pm ist
async def Dinner():
    HOUR = (datetime.datetime.now().hour)*100 + (datetime.datetime.now().minute)
    # if HOUR <= 1900 and HOUR >= 1830:
    MEAL = "DINNER"
    await bot.rest.create_message(channel_id, f'** {MEAL} **\n```  {MakeString(menu[ days[DAY] ][meals[MEAL]])} ```\n @everyone',mentions_everyone=True)



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


