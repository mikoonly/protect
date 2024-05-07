import asyncio
import re
from io import BytesIO

import requests
from config import *
from pyrogram import *
from men import app, list_admins, member_permissions, extract_user
from pler import kntl
from db import *

async def init():
    await app.start()
    await premtool()
    await idle()
    await app.stop()

@app.on_message(filters.command("protec", PREFIX) & ~filters.private)
@prouser
# @language
async def anti_anti(_, m):
    if len(m.command) != 2:
        return await m.reply_text("Usage: /Protec [on|off]")
    status = m.text.split(None, 1)[1].strip()
    status = status.lower()
    chat_id = m.chat.id
    if status == "on":
        if await is_antigcast_on(chat_id):
            await m.reply_text("Protec Anti-Gcast Active.")
        else:
            await antigcast_on(chat_id)
            await m.reply_text(
                "Enabled Anti-Gcast System. I will Delete Messages from Now on."
            )
    elif status == "off":
        if not await is_antigcast_on(chat_id):
            await m.reply_text("Protec Anti-Gcast sudah No Active.")
        else:
            await antigcast_off(chat_id)
            await m.reply_text(
                "Disabled Anti-Gcast System. I won't Be Deleting Message from Now on."
            )
    else:
        await m.reply_text("Unknown Suffix, Use /protec [on|off]")


async def isGcast(filter, c, update):
    bl = "€¥£¢𝑎𝑏𝑐𝑑𝑒𝑓𝑔𝒉𝑖𝑗𝑘𝑙𝑚𝑛𝑜𝑝𝑞𝑟𝑠𝑡𝑢𝑣𝑤𝑥𝑦𝑧𝐴𝐵𝐶𝐷𝐸𝐹𝐺𝐻𝐼𝐽𝐾𝐿𝑀𝑁𝑂𝑃𝑄𝑅𝑆𝑇𝑈𝑉𝑊𝑋𝑌𝑍𝘢𝘣𝘤𝘥𝘦𝘧𝘨𝘩𝘪𝘫𝘬𝘭𝘮𝘯𝘰𝘱𝘲𝘳𝘴𝘵𝘶𝘷𝘸𝘹𝘺𝘻𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏𝘐𝘑𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘞𝘟𝘠𝘡𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ×‌ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂ️ⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏ🅐🅑🅒🅓🅔🅕🅖🅗🅘🅙🅚🅛🅜🅝🅞🅟🅠🅡🅢🅣🅤🅥🅦🅧🅨🅩🅐🅑🅒🅓🅔🅕🅖🅗🅘🅙🅚🅛🅜🅝🅞🅟🅠🅡🅢🅣🅤🅥🅦🅧🅨🅩🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅀🅁🅂🅃🅄🅅🅆🅇🅈🅉🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅀🅁🅂🅃🅄🅅🅆🅇🅈🅉🅰️🅱️🅲🅳🅴🅵🅶🅷🅸🅹🅺🅻🅼🅽🅾️🅿️🆀🆁🆂🆃🆄🆅🆆🆇🆈🆉🅰️🅱️🅲🅳🅴🅵🅶🅷🅸🅹🅺🅻🅼🅽🅾️🅿️🆀🆁🆂🆃🆄🆅🆆🆇🆈🆉🇦 🇧 🇨 🇩 🇪 🇫 🇬 🇭 🇮 🇯 🇰 🇱 🇲 🇳 🇴 🇵 🇶 🇷 🇸 🇹 🇺 🇻 🇼 🇽 🇾 🇿 🇦 🇧 🇨 🇩 🇪 🇫 🇬 🇭 🇮 🇯 🇰 🇱 🇲 🇳 🇴 🇵 🇶 🇷 🇸 🇹 🇺 🇻 🇼 🇽 🇾 🇿 ᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘϙʀᴛᴜᴠᴡʏᴢᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘϙʀᴛᴜᴠᴡʏᴢᵃᵇᶜᵈᵉᶠᵍʰⁱʲᵏˡᵐⁿᵒᵖᵠʳˢᵗᵘᵛʷˣʸᶻᵃᵇᶜᵈᵉᶠᵍʰⁱʲᵏˡᵐⁿᵒᵖᵠʳˢᵗᵘᵛʷˣʸᶻᵃᵇᶜᵈᵉᶠᵍʰⁱʲᵏˡᵐⁿᵒᵖᵠʳˢᵗᵘᵛʷˣʸᶻᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘϙʀᴛᴜᴠᴡʏᴢᗩᗷᑕᗞᗴᖴᏀᕼᏆᒍᏦしᗰᑎᝪᑭᑫᖇᔑᎢᑌᐯᗯ᙭ᎩᏃᗩᗷᑕᗞᗴᖴᏀᕼᏆᒍᏦしᗰᑎᝪᑭᑫᖇᔑᎢᑌᐯᗯ᙭ᎩᏃᎪᏴᏟᎠᎬҒᏀᎻᏆᎫᏦᏞᎷΝϴᏢϘᎡՏͲႮᏙᏔХᎽᏃᎪᏴᏟᎠᎬҒᏀᎻᏆᎫᏦᏞᎷΝϴᏢϘᎡՏͲႮᏙᏔХᎽᏃａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭𝙖𝙗𝙘𝙙𝙚𝙛𝙜𝙝𝙞𝙟𝙠𝙡𝙢𝙣𝙤𝙥𝙦𝙧𝙨𝙩𝙪𝙫𝙬𝙭𝙮𝙯𝘼𝘽𝘾𝘿𝙀𝙁𝙂𝙃𝙄𝙅𝙆𝙇𝙈𝙉𝙊𝙋𝙌𝙍𝙎𝙏𝙐𝙑𝙒𝙓𝙔𝙕𝚊𝚋𝚌𝚍𝚎𝚏𝚐𝚑𝚒𝚓𝚔𝚕𝚖𝚗𝚘𝚙𝚚𝚛𝚜𝚝𝚞𝚟𝚠𝚡𝚢𝚣𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙𝒂𝒃𝒄𝒅𝒆𝒇𝒈𝒉𝒊𝒋𝒌𝒍𝒎𝒏𝒐𝒑𝒒𝒓𝒔𝒕𝒖𝒗𝒘𝒙𝒚𝒛𝑨𝑩𝑪𝑫𝑬𝑭𝑮𝑯𝑰𝑱𝑲𝑳𝑴𝑵𝑶𝑷𝑸𝑹𝑺𝑻𝑼𝑽𝑾𝑿𝒀𝒁"
    awoos = update.text
    user = update.from_user.id
    x = awoos.lower()
    bl_url = "https://raw.githubusercontent.com/naya1503/bl/main/bl.json"
    response = requests.get(bl_url)
    if response.status_code == 200:
        lbl = response.text.split("\n")
    else:
        lbl = []

    # with open("bl.txt", "r") as file:
    # blc = [w.lower().strip() for w in file.readlines()]
    #
    blc = [w.lower().strip() for w in lbl]
    bluser = await is_bisu_user(user)
    for chara in bl:
        blc.append(chara)
    for chara in blc:
        if chara in x:
            return True
    if bluser:
        return True
    if x in await bl_bang():
        return True

    return False


