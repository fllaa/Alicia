import datetime
import html
import re
import textwrap

import bs4
import jikanpy
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from alicia import alia
from alicia.utils import (
    AioHttp,
    airing_query,
    anime_query,
    character_query,
    f_time,
    manga_query,
    shorten,
    url,
    user_query,
)

info_btn = "More Information"
kaizoku_btn = "Kaizoku ☠️"
kayo_btn = "Kayo 🏴‍☠️"
prequel_btn = "⬅️ Prequel"
sequel_btn = "Sequel ➡️"
close_btn = "Close ❌"


@alia.on_message(filters.command("airing"))
async def airing(client, message):
    search_str = message.text.split(None, 1)
    if len(search_str) == 1:
        await message.reply_text(
            "Tell Anime Name :) ( /airing <anime name>)"
        )
        return
    variables = {"search": search_str[1]}
    resp = await AioHttp().post_json(
        url, json={"query": airing_query, "variables": variables}
    )
    response = resp['data']['Media']
    msg = f"**Name**: **{response['title']['romaji']}**(`{response['title']['native']}`)\n**ID**: `{response['id']}`"
    if response["nextAiringEpisode"]:
        time = response["nextAiringEpisode"]["timeUntilAiring"] * 1000
        time = f_time(time)
        msg += f"\n**Episode**: `{response['nextAiringEpisode']['episode']}`\n**Airing In**: `{time}`"
    else:
        msg += f"\n**Episode**:{response['episodes']}\n**Status**: `N/A`"
    await message.reply_text(msg, parse_mode="markdown")


@alia.on_message(filters.command("anime"))
async def anime(client, message):
    search = message.text.split(None, 1)
    if len(search) == 1:
        await message.reply_text("Format : /anime < anime name >")
        return
    else:
        search = search[1]
    variables = {"search": search}
    json = await AioHttp().post_json(
        url, json={"query": anime_query, "variables": variables}
    )
    if "errors" in json.keys():
        await message.reply_text("Anime not found")
        return
    if json:
        json = json["data"]["Media"]
        msg = f"**{json['title']['romaji']}**(`{json['title']['native']}`)\n**Type**: {json['format']}\n**Status**: {json['status']}\n**Episodes**: {json.get('episodes', 'N/A')}\n**Duration**: {json.get('duration', 'N/A')} Per Ep.\n**Score**: {json['averageScore']}\n**Genres**: `"
        for x in json["genres"]:
            msg += f"{x}, "
        msg = msg[:-2] + "`\n"
        msg += "**Studios**: `"
        for x in json["studios"]["nodes"]:
            msg += f"{x['name']}, "
        msg = msg[:-2] + "`\n"
        info = json.get("siteUrl")
        trailer = json.get("trailer", None)
        if trailer:
            trailer_id = trailer.get("id", None)
            site = trailer.get("site", None)
            if site == "youtube":
                trailer = "https://youtu.be/" + trailer_id
        description = (
            json.get("description", "N/A")
            .replace("<i>", "")
            .replace("</i>", "")
            .replace("<br>", "")
        )
        msg += shorten(description, info)
        image = f"https://img.anili.st/media/{json['id']}"
        if trailer:
            buttons = [
                [
                    InlineKeyboardButton("More Info", url=info),
                    InlineKeyboardButton("Trailer 🎬", url=trailer),
                ]
            ]
        else:
            buttons = [[InlineKeyboardButton("More Info", url=info)]]
        if image:
            try:
                await message.reply_photo(
                    photo=image,
                    caption=msg,
                    parse_mode="markdown",
                    reply_markup=InlineKeyboardMarkup(buttons),
                )
            except BaseException:
                msg += f" [〽️]({image})"
                await message.reply_text(
                    msg,
                    parse_mode="markdown",
                    reply_markup=InlineKeyboardMarkup(buttons),
                )
        else:
            await message.reply_text(
                msg,
                parse_mode="markdown",
                reply_markup=InlineKeyboardMarkup(buttons),
            )


@alia.on_message(filters.command("character"))
async def character(client, message):
    search = message.text.split(None, 1)
    if len(search) == 1:
        await message.reply_text("Format : /character < character name >")
        return
    search = search[1]
    variables = {"query": search}
    json = await AioHttp().post_json(
        url, json={"query": character_query, "variables": variables}
    )
    if "errors" in json.keys():
        await message.reply_text("Character not found")
        return
    if json:
        json = json["data"]["Character"]
        msg = f"**{json.get('name').get('full')}**(`{json.get('name').get('native')}`)\n"
        description = f"{json['description']}"
        site_url = json.get("siteUrl")
        msg += shorten(description, site_url)
        image = json.get("image", None)
        button = [[InlineKeyboardButton("More Info", url=site_url)]]
        if image:
            image = image.get("large")
            await message.reply_photo(
                photo=image,
                caption=msg,
                parse_mode="markdown",
                reply_markup=InlineKeyboardMarkup(button),
            )
        else:
            await message.reply_text(
                msg,
                parse_mode="markdown",
                reply_markup=InlineKeyboardMarkup(button),
            )


