import discord
import os
from discord.ext import commands as cm
from sys import exit
from settings import *

intents = discord.Intents.default()
intents.members = True 
bot = cm.Bot(command_prefix=cm.when_mentioned_or("/"), intents=intents)
bot.load_extension("Cogs.DbDm")
bot.load_extension("Cogs.weather")

cogs = list()
for cog in os.listdir("Cogs"):
    if cog.endswith(".py"):
        cogs.append(cog[:-3])

@bot.event
async def on_ready():
    print("Discord bot is working...")
    loaded_cogs = list()
    for cog in bot.extensions:
        loaded_cogs.append(cog.split(".")[1])
    print(f"loaded cogs: {', '.join(loaded_cogs)}")
    print(f"available cogs: {', '.join(cogs)}")

@bot.command()
async def load_cog(ctx, extension):
    if ctx.author.id == admin_id:
        bot.load_extension(f"Cogs.{extension}")
        await ctx.send("Cog loaded")
    else:
        await ctx.send(bruh_message)

@bot.command()
async def unload_cog(ctx, extension):
    if ctx.author.id == admin_id:
        bot.unload_extension(f"Cogs.{extension}")
        await ctx.send("Cog unloaded")
    else:
        await ctx.send(bruh_message)

@bot.command()
async def reload_cog(ctx, extension):
    if ctx.author.id == admin_id:
        bot.unload_extension(f"Cogs.{extension}")
        bot.load_extension(f"Cogs.{extension}")
        await ctx.send("Cog reloaded")
    else:
        await ctx.send(bruh_message)

@bot.command()
async def load_cogs(ctx):
    if ctx.author.id == admin_id:
        for extension in cogs:
            bot.load_extension(f"Cogs.{extension}")
            await ctx.send(f"{extension} loaded")
        await ctx.send("Cogs loaded")
    else:
        await ctx.send(bruh_message)

@bot.command()
async def reload_cogs(ctx):
    if ctx.author.id == admin_id:
        for extension in cogs:
            bot.unload_extension(f"Cogs.{extension}")
            bot.load_extension(f"Cogs.{extension}")
            await ctx.send(f"{extension} reloaded")
        await ctx.send("Cogs reloaded")
    else:
        await ctx.send(bruh_message)

bot.run(token)
