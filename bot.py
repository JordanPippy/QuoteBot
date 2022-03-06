# bot.py
import os

import discord
from dotenv import load_dotenv
import asyncio
import datetime
from datetime import time
import random
from discord.ext import commands
from asyncSleep import Sleep
#from datetime import time, date

client = commands.Bot(command_prefix='>')

wait_amount = "0800"
light = Sleep()
interrupted = False
luck_protection_list = []
luck_protection_threshold = 10

@client.command()
async def quote(ctx):
    await sendRandomQuote()
    await ctx.messagemessage.add_reaction(":japanese_goblin:")

@client.command()
async def usage(ctx):
    message = '''
```Commands:
>usage               -     get help with commands
>quote               -     get a random quote
>set_time HHMM       -     sets the time (AM/PM) to send a quote 
                           SHOULD BE LESS THAN 12 
                           (for noon/midnight use 0000)
>time_until_quote    -     get time before next quote
>get_time            -     get current quote timestamp
    ```'''
    await client.get_channel(GENERAL_ID).send(message)

@client.command()
async def set_time(ctx, arg1):
    global wait_amount, interrupted
    wait_amount = str(arg1)
    light.cancel_all()
    interrupted = True
    await client.get_channel(GENERAL_ID).send("Quote set for " + wait_amount)

@client.command()
async def get_time(ctx):
    await client.get_channel(GENERAL_ID).send(str(wait_amount))

@client.command()
async def time_until_quote(ctx):
    seconds = wait_time()

    hours = int(int(seconds) / (60 * 60))
    seconds -= int((int(hours) * 60 * 60))

    minutes = int(int(seconds) / 60)
    seconds -= int((int(minutes) * 60))
    await client.get_channel(GENERAL_ID).send(f"{hours} hours {minutes} minutes {seconds} seconds")

@client.command()
async def number_of_quotes(ctx):
    messages = await get_messages()
    await client.get_channel(GENERAL_ID).send(len(messages))

@client.command()
async def luck_protection(ctx):
    await client.get_channel(GENERAL_ID).send(luck_protection_list)



def wait_time():
    global wait_amount
    hours = int(wait_amount[0] + wait_amount[1])
    minutes = int(wait_amount[2] + wait_amount[3])

    current_time = datetime.datetime.now().time()
    morning = time(hour=hours, minute=minutes, second=0)
    evening = time(hour=hours+12, minute=minutes, second=0)

    date = datetime.date(1, 1, 1)
    morning_dt = datetime.datetime.combine(date, morning)
    evening_dt = datetime.datetime.combine(date, evening)
    current_dt = datetime.datetime.combine(date, current_time)

    morning_time = morning_dt - current_dt
    evening_time = evening_dt - current_dt
    #print("waiting:", min(morning_time.seconds, evening_time.seconds))
    return min(morning_time.seconds, evening_time.seconds)

async def run():
    global interrupted
    while (True):
        await light.sleep(wait_time())
        if (interrupted):
            interrupted = False
            continue
        await sendRandomQuote()
        await asyncio.sleep(2)

async def sendRandomQuote():
    global luck_protection_list
    messages = await get_messages()
    message = random.choice(messages).content

    if (len(luck_protection_list) < luck_protection_threshold and message not in luck_protection_list):
        luck_protection_list.append(message)
    else:
        while (message in luck_protection_list):
            message = random.choice(messages).content
        luck_protection_list.pop(0)
        luck_protection_list.append(message)

    await client.get_channel(GENERAL_ID).send(message)

async def get_messages():
    return await client.get_channel(QUOTES_ID).history(limit=1000).flatten()

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
QUOTES_ID = int(os.getenv('QUOTES_ID'))
GENERAL_ID = int(os.getenv('GENERAL_ID'))

#client = discord.Client()



@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    print("Quote:", QUOTES_ID)
    print("General:,", GENERAL_ID)
    await run()


if __name__ == "__main__":
    client.run(TOKEN)