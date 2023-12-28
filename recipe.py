import requests
import html
import discord
import json
import random

# api docs: https://developer.edamam.com/edamam-docs-recipe-api

AppID = "98c5550d"
AppKey = "c50b513d9f093207770b693c7ab80ce9"

def gerar_emoji():
    emojis = ['🧀','🍖','🍗','🥩','🥓','🍔','🍟','🍕','🌭','🥪','🌮','🌯','🥙','🧆','🥚','🍳','🥘','🍲','🥣','🥗','🍿','🧈','🧂','🥫','🍝']
    return random.choice(emojis)

async def sendApiByCuisine(cuisine: str):
    link = f"https://api.edamam.com/api/recipes/v2?type=public&app_id={AppID}&app_key={AppKey}&cuisineType={cuisine}"
    print(link)
    response = requests.get(link)
    page = html.unescape(response.text)
    data = json.loads(str(page))
    embed = discord.Embed(
        title=f"Search results: '{cuisine}'"
        )
    for recipe in data['hits']:
        emoji = gerar_emoji()
        embed.add_field(
            name=f"{emoji} {recipe['recipe']['label']}",
            value=str(recipe['recipe']['uri']).replace("http://www.edamam.com/ontologies/edamam.owl#recipe_", "")
        )
    if data['count'] == 0:
        embed.description = "Nothing to see here, try using: `American, Asian, British, Caribbean, Central Europe, French, Indian, Italian, Japanese, Kosher, Mediterranean, Mexican, Middle Eastern, Nordic, South American` or `South East Asian`"
    else:
        embed.description = "Here are the recipes with their ID to search using `/recipe id_recipe`:"
    embed.set_author(name="YakiBot", icon_url="https://cdn.discordapp.com/attachments/1060885579992141954/1189524313225830430/Yakibot.jpg?ex=659e79d8&is=658c04d8&hm=0fd8ed772aac1edd0b15bb163041d94429bb3e9337cbb0f7c25367652f998196&")
    embed.set_footer(text=f"Over {data['count']} results. P.S.: The emojis aren't actually the food ;P")
    embed.color = discord.Color.green()
    return embed

async def sendApiByQuery(query: str):
    link = f"https://api.edamam.com/api/recipes/v2?type=public&app_id={AppID}&app_key={AppKey}&q={query}"
    response = requests.get(link)
    page = html.unescape(response.text)
    data = json.loads(str(page))
    embed = discord.Embed(
        title=f"Search results: '{query}'"
        )
    for recipe in data['hits']:
        emoji = gerar_emoji()
        embed.add_field(
            name=f"{emoji} {recipe['recipe']['label']}",
            value=str(recipe['recipe']['uri']).replace("http://www.edamam.com/ontologies/edamam.owl#recipe_", "")
        )
    if data['count'] == 0:
        embed.description = f"No results for '{query}'. Nothing to see here, try using other query"
    else:
        embed.description = "Here are the recipes with their ID to search using `/recipe id_recipe`:"
    embed.set_author(name="YakiBot", icon_url="https://cdn.discordapp.com/attachments/1060885579992141954/1189524313225830430/Yakibot.jpg?ex=659e79d8&is=658c04d8&hm=0fd8ed772aac1edd0b15bb163041d94429bb3e9337cbb0f7c25367652f998196&")
    embed.set_footer(text=f"Over {data['count']} results. P.S.: The emojis aren't actually the food ;P")
    embed.color = discord.Color.green()
    return embed
    
def fetchIngredients(ingredients: dict):
    list = ""
    for ingredient in ingredients:
        formattedweight = "{:.2f}".format(ingredient['weight'])
        list += f"- {ingredient['text']} ({formattedweight}g)\n"
    return list
    
def fetchInstructions(instructions: dict):
    list = ""
    for instruction in instructions:
        list += f"- {instruction}\n"
    return list
    
async def fetchRecipeById(id_recipe: str):
    link = f"https://api.edamam.com/api/recipes/v2/{id_recipe}?type=public&app_id={AppID}&app_key={AppKey}"
    response = requests.get(link)
    print(link)
    page = html.unescape(response.text)
    data = json.loads(str(page))
    emoji = gerar_emoji()
    embed = discord.Embed() 
    if len(data) == 1:
        embed.title = f"❓ Error: {data[0]['errorCode']}"  
        embed.description = data[0]['message'] + " 😢"
        embed.color = discord.Color.red()
    else:
        embed.title=f"{emoji} {data['recipe']['label']}"
        ingredients = fetchIngredients(data['recipe']['ingredients'])
        instructions = fetchInstructions(data['recipe']['instructionLines'])
        healtLabels = ""
        for label in data['recipe']['healthLabels']:
            if label == data['recipe']['healthLabels'][-1]:
                healtLabels += f" {label}."
            else:
                healtLabels += f"{label}, "
        
        embed.description = f"""Here is the recipe you wanted, seems delicious 👌
        
        **Ingredients:**
        {ingredients}
        
        **Instructions:**
        {instructions}
        
        Health Labels: _{healtLabels}_"""
        calories = "{:.2f}".format(data['recipe']['calories'])
        embed.add_field(name="Calories", value=f"{calories}cal")
        embed.add_field(name=f"From: {data['recipe']['source']}", value=f"[Click Here to see more]({data['recipe']['url']})")
        embed.set_image(url=data['recipe']['images']['REGULAR']['url'])
        embed.color = discord.Color.random()
    embed.set_author(name="YakiBot", icon_url="https://cdn.discordapp.com/attachments/1060885579992141954/1189524313225830430/Yakibot.jpg?ex=659e79d8&is=658c04d8&hm=0fd8ed772aac1edd0b15bb163041d94429bb3e9337cbb0f7c25367652f998196&")
    embed.set_footer(text=f"Thank you for using my service! P.S.: The emojis aren't actually the food ;P")
    return embed
    
async def useApiData(data: dict, query: str):
    embed = discord.Embed(
        title=f"Search results: '{query}'"
        )
    for recipe in data['hits']:
        embed.add_field(
            name=recipe['recipe']['label'],
            value=f"""Search ID: {str(recipe['recipe']['uri']).replace("http://www.edamam.com/ontologies/edamam.owl", "")}
            [Click here to see the recipe]({recipe['recipe']['url']})"""
        )
        print(recipe['recipe']['label'])
    embed.set_author(name="YakiBot", icon_url="https://cdn.discordapp.com/attachments/1060885579992141954/1189524313225830430/Yakibot.jpg?ex=659e79d8&is=658c04d8&hm=0fd8ed772aac1edd0b15bb163041d94429bb3e9337cbb0f7c25367652f998196&")
    embed.set_footer(text=f"Over {data['count']} results. P.S.: The emojis aren't actually the food ;P")
    return embed