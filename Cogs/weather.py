import requests
import json
from pymorphy2 import MorphAnalyzer
from discord.ext import commands as cm
from settings import *

owm_id = "376c66c5e92a9637fc90d4374b315b6e"

word_analyzer = MorphAnalyzer(lang="ru")

class DbDm(cm.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cm.command(aliases=["погода"])
    async def weather(self, ctx, arg=None):
        if ctx.channel.id == bot_channel_id:
            if arg == None:
                await ctx.send("Нужно место")
            else:
                await ctx.send(get_weather_info_of_city(arg))

def setup(bot):
    bot.add_cog(DbDm(bot))


def get_data_of_place(name_of_city):
    w = "https://api.openweathermap.org/data/2.5/weather?q={0}&units=metric&appid={1}" \
        "&lang=ru".format(name_of_city, owm_id)
    data = json.loads(requests.get(w).text)
    return data

def get_weather_info_of_city(name_of_city):
    word = word_analyzer.parse(name_of_city)[0]
    normal_word = word.normal_form
    loct_form_word = word.inflect({"loct"})[0]
    dict = get_data_of_place(normal_word)
    try:
        temp = round(dict["main"]["temp"])
        fells_like_temp = round(dict["main"]["feels_like"])
        description = dict["weather"][0]["description"]
    except KeyError:
        return choice("Не могу узнать погоду в этом месте")
    else:
        return f"Температура в {loct_form_word.title()} сейчас, {temp} °C. Чувствуется будто {fells_like_temp} °C. \n А ещё там {description}."
   