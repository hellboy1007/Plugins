from telethon import events
from telethon.tl.functions.channels import EditAdminRequest
from telethon.tl.types import ChatAdminRights

from hellbot.plugins.sql.gban_sql import is_gbanned, gbaner, ungbaner, all_gbanned
from . import *


@bot.on(hell_cmd(pattern=r"gban ?(.*)"))
@bot.on(sudo_cmd(pattern=r"gban ?(.*)", allow_sudo=True))
async def _(event):
    hell = await eor(event, "`Gbanning...`")
    reason = ""
    if event.reply_to_msg_id:
        userid = (await event.get_reply_message()).sender_id
        try:
            reason = event.text.split(" ", maxsplit=1)[1]
        except IndexError:
            reason = ""
    elif event.pattern_match.group(1):
        usr = event.text.split(" ", maxsplit=2)[1]
        userid = await get_user_id(usr)
        try:
            reason = event.text.split(" ", maxsplit=2)[2]
        except IndexError:
            reason = ""
    elif event.is_private:
        userid = (await event.get_chat()).id
        try:
            reason = event.text.split(" ", maxsplit=1)[1]
        except IndexError:
            reason = ""
    else:
        return await eod(hell, "**To gban a user i need a userid or reply to his/her message!!**")
    name = (await event.client.get_entity(userid)).first_name
    chats = 0
    if userid == ForGo10God:
        return await eod(hell, "🥴 **Nashe me hai kya lawde ‽**")
    if str(userid) in DEVLIST:
        return await eod(hell, "😑 **GBan my creator ?¿ Really‽**")
    if is_gbanned(userid):
        return await eod(
            hell,
            "This kid is already gbanned and added to my **Gban Watch!!**",
        )
    async for gfuck in event.client.iter_dialogs():
        if gfuck.is_group or gfuck.is_channel:
            try:
                await event.client.edit_permissions(gfuck.id, userid, view_messages=False)
                chats += 1
            except BaseException:
                pass
    gbaner(userid)
    gmsg = f"🥴 [{name}](tg://user?id={userid}) **beta majdur ko khodna 😪 aur** {hell_mention} **ko chodna... Kabhi sikhana nhi!! 😏**\n\n📍 Added to Gban Watch!!\n**🔰 Total Chats :**  `{chats}`"
    if reason != "":
        gmsg += f"\n**🔰 Reason :**  `{reason}`"
    await hell.edit(gmsg)


@bot.on(hell_cmd(pattern=r"ungban ?(.*)"))
@bot.on(sudo_cmd(pattern=r"ungban ?(.*)", allow_sudo=True))
async def _(event):
    hell = await eor(event, "`Ungban in progress...`")
    if event.reply_to_msg_id:
        userid = (await event.get_reply_message()).sender_id
    elif event.pattern_match.group(1):
        userid = await get_user_id(event.pattern_match.group(1))
    elif event.is_private:
        userid = (await event.get_chat()).id
    else:
        return await eod(hell, "`Reply to a user or give their userid... `")
    name = (await event.client.get_entity(userid)).first_name
    chats = 0
    if not is_gbanned(userid):
        return await eod(hell, "`User is not gbanned.`")
    async for gfuck in event.client.iter_dialogs():
        if gfuck.is_group or gfuck.is_channel:
            try:
                await event.client.edit_permissions(gfuck.id, userid, view_messages=True)
                chats += 1
            except BaseException:
                pass
    ungbaner(userid)
    await hell.edit(
        f"📍 [{name}](tg://user?id={userid}) **is now Ungbanned from `{chats}` chats and removed from Gban Watch!!**",
    )


@bot.on(hell_cmd(pattern="listgban$"))
@bot.on(sudo_cmd(pattern="listgban$", allow_sudo=True))
async def already(event):
    gbanned_users = all_gbanned()
    GBANNED_LIST = "**Gbanned Users :**\n"
    if len(gbanned_users) > 0:
        for user in gbanned_users:
            GBANNED_LIST += f"📍 [{user.chat_id}](tg://user?id={user.chat_id})\n"
    else:
        GBANNED_LIST = "No Gbanned Users!!"
    await edit_or_reply(event, GBANNED_LIST)


@bot.on(events.ChatAction)
async def _(event):
    if event.user_joined or event.added_by:
        user = await event.get_user()
        chat = await event.get_chat()
        if is_gbanned(str(user.id)):
            if chat.admin_rights:
                try:
                    await event.client.edit_permissions(
                        chat.id,
                        user.id,
                        view_messages=False,
                    )
                    gban_watcher = f"⚠️⚠️**Warning**⚠️⚠️\n\n`Gbanned User Joined the chat!!`\n**⚜️ Victim Id :**  [{user.first_name}](tg://user?id={user.id})\n"
                    gban_watcher += f"**🔥 Action 🔥**  \n`Banned this piece of shit....` **AGAIN!**"
                    await event.reply(gban_watcher)
                except BaseException:
                    pass


CmdHelp("global").add_command(
  "gban", "<reply>/<userid>", "Globally Bans the mentioned user in 'X' chats you are admin with ban permission."
).add_command(
  "ungban", "<reply>/<userid>", "Globally Unbans the user in 'X' chats you are admin!"
).add_info(
  "Global Admin Tool."
).add_warning(
  "✅ Harmlesss Module."
).add()
