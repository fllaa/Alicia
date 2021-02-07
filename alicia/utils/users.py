from pyrogram import Client as client
from pyrogram.errors import BadRequest

import alicia.modules.sql.users_sql as sql
from alicia import LOGGER


async def get_user_id(username):
    # ensure valid userid
    if len(username) <= 5:
        return None

    if username.startswith("@"):
        username = username[1:]

    users = sql.get_userid_by_name(username)

    if not users:
        return None

    elif len(users) == 1:
        return users[0].user_id

    else:
        for user_obj in users:
            try:
                userdat = await client.get_chat(user_obj.user_id)
                if userdat.username == username:
                    return userdat.id

            except BadRequest as excp:
                if excp.message != "Chat not found":
                    LOGGER.exception("Error extracting user ID")

    return None