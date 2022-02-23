# bot.py
import os

import discord
from dotenv import load_dotenv
import asyncio
import datetime
from datetime import time
import random
#from datetime import time, date


def wait_time():
    current_time = datetime.datetime.now().time()
    morning = time(hour=8, minute=0, second=0)
    evening = time(hour=20, minute=0, second=0)

    date = datetime.date(1, 1, 1)
    morning_dt = datetime.datetime.combine(date, morning)
    evening_dt = datetime.datetime.combine(date, evening)
    current_dt = datetime.datetime.combine(date, current_time)

    morning_time = morning_dt - current_dt
    evening_time = evening_dt - current_dt
    print("waiting:", min(morning_time.seconds, evening_time.seconds))
    return min(morning_time.seconds, evening_time.seconds)

async def run():
    while (True):
        await asyncio.sleep(wait_time())
        messages = await client.get_channel(QUOTES_ID).history(limit=1000).flatten()
        randomMessage = random.choice(messages).content
        await client.get_channel(GENERAL_ID).send(randomMessage)
        await asyncio.sleep(60)

async def get_messages():
    return await client.get_channel(QUOTES_ID).history(limit=200).flatten()

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
QUOTES_ID = int(os.getenv('QUOTES_ID'))
GENERAL_ID = int(os.getenv('GENERAL_ID'))

client = discord.Client()

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

client.run(TOKEN)