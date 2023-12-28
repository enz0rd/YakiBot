import asyncio
from functools import partial
import string
from typing import Any, Optional
import discord
from discord import app_commands
from discord.enums import ButtonStyle
from discord.ui import Button
from discord.ui import View
from discord.flags import Intents
from dotenv import dotenv_values
from recipe import *

env = dotenv_values('.env')
MYTOKEN = env['MYTOKEN']

github = "[Github](https://github.com/enz0rd)"
instagram = "[Instagram](https://instagram.com/enz0rd)"
linktree = "[Linktree](https://linktr.ee/megab_07)"

class client(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.all())
        self.synced = False
        
    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True
        print(f"Entramos como {self.user}")

aclient = client()
tree = app_commands.CommandTree(aclient)

@tree.command(name='about', description='Learn more about me and what I can do for you!')
async def about(interaction: discord.Interaction):
    desc = f"""A discord bot for searching recipes around the internet.
In the palm of your hand, select between diverse categories of meals and get the exact recipe you want!
    
P.S.: If the recipe you want is **not** in the list, please contact my administrator
Powered by [EDAMAM API](https://developer.edamam.com/edamam-docs-recipe-api#/)
Author: enz0rd
Social: {github} {instagram} {linktree}"""
    embed = discord.Embed(
        title="About me!",
        description=desc,
        color=discord.Color.brand_green()
    )
    embed.set_image(url="https://media.giphy.com/media/2JjDO2aWovqo0/giphy.gif")
    embed.set_author(name="YakiBot", icon_url="https://cdn.discordapp.com/attachments/1060885579992141954/1189524313225830430/Yakibot.jpg?ex=659e79d8&is=658c04d8&hm=0fd8ed772aac1edd0b15bb163041d94429bb3e9337cbb0f7c25367652f998196&")
    embed.set_footer(text="~ YakiBot, recipes in your hand! ~")
    await interaction.response.send_message(embed=embed, ephemeral=True)

@tree.command(name='cuisinetype', description='Discover recipes from a specific cuisine type!')
async def cuisinetype(interaction: discord.Interaction, cuisine:str):
    embed = await sendApiByCuisine(cuisine.upper())
    await interaction.response.defer(ephemeral=True)
    await asyncio.sleep(1)
    await interaction.followup.send(embed=embed)

@tree.command(name='recipe', description='Retrieve detailed information about a specific recipe by its ID')
async def food(interaction: discord.Interaction, recipe_id: str):
    new_recipe_id = f"recipe_{recipe_id.translate({ord(c): None for c in string.whitespace})}"
    embed = await fetchRecipeById(new_recipe_id)
    await interaction.response.defer(ephemeral=True)
    await asyncio.sleep(1)
    await interaction.followup.send(embed=embed)
    
@tree.command(name='search', description='Find delicious recipes based on your query')
async def search(interaction: discord.Interaction, query: str):
    embed = await sendApiByQuery(query)
    await interaction.response.defer(ephemeral=True)
    await asyncio.sleep(1)
    await interaction.followup.send(embed=embed)

@tree.command(name='helpme', description='Check wich commands are available for you to use!')
async def help(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Helping you to have a delicious meal!"
    )
    embed.description = f"""Hello! I'm YakiBot, your fastest recipe bot, and these are my commands!\n
- `/about` - Learn more about me and what I can do for you!
- `/cuisinetype cuisine` - Discover recipes from a specific cuisine type
- `/recipe recipe_id` - Retrieve detailed information about a specific recipe by its ID
- `/search query` - Find delicious recipes based on your query
- `/helpme` - Check wich commands are available for you to use (the command you just used!)\n
You can count on me to make your day a little more delicious! XOXO"""
    embed.set_author(name="YakiBot", icon_url="https://cdn.discordapp.com/attachments/1060885579992141954/1189524313225830430/Yakibot.jpg?ex=659e79d8&is=658c04d8&hm=0fd8ed772aac1edd0b15bb163041d94429bb3e9337cbb0f7c25367652f998196&")
    embed.set_footer(text=f"Thank you for using my service!")
    embed.color = discord.Color.green()
    embed.set_image(url="https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExY3B2angxMHF5dmxyMWgxaHpvMXFjNG9iNjloZzNwNzBic3loYTl1ayZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/q2ePk5TyEq8da/giphy.gif")
    await interaction.response.defer(ephemeral=True)
    await asyncio.sleep(1)
    await interaction.followup.send(f"{interaction.user.mention}, just sent a message in your DM!")
    await interaction.user.send(embed=embed)
    
aclient.run(MYTOKEN)
