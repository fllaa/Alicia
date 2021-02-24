async def user_can_promote(client, chat, user) -> bool:
    member = await client.get_chat_member(chat.id, user.id)
    return member.can_promote_members


async def user_can_ban(client, chat, user) -> bool:
    member = await client.get_chat_member(chat.id, user.id)
    return member.can_restrict_members


async def user_can_pin(client, chat, user) -> bool:
    member = await client.get_chat_member(chat.id, user.id)
    return member.can_edit_messages


async def user_can_changeinfo(client, chat, user) -> bool:
    member = await client.get_chat_member(chat.id, user.id)
    return member.can_change_info
