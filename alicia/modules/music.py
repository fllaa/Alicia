import asyncio
import os
import shutil

import deezloader
from deezloader.exceptions import NoDataApi
from pyrogram import filters
from tswift import Song

import alicia.modules.sql.last_fm_sql as sql
from alicia import ARL, LASTFM_API_KEY, alia
from alicia.utils import AioHttp

TEMP_PATH = "deez_temp/"


@alia.on_message(filters.command("music"))
async def music(client, message):
    if not os.path.exists(TEMP_PATH):
        os.makedirs(TEMP_PATH)
    args = message.text.split()
    track = ""
    try:
        loader = deezloader.Login(ARL)
    except Exception as excp:
        await message.reply_text(f"Failed to load token. Error: {excp}")
        return
    try:
        flag = args[1]
        query = args[2]
    except IndexError:
        await message.reply_text(
            "use format: `/music` <flag> <link/song name> <quality>", parse_mode="markdown")
        return
    quality = "MP3_320"
    if len(args) == 4:
        quality = args[3]
    msg = await message.reply_text(f"Searching the music as {quality} . . .")
    try:
        if flag == "-link":
            if "deezer" in query:
                track = loader.download_trackdee(
                    query,
                    output=TEMP_PATH,
                    quality=quality,
                    recursive_quality=True,
                    recursive_download=True,
                    not_interface=True,
                )
            if "spotify" in query:
                track = loader.download_trackspo(
                    query,
                    output=TEMP_PATH,
                    quality=quality,
                    recursive_quality=True,
                    recursive_download=True,
                    not_interface=True,
                )
        if flag == "-song":
            if len(query.split("-")) == 2:
                artist, song = query.split("-")
            else:
                await msg.edit_text("read /help music plox on me")
                return
            track = loader.download_name(
                artist=artist,
                song=song,
                output=TEMP_PATH,
                recursive_quality=True,
                recursive_download=True,
                not_interface=True,
            )
    except NoDataApi:
        await msg.edit_text("Song Not Found *sad")
        return
    except Exception as excp:
        await msg.edit_text(f"Failed. Error: {excp}")
        return
    try:
        await asyncio.gather(
            msg.edit_text("Uploading music . . ."),
            msg.reply_audio(audio=open(track, "rb")),
            msg.edit_text("Done. :)"),
        )
    except FileNotFoundError:
        await msg.edit_text("read /help music plox on me")
    shutil.rmtree(TEMP_PATH)


@alia.on_message(filters.command("setuser"))
async def set_user(client, message):
    args = message.text.split(None, 1)
    if args:
        user = message.from_user.id
        username = args[1]
        sql.set_user(user, username)
        await message.reply_text(f"Username set as {username}!")
    else:
        await message.reply_text(
            "That's not how this works...\nRun /setuser followed by your username!"
        )


@alia.on_message(filters.command("clearuser"))
async def clear_user(client, message):
    user = message.frouser.id
    sql.set_user(user, "")
    await message.reply_text(
        "Last.fm username successfully cleared from my database!"
    )


@alia.on_message(filters.command("lastfm"))
async def last_fm(client, message):
    user = message.from_user.first_name
    user_id = message.from_user.id
    username = sql.get_user(user_id)
    if not username:
        await message.reply_text("You haven't set your username yet!")
        return

    base_url = "http://ws.audioscrobbler.com/2.0"
    res = await AioHttp().get_json(
        f"{base_url}?method=user.getrecenttracks&limit=3&extended=1&user={username}&api_key={LASTFM_API_KEY}&format=json"
    )
    try:
        if res["message"] == "User not found":
            await message.reply_text(
                "Hmm... something went wrong.\nPlease ensure that you've set the correct username!"
            )
        return
    except KeyError:
        pass

    try:
        first_track = res.get("recenttracks").get("track")[0]
    except IndexError:
        await message.reply_text("You don't seem to have scrobbled any songs...")
        return
    if first_track.get("@attr"):
        # Ensures the track is now playing
        image = first_track.get("image")[3].get("#text")  # Grab URL of 300x300 image
        artist = first_track.get("artist").get("name")
        song = first_track.get("name")
        loved = int(first_track.get("loved"))
        rep = f"{user} is currently listening to:\n"
        if not loved:
            rep += f"🎧  <code>{artist} - {song}</code>"
        else:
            rep += f"🎧  <code>{artist} - {song}</code> (♥️, loved)"
        if image:
            rep += f"<a href='{image}'>\u200c</a>"
    else:
        tracks = res.get("recenttracks").get("track")
        track_dict = {
            tracks[i].get("artist").get("name"): tracks[i].get("name") for i in range(3)
        }
        rep = f"{user} was listening to:\n"
        for artist, song in track_dict.items():
            rep += f"🎧  <code>{artist} - {song}</code>\n"
        last_user = (
            (await AioHttp().get_json(
                f"{base_url}?method=user.getinfo&user={username}&api_key={LASTFM_API_KEY}&format=json"
            ))
            .get("user")
        )
        scrobbles = last_user.get("playcount")
        rep += f"\n(<code>{scrobbles}</code> scrobbles so far)"

    await message.reply_text(rep, parse_mode="HTML")


@alia.on_message(filters.command("lyrics"))
async def lyrics(client, message):
    args = message.text.split(None, 1)
    query = args[1]
    song = ""
    if not query:
        await message.reply_text("You haven't specified which song to look for!")
        return
    song = Song.find_song(query)
    if song:
        if song.lyrics:
            reply = song.format()
        else:
            reply = "Couldn't find any lyrics for that song!"
    else:
        reply = "Song not found!"
    if len(reply) > 4090:
        with open("lyrics.txt", "w") as f:
            f.write(f"{reply}\n\n\nOwO UwU OmO")
        with open("lyrics.txt", "rb") as f:
            await message.reply_document(
                document=f,
                caption="Message length exceeded max limit! Sending as a text file.",
            )
    else:
        await message.reply_text(reply)


__help__ = """
Like name this module, you can search anything about music

 × /music <flag> <query> <quality> : Download music [more info](https://telegra.ph/Music-Downloader-Info-01-20)
 × /lyrics <query>: search lyrics can be song name or artist name
 *Last.FM*
 × /setuser <username>: sets your last.fm username.
 × /clearuser: removes your last.fm username from the bot's database.
 × /lastfm: returns what you're scrobbling on last.fm.
"""

__mod_name__ = "Music"