@alia.on_message(filters.command("manga"))
async def manga(client, message):
    search = message.text.split(None, 1)
    if len(search) == 1:
        await message.reply_text("Format : /manga < manga name >")
        return
    search = search[1]
    variables = {"search": search}
    json = await AioHttp().post_json(
        url, json={"query": manga_query, "variables": variables}
    )
    msg = ""
    if "errors" in json.keys():
        await message.reply_text("Manga not found")
        return
    if json:
        json = json["data"]["Media"]
        title, title_native = json["title"].get("romaji", False), json["title"].get(
            "native", False
        )
        start_date, status, score = (
            json["startDate"].get("year", False),
            json.get("status", False),
            json.get("averageScore", False),
        )
        if title:
            msg += f"**{title}**"
            if title_native:
                msg += f"(`{title_native}`)"
        if start_date:
            msg += f"\n**Start Date** - `{start_date}`"
        if status:
            msg += f"\n**Status** - `{status}`"
        if score:
            msg += f"\n**Score** - `{score}`"
        msg += "\n**Genres** - "
        for x in json.get("genres", []):
            msg += f"{x}, "
        msg = msg[:-2]
        info = json["siteUrl"]
        buttons = [[InlineKeyboardButton("More Info", url=info)]]
        image = json.get("bannerImage", False)
        msg += f"_{json.get('description', None)}_"
        if image:
            try:
                await message.reply_photo(
                    photo=image,
                    caption=msg,
                    parse_mode="markdown",
                    reply_markup=InlineKeyboardMarkup(buttons),
                )
            except BaseException:
                msg += f" [〽️]({image})"
                await message.reply_text(
                    msg,
                    parse_mode="markdown",
                    reply_markup=InlineKeyboardMarkup(buttons),
                )
        else:
            await message.reply_text(
                msg,
                parse_mode="markdown",
                reply_markup=InlineKeyboardMarkup(buttons),
            )


@alia.on_message(filters.command("mal"))
async def mal(client, message):
    args = message.text.split(None, 1)

    try:
        search_query = args[1]
    except BaseException:
        if message.reply_to_message:
            search_query = message.reply_to_message.text
        else:
            await message.reply_text("Format : /user <username>")
            return

    jikan = jikanpy.jikan.Jikan()

    try:
        user = jikan.user(search_query)
    except jikanpy.APIException:
        await message.reply_text("Username not found.")
        return

    progress_message = await message.reply_text("Searching.... ")

    date_format = "%Y-%m-%d"
    if user["image_url"] is None:
        img = "https://cdn.myanimelist.net/images/questionmark_50.gif"
    else:
        img = user["image_url"]

    try:
        user_birthday = datetime.datetime.fromisoformat(user["birthday"])
        user_birthday_formatted = user_birthday.strftime(date_format)
    except BaseException:
        user_birthday_formatted = "Unknown"

    user_joined_date = datetime.datetime.fromisoformat(user["joined"])
    user_joined_date_formatted = user_joined_date.strftime(date_format)

    for entity in user:
        if user[entity] is None:
            user[entity] = "Unknown"

    about = user["about"].split(" ", 60)

    try:
        about.pop(60)
    except IndexError:
        pass

    about_string = " ".join(about)
    about_string = about_string.replace("<br>", "").strip().replace("\r\n", "\n")

    caption = ""

    caption += textwrap.dedent(
        f"""
    **Username**: [{user['username']}]({user['url']})

    **Gender**: `{user['gender']}`
    **Birthday**: `{user_birthday_formatted}`
    **Joined**: `{user_joined_date_formatted}`
    **Days wasted watching anime**: `{user['anime_stats']['days_watched']}`
    **Days wasted reading manga**: `{user['manga_stats']['days_read']}`

    """
    )

    caption += f"**About**: {about_string}"

    buttons = [
        [InlineKeyboardButton(info_btn, url=user["url"])],
        [
            InlineKeyboardButton(
                close_btn, callback_data=f"anime_close, {message.from_user.id}"
            )
        ],
    ]

    await message.reply_photo(
        photo=img,
        caption=caption,
        parse_mode="markdown",
        reply_markup=InlineKeyboardMarkup(buttons),
    )
    progress_message.delete()


@alia.on_message(filters.command("upcoming"))
async def upcoming(client, message):
    jikan = jikanpy.jikan.Jikan()
    upcoming = jikan.top("anime", page=1, subtype="upcoming")

    upcoming_list = [entry["title"] for entry in upcoming["top"]]
    upcoming_message = ""

    for entry_num in range(len(upcoming_list)):
        if entry_num == 10:
            break
        upcoming_message += f"{entry_num + 1}. {upcoming_list[entry_num]}\n"

    await message.reply_text(upcoming_message)


