from datetime import datetime
from multiprocessing import Process, freeze_support
import asyncio
import pendulum
import Client
pst = pendulum.timezone("America/Los_Angeles")

client = Client.get_client()
user = 181577041982783491
gChannel = 925209208394240043

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

if __name__ == "main":
    freeze_support()
    p = Process(target=sched_auto_message)
    p.start()