Gcast = filters.create(isGcast)


@app.on_message(filters.text & filters.group & Gcast, group=-1)
@anti_gcast
async def deletermessag(app, m):
    chat_id = m.chat.id
    user = m.from_user
    if chat_id not in await cek_pro():
        return
    if not user:
        return
    elif user.id in await list_admins(chat_id):
        return

    try:
        await app.delete_messages(chat_id, message_ids=m.id)
    except FloodWait as e:
        await asyncio.sleep(e.value)
        await app.delete_messages(chat_id, message_ids=m.id)
    except MessageDeleteForbidden:
        return

@app.on_message(filters.command(["duar"], PREFIX) & ~filters.private & filters.user(OWNER_ID))
async def banFunc(_, m):
    ijin = await member_permissions(m.chat.id, m.from_user.id)
    xx = "can_restrict_members"
    if xx not in ijin:
        return
    user_id = await extract_user(m)
    if not user_id:
        return
    if user_id == app.me.id:
        return
    if user_id in OWNER_ID:
        return
    if user_id in (await list_admins(m.chat.id)):
        return
    dicekah = await is_bisu_user(user_id)
    if dicekah:
        return await m.reply_text("Binatang Liar Ini Sudah Terblacklist.")
    try:
        mention = (await app.get_users(user_id)).mention
    except IndexError:
        mention = (
            m.reply_to_m.sender_chat.title
            if m.reply_to_message
            else "Anon"
        )
    await add_bisu_user(user_id)
    return await m.reply(f"User : {mention} Binatang Liar Ini Sudah Terblacklist.")

@app.on_message(filters.command(["lepas"], PREFIX) & ~filters.private & filters.user(OWNER_ID))
async def banFunc(_, m):
    ijin = await member_permissions(m.chat.id, m.from_user.id)
    xx = "can_restrict_members"
    if xx not in ijin:
        return
    user_id = await extract_user(m)
    if not user_id:
        return
    dicekah = await is_bisu_user(user_id)
    if not dicekah:
        return await m.reply_text("Binatang Liar Terlepas Dari Blacklist.")
    try:
        mention = (await app.get_users(user_id)).mention
    except IndexError:
        mention = (
            m.reply_to_m.sender_chat.title
            if m.reply_to_message
            else "Anon"
        )
    await remove_bisu_user(user_id)
    return await m.reply(f"User : {mention} added to whitelist.")

@app.on_message(filters.command(["pro"], PREFIX))
@prouser
async def diproin(c, m):
    chat_id = (
        m.chat.id if m.chat.id else int(m.text.strip().split()[1])
    )
    if chat_id in await cek_pro():
        return
    diprokan = await add_pro(chat_id)
    if diprokan:
        return
    else:
        await m.reply_text("Added to Anti-Gcast.")


@app.on_message(filters.command("listpro", PREFIX))
@prouser
async def KONTOL(c, m):
    text = ""
    for count, chat_id in enumerate(await cek_pro(), 1):
        try:
            title = (await app.get_chat(chat_id)).title
        except Exception:
            title = "Private"
        text += "<b>• {count}. {title} [<code>{chat_id}</code>]</b>\n".format(count, title, chat_id)
    if text == "":
        return
    await m.reply_text(text)


@app.on_message(filters.command(["unpro"], PREFIX))
@prouser
async def diproin(c, m):
    chat_id = (
        m.chat.id if m.chat.id else int(m.text.strip().split()[1])
    )
    if chat_id not in await cek_pro():
        return
    diprokan = await remove_pro(chat_id)
    if diprokan:
        await m.reply_text("Done disable Anti-Gcast")
    else:
        return


if __name__ == "__main__":
    loop = asyncio.get_event_loop_policy().get_event_loop()
    loop.run_until_complete(init())
    kntl.run_until_disconnected()