@alia.on_message(filters.command("anilist"))
async def anilist(client, message):
    search_str = message.text.split(None, 1)
    if len(search_str) == 1:
        await message.reply_text("Tell Your Username :) ( /anilist <user>)")
        return
    variables = {"name": search_str[1]}
    resp = await AioHttp().post_json(
        url, json={"query": user_query, "variables": variables}
    )
    response = resp["data"]["User"]
    if not response:
        await message.reply_text("User not found")
        return
    else:
        stats = response["statistics"]["anime"]
        time = stats["minutesWatched"] * 60000
        time = f_time(time)
        msg = f"**Username :** `{response['name']}`\n**Watch Stats :** `{stats['count']} Animes`\n**Time Stats :** `{time}`\n**Episodes Stats :** `{stats['episodesWatched']}`\n**Top Genres :**"
        for x in stats["genres"][:3]:
            msg += f"`{x['genre']}`, "
        msg = msg[:-2] + "\n"
        abouto = response["about"].replace("<p>", "").replace("</p>", "")
        about = re.compile("<img.*?>").sub("", abouto)
        msg += f"**About :** `{about}`"
        image = response["avatar"]["large"]
        await message.reply_photo(
            photo=image, caption=msg, parse_mode="markdown"
        )


async def site_search(client, message, site: str):
    args = message.text.split(None, 1)
    more_results = True

    if len(args) == 2:
        split_query = args[1].split()
        search_query = "+".join(split_query)
    else:
        await message.reply_text("Give something to search")
        return

    if site == "kaizoku":
        search_url = f"https://animekaizoku.com/?s={search_query}"
        html_text = await AioHttp().get_text(search_url)
        soup = bs4.BeautifulSoup(html_text, "html.parser")
        search_result = soup.find_all("h2", {"class": "post-title"})

        if search_result:
            result = f"<b>Search results for</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>AnimeKaizoku</code>: \n"
            for entry in search_result:
                post_link = entry.a["href"]
                post_name = html.escape(entry.text)
                result += f"× <a href='https://animekaizoku.com/{post_link}'>{post_name}</a>\n"
        else:
            more_results = False
            result = f"<b>No result found for</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>AnimeKaizoku</code>"

    elif site == "kayo":
        search_url = f"https://animekayo.com/?s={search_query}"
        html_text = await AioHttp().get_text(search_url)
        soup = bs4.BeautifulSoup(html_text, "html.parser")
        search_result = soup.find_all("h2", {"class": "title"})

        result = f"<b>Search results for</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>AnimeKayo</code>: \n"
        for entry in search_result:

            if entry.text.strip() == "Nothing Found":
                result = f"<b>No result found for</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>AnimeKayo</code>"
                more_results = False
                break

            post_link = entry.a["href"]
            post_name = html.escape(entry.text.strip())
            result += f"× <a href='{post_link}'>{post_name}</a>\n"

    elif site == "kuso":
        search_url = f"https://kusonime.com/?s={search_query}"
        html_text = await AioHttp().get_text(search_url)
        soup = bs4.BeautifulSoup(html_text, "html.parser")
        search_result = soup.find_all("h2", {"class": "episodeye"})

        result = f"<b>Hasil pencarian untuk</b> <code>{html.escape(search_query)}</code> <b>di</b> <code>Kusonime</code>: \n"
        for entry in search_result:

            if not entry.text.strip():
                result = f"<b>Tidak ditemukan hasil untuk</b> <code>{html.escape(search_query)}</code> <b>di</b> <code>Kusonime</code>"
                more_results = False
                break

            post_link = entry.a["href"]
            post_name = html.escape(entry.text.strip())
            result += f"× <a href='{post_link}'>{post_name}</a>\n"

    elif site == "drive":
        search_url = f"https://drivenime.com/?s={search_query}"
        html_text = await AioHttp().get_text(search_url)
        soup = bs4.BeautifulSoup(html_text, "html.parser")
        search_result = soup.find_all("h2", {"class": "title"})

        result = f"<b>Hasil pencarian untuk</b> <code>{html.escape(search_query)}</code> <b>di</b> <code>Drivenime</code>: \n"
        for entry in search_result:

            if not entry.text.strip():
                result = f"<b>Tidak ditemukan hasil untuk</b> <code>{html.escape(search_query)}</code> <b>di</b> <code>Drivenime</code>"
                more_results = False
                break

            post_link = entry.a["href"]
            post_name = html.escape(entry.text.strip())
            result += f"× <a href='{post_link}'>{post_name}</a>\n"


    elif site == "neo":
        search_url = f"https://neonime.vip/?s={search_query}"
        html_text = await AioHttp().get_text(search_url)
        soup = bs4.BeautifulSoup(html_text, "html.parser")
        search_result = soup.find_all("div", {"class": "item episode-home"})

        result = f"<b>Hasil pencarian untuk</b> <code>{html.escape(search_query)}</code> <b>di</b> <code>Neonime</code>: \n"
        for entry in search_result:

            if not entry.text.strip():
                result = f"<b>Tidak ditemukan hasil untuk</b> <code>{html.escape(search_query)}</code> <b>di</b> <code>Neonime</code>"
                more_results = False
                break

            post_link = entry.a["href"]
            post_name = entry.img["alt"]
            result += f"× <a href='{post_link}'>{post_name}</a>\n"

    elif site == "same":
        search_url = f"https://samehadaku.vip/?s={search_query}"
        html_text = await AioHttp().get_text(search_url)
        soup = bs4.BeautifulSoup(html_text, "html.parser")
        search_result = soup.find_all("div", {"class": "animposx"})

        result = f"<b>Hasil pencarian untuk</b> <code>{html.escape(search_query)}</code> <b>di</b> <code>Samehadaku</code>: \n"
        for entry in search_result:

            if not entry.text.strip():
                result = f"<b>Tidak ditemukan hasil untuk</b> <code>{html.escape(search_query)}</code> <b>di</b> <code>Samehadaku</code>"
                more_results = False
                break

            post_link = entry.a["href"]
            post_name = entry.a["title"]
            result += f"× <a href='{post_link}'>{post_name}</a>\n"

    elif site == "otaku":
        search_url = f"https://otakudesu.tv/?s={search_query}&post_type=anime"
        api_url = f"https://anime.kaedenoki.net/api/search/{search_query}"
        json_text = await AioHttp().get_json(api_url)
        try:
            search_result = json_text["search_results"]
        except KeyError:
            result = f"<b>Tidak ditemukan hasil untuk</b> <code>{html.escape(search_query)}</code> <b>di</b> <code>Samehadaku</code>"
            more_results = False
            return

        result = f"<b>Hasil pencarian untuk</b> <code>{html.escape(search_query)}</code> <b>di</b> <code>Otakudesu</code>: \n"
        for entry in search_result:
            post_link = entry["link"]
            post_name = entry["title"]
            result += f"× <a href='{post_link}'>{post_name}</a>\n"

    buttons = [[InlineKeyboardButton("See all results", url=search_url)]]

    if more_results:
        await message.reply_text(
            result,
            parse_mode="html",
            reply_markup=InlineKeyboardMarkup(buttons),
            disable_web_page_preview=True,
        )
    else:
        await message.reply_text(
            result, parse_mode="html", disable_web_page_preview=True
        )


