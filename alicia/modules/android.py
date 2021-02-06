import json

from bs4 import BeautifulSoup
from pyrogram import filters

from alicia import alia
from alicia.utils import AioHttp

GITHUB = "https://github.com"
DEVICES_DATA = "https://raw.githubusercontent.com/androidtrackers/certified-android-devices/master/by_device.json"


@alia.on_message(filters.command("magisk"))
async def magisk(client, message):
    url = "https://raw.githubusercontent.com/topjohnwu/magisk_files/"
    releases = ""
    for types, branch in {
        "Stable": ["master/stable", "master"],
        "Beta": ["master/beta", "master"],
        "Canary (debug)": ["canary/canary", "canary"],
    }.items():
        data = await AioHttp().get_text(url + branch[0] + ".json")
        data = json.loads(data)
        releases += (
            f"*{types}*: \n"
            f"× [Changelog](https://github.com/topjohnwu/magisk_files/blob/{branch[1]}/notes.md)\n"
            f'× Zip - [{data["magisk"]["version"]}-{data["magisk"]["versionCode"]}]({data["magisk"]["link"]}) \n'
            f'× App - [{data["app"]["version"]}-{data["app"]["versionCode"]}]({data["app"]["link"]}) \n'
            f'× Uninstaller - [{data["magisk"]["version"]}-{data["magisk"]["versionCode"]}]({data["uninstaller"]["link"]})\n\n'
        )

    await message.reply_text(
        "*Latest Magisk Releases:*\n{}".format(releases),
        parse_mode="markdown",
        disable_web_page_preview=True,
    )


@alia.on_message(filters.command("device"))
async def device(client, message):
    args = message.text.split(None, 1)
    if len(args) == 1:
        reply = "No codename provided, write a codename for fetching informations."
        await message.reply_text(
            "{}".format(reply),
            parse_mode="markdown",
            disable_web_page_preview=True,
        )
        return
    device = args[1]
    db = await AioHttp().get_text(DEVICES_DATA)
    db = json.loads(db)
    newdevice = device.strip("lte") if device.startswith("beyond") else device
    try:
        reply = f"Search results for {device}:\n\n"
        brand = db[newdevice][0]["brand"]
        name = db[newdevice][0]["name"]
        model = db[newdevice][0]["model"]
        codename = newdevice
        reply += (
            f"<b>{brand} {name}</b>\n"
            f"Model: <code>{model}</code>\n"
            f"Codename: <code>{codename}</code>\n\n"
        )
    except KeyError:
        reply = f"Couldn't find info about {device}!\n"
        await message.reply_text(
            "{}".format(reply),
            parse_mode="markdown",
            disable_web_page_preview=True,
        )
    await message.reply_text(
        "{}".format(reply), parse_mode="HTML", disable_web_page_preview=True
    )


@alia.on_message(filters.command("twrp"))
async def twrp(client, message):
    args = message.text.split(None, 1)
    if len(args) == 1:
        reply = "No codename provided, write a codename for fetching informations."
        await message.reply_text(
            "{}".format(reply),
            parse_mode="markdown",
            disable_web_page_preview=True,
        )
        return
    device = args[1]
    url = f"https://eu.dl.twrp.me/{device}"
    reply = f"*Latest Official TWRP for {device}*\n"
    db = await AioHttp().get_text(DEVICES_DATA)
    db = json.loads(db)
    newdevice = device.strip("lte") if device.startswith("beyond") else device
    try:
        brand = db[newdevice][0]["brand"]
        name = db[newdevice][0]["name"]
        reply += f"*{brand} - {name}*\n"
    except KeyError:
        pass
    try:
        page = BeautifulSoup((await AioHttp().get(url)).content, "lxml")
        date = page.find("em").text.strip()
        reply += f"*Updated:* {date}\n"
        trs = page.find("table").find_all("tr")
        row = 2 if trs[0].find("a").text.endswith("tar") else 1
        for i in range(row):
            download = trs[i].find("a")
            dl_link = f"https://eu.dl.twrp.me{download['href']}"
            dl_file = download.text
            size = trs[i].find("span", {"class": "filesize"}).text
            reply += f"[{dl_file}]({dl_link}) - {size}\n"

        await message.reply_text(
            "{}".format(reply),
            parse_mode="markdown",
            disable_web_page_preview=True,
        )
    except KeyError:
        await message.reply_text("can't find twrp for {}".fornat(device))


__help__ = """
Get Latest magisk relese, Twrp for your device or info about some device using its codename, Directly from Bot!

*Android related commands:*

 × /magisk - Gets the latest magisk release for Stable/Beta/Canary.
 × /device <codename> - Gets android device basic info from its codename.
 × /twrp <codename> -  Gets latest twrp for the android device using the codename.
"""

__mod_name__ = "Android"
