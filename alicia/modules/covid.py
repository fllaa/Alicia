import datetime

from pyrogram import filters

from alicia import alia
from alicia.utils import AioHttp


def dot(number, thousand_separator="."):
    def reverse(string):
        string = "".join(reversed(string))
        return string

    s = reverse(str(number))
    count = 0
    result = ""
    for char in s:
        count = count + 1
        if count % 3 == 0:
            if len(s) == count:
                result = char + result
            else:
                result = thousand_separator + char + result
        else:
            result = char + result
    return result


@alia.on_message(filters.command("covid"))
async def covid(client, message):
    args = message.text.split(None, 1)
    country = ""
    if len(args) == 2:
        re_split = args[1].split()
        country = "%20".join(re_split)
    if country:
        url = f"https://disease.sh/v3/covid-19/countries/{country}?yesterday=false&twoDaysAgo=false&strict=true&allowNull=true"
    else:
        url = "https://disease.sh/v3/covid-19/all?yesterday=false&twoDaysAgo=false&allowNull=true"
        country = "World"
    case = await AioHttp().get_json(url)
    try:
        json_date = case["updated"]
    except KeyError:
        await message.reply_text("Make sure you have input correct country")
        return
    float_date = float(json_date) / 1000.0
    date = datetime.datetime.fromtimestamp(float_date).strftime("%d %b %Y %I:%M:%S %p")
    try:
        flag = case["countryInfo"]["flag"]
    except KeyError:
        flag = []
    if flag:
        text = f"**COVID-19 Statistics in** [{args[1]}]({flag})\n"
    else:
        text = f"**COVID-19 Statistics in {country} :**\n"
    text += f"Last Updated on `{date} GMT`\n\n🔼 Confirmed Cases : `{dot(case['cases'])}` | `+{dot(case['todayCases'])}`\n🔺 Active Cases : `{dot(case['active'])}`\n⚰️ Deaths : `{dot(case['deaths'])}` | `+{dot(case['todayDeaths'])}`\n💹 Recovered Cases: `{dot(case['recovered'])}` | `+{dot(case['todayRecovered'])}`\n💉 Total Tests : `{dot(case['tests'])}`\n👥 Populations : `{dot(case['population'])}`\n🌐 Source : worldometers"
    try:
        await message.reply_text(text, parse_mode="markdown")
    except Exception:
        await message.reply_text("Try again in few times, maybe API are go down")


__help__ = """
2020 are disaster year :( and now, 2021 are 2020 Season II

 × /covid <country>: Get information about COVID-19 Country Stats
 × /covid : Get information about COVID-19 World Stats
"""

__mod_name__ = "Covid"