@alia.on_message(filters.command("kaizoku"))
async def kaizoku(client, message):
    await site_search(client, message, "kaizoku")


@alia.on_message(filters.command("kayo"))
async def kayo(client, message):
    await site_search(client, message, "kayo")


@alia.on_message(filters.command("kuso"))
async def kuso(client, message):
    await site_search(client, message, "kuso")


@alia.on_message(filters.command("drvnime"))
async def drive(client, message):
    await site_search(client, message, "drive")


@alia.on_message(filters.command("neo"))
async def neo(client, message):
    await site_search(client, message, "neo")


@alia.on_message(filters.command("same"))
async def same(client, message):
    await site_search(client, message, "same")


@alia.on_message(filters.command("otaku"))
async def otaku(client, message):
    await site_search(client, message, "otaku")


__help__ = """
Get information about anime, manga or characters from [AniList](anilist.co).

**Available commands:**

 × `/anime <anime>`**:** returns information about the anime.
 × `/character <character>`**:** returns information about the character.
 × `/manga <manga>`**:** returns information about the manga.
 × `/mal <user>`**:** returns information about a MyAnimeList user.
 × `/anilist <user>`**:** returns information about a Anilist user.
 × `/upcoming`**:** returns a list of new anime in the upcoming seasons.
 × `/kaizoku <anime>`**:** search an anime on animekaizoku.com
 × `/kayo <anime>`**:** search an anime on animekayo.com
 × `/airing <anime>`**:** returns anime airing info.
 × `/whatanime` **:** find what anime is from by replying a media
 **Only for** 🇮🇩
 × `/kuso <anime>`**:** Cari anime di kusonime.com
 × `/drvnime <anime>`**:** Cari anime di drivenime.com
 × `/neo <anime>`**:** Cari anime di neonime.vip
 × `/same <anime>`**:** Cari anime di samehadaku.vip
 × `/otaku <anime>`**:** Cari anime di otakudesu.tv

 """

__mod_name__ = "Anime"
