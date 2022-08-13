from http import client
#import discord  
import pandas as pd 
import hikari
import datetime
import time
import asyncio
import lightbulb
from lightbulb.ext import tasks

df=pd.read_excel('/Users/apple/Desktop/Menu-Bot/bot/new_menu.xlsx') 

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

TOKEN = "OTY2NTAzMDM1Mzk0MTk5NTgy.GSdij5.5GL8Ln3A4PyyZoFTUXjiLyZ8VTwK6zn6NR0QE4"
menu = processEXCEL(df) 
DAY = datetime.datetime.today().strftime('%A')
# bot = hikari.GatewayBot(TOKEN)
bot = lightbulb.BotApp(TOKEN)
tasks.load(bot)
channel_id = "977533348278841356"

@bot.listen()
async def on_message(event: hikari.MessageCreateEvent) -> None:
    """Listen for messages being created."""
    if not event.is_human:
        # Do not respond to bots or webhooks!
        return

    HOUR = (datetime.datetime.now().hour)*100 + (datetime.datetime.now().minute)
    # if event.content=="!tag":
    #    await bot.rest.create_message(channel_id,"@everyone")

    if event.content == "!food":
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
        await bot.rest.create_message(channel_id, answer+"@everyone")

    elif(event.content[0] == "!"):
        MEAL = (event.content)[1:].upper()
        if(MEAL=="BREAKFAST" or MEAL=="LUNCH" or MEAL=="DINNER" or MEAL=="SNACKS"):
            answer = ""
            for item in menu[ days[DAY] ][meals[MEAL]]:
                answer = answer +  item+ "\n"
            await bot.rest.create_message(channel_id,answer+"<@everyone>")
        else:
            await bot.rest.create_message(channel_id,"Did you ping me?! I don't understand the command tho.")


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
    await bot.rest.create_message(channel_id, f'** {MEAL} **\n```  {MakeString(menu[ days[DAY] ][meals[MEAL]])} \n```\n <@everyone>' )

@tasks.task(tasks.CronTrigger('30 12 * * *'), auto_start=True)
async def Lunch():
    HOUR = (datetime.datetime.now().hour)*100 + (datetime.datetime.now().minute)

    # if HOUR <= 1230 and HOUR >= 1200:
    MEAL = "LUNCH"
    await bot.rest.create_message(channel_id, f'** {MEAL} **\n```  {MakeString(menu[ days[DAY] ][meals[MEAL]])} ```\n <@everyone>' )

@tasks.task(tasks.CronTrigger('0 16 * * *'), auto_start=True)
async def Lunch():
    HOUR = (datetime.datetime.now().hour)*100 + (datetime.datetime.now().minute)

    # if HOUR <= 1600 and HOUR >= 1530:
    MEAL = "SNACKS"
    await bot.rest.create_message(channel_id, f'** {MEAL} **\n```  {MakeString(menu[ days[DAY] ][meals[MEAL]])} ```\n <@everyone>' )

@tasks.task(tasks.CronTrigger('0 19 * * *'), auto_start=True)
async def Lunch():
    HOUR = (datetime.datetime.now().hour)*100 + (datetime.datetime.now().minute)
    # if HOUR <= 1900 and HOUR >= 1830:
    MEAL = "DINNER"
    await bot.rest.create_message(channel_id, f'** {MEAL} **\n```  {MakeString(menu[ days[DAY] ][meals[MEAL]])} ```\n <@everyone>' )

# scheduler.start() 


bot.run() 
#git functioning
