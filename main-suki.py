import suki

import os
import discord
from dotenv import load_dotenv
from discord.ext import tasks
import concurrent.futures
import asyncio


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = int(os.getenv('DISCORD_GUILD_ID'))

client = discord.Client(intents=discord.Intents.default())

current_food_items = []

@client.event
async def on_ready():
    global current_food_items
    print(f'{client.user} has connected to Discord!')
    current_food_items = suki.get_unavail_dishes()
    for guild in client.guilds:
        if guild.id == GUILD_ID:
            break
            
    category_name = "Project Suki"
    category = discord.utils.get(guild.categories, name=category_name)

    if not category:
        await guild.create_category(category_name)
        print("Created category"+category_name)
        category = discord.utils.get(guild.categories, name=category_name)
    else:
        print("Fine, category exists "+category_name)
        
    for important_preboot_channels in ("initialization", "additions", "removals"):
        channel = discord.utils.get(guild.text_channels, name=important_preboot_channels)
        if not channel:
            try:
                channel = await guild.create_text_channel(important_preboot_channels, category=category)
                # await channel.edit(type=discord.ChannelType.news)
                print(channel.type)
            except Exception as e:
                print(e)
                print(traceback.format_exc())
                await guild.create_text_channel(important_preboot_channels)
    await discord.utils.get(guild.text_channels, name="initialization").send("Ready!")
    myLoop.start()
    
@tasks.loop(seconds = 20) # repeat after every 10 seconds
async def myLoop():
    global current_food_items
    for guild in client.guilds:
        if guild.id == GUILD_ID:
            break
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        loop = asyncio.get_event_loop()
        futures = [

            loop.run_in_executor(
                executor, 
                suki.get_unavail_dishes
            )
            for _ in ["DO_ONCE"]
        ]
        rs2 = await asyncio.gather(*futures)
    new_food_items = rs2[0]
    print(new_food_items)
    in_stock = set(current_food_items).difference(new_food_items)
    if in_stock:
        msg_string = "Items now in stock:\n"+"\n".join(set(current_food_items).difference(new_food_items))
        print(msg_string)
        await discord.utils.get(guild.text_channels, name="additions").send(msg_string)
    out_of_stock = set(new_food_items).difference(current_food_items)
    if out_of_stock:
        msg_string = "Items now out of stock:\n"+"\n".join(set(new_food_items).difference(current_food_items))
        print(msg_string)
        await discord.utils.get(guild.text_channels, name="removals").send(msg_string)
    current_food_items = new_food_items
        
client.run(TOKEN)