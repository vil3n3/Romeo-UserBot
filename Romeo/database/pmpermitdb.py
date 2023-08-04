from Romeo.database import cli
import asyncio

collection = cli["Romeo"]["pmpermit"]

PMPERMIT_MESSAGE = (
    "**𝙬𝙖𝙧𝙣𝙞𝙣𝙜!⚠️ 𝙥𝙡𝙯 𝙧𝙚𝙖𝙙 𝙩𝙝𝙞𝙨 𝙢𝙚𝙨𝙨𝙖𝙜𝙚 𝙘𝙖𝙧𝙚𝙛𝙪𝙡𝙡𝙮..\n\n**"
    "**𝑰'𝒎 𝑼𝒔𝒆𝒓-𝑽𝒊𝒍𝒍𝒊𝒂𝒏 𝑰'𝒎 𝒉𝒆𝒓𝒆 𝒕𝒐 𝒑𝒓𝒐𝒕𝒆𝒄𝒕 𝒎𝒚 𝒎𝒂𝒔𝒕𝒆𝒓 𝒇𝒓𝒐𝒎 𝒔𝒑𝒂𝒎𝒎𝒆𝒓𝒔.**"
    "**𝑖𝑓 𝑦𝑜𝑢 𝑎𝑟𝑒 𝑛𝑜𝑡 𝑎 𝑠𝑝𝑎𝑚𝑚𝑒𝑟 𝑡𝒉𝑒𝑛 𝑝𝑙𝑧 𝑤𝑎𝑖𝑡!.\n\n**"
    "**𝙪𝙣𝙩𝙞𝙡 𝙩𝙝𝙚𝙣, 𝙙𝙤𝙣'𝙩 𝙨𝙥𝙖𝙢, 𝙤𝙧 𝙮𝙤𝙪'𝙡𝙡 𝙜𝙚𝙩 𝙗𝙡𝙤𝙘𝙠𝙚𝙙 𝙖𝙣𝙙 𝙧𝙚𝙥𝙤𝙧𝙩𝙚𝙙 𝙗𝙮 𝙢𝙚, 𝙨𝙤 𝙗𝙚 𝙘𝙖𝙧𝙚𝙛𝙪𝙡𝙡 𝙩𝙤 𝙨𝙚𝙣𝙙 𝙖𝙣𝙮 𝙢𝙚𝙨𝙨𝙖𝙜𝙚𝙨!**"
)

BLOCKED = "**𝑩𝑬𝑬𝑷 𝑩𝑶𝑶𝑷 𝑭𝑶𝑼𝑵𝑫𝑬𝑫 𝑨 𝑺𝑷𝑨𝑴𝑴𝑬𝑹!, 𝑩𝑳𝑶𝑪𝑲 𝑺𝑼𝑪𝑪𝑬𝑺𝑺𝑭𝑼𝑳𝑳𝒀!**"

LIMIT = 5


async def set_pm(value: bool):
    doc = {"_id": 1, "pmpermit": value}
    doc2 = {"_id": "Approved", "users": []}
    r = await collection.find_one({"_id": 1})
    r2 = await collection.find_one({"_id": "Approved"})
    if r:
        await collection.update_one({"_id": 1}, {"$set": {"pmpermit": value}})
    else:
        await collection.insert_one(doc)
    if not r2:
        await collection.insert_one(doc2)


async def set_permit_message(text):
    await collection.update_one({"_id": 1}, {"$set": {"pmpermit_message": text}})


async def set_block_message(text):
    await collection.update_one({"_id": 1}, {"$set": {"block_message": text}})


async def set_limit(limit):
    await collection.update_one({"_id": 1}, {"$set": {"limit": limit}})


async def get_pm_settings():
    result = await collection.find_one({"_id": 1})
    if not result:
        return False
    pmpermit = result["pmpermit"]
    pm_message = result.get("pmpermit_message", PMPERMIT_MESSAGE)
    block_message = result.get("block_message", BLOCKED)
    limit = result.get("limit", LIMIT)
    return pmpermit, pm_message, limit, block_message


async def allow_user(chat):
    doc = {"_id": "Approved", "users": [chat]}
    r = await collection.find_one({"_id": "Approved"})
    if r:
        await collection.update_one({"_id": "Approved"}, {"$push": {"users": chat}})
    else:
        await collection.insert_one(doc)


async def get_approved_users():
    results = await collection.find_one({"_id": "Approved"})
    if results:
        return results["users"]
    else:
        return []


async def deny_user(chat):
    await collection.update_one({"_id": "Approved"}, {"$pull": {"users": chat}})


async def pm_guard():
    result = await collection.find_one({"_id": 1})
    if not result:
        return False
    if not result["pmpermit"]:
        return False
    else:
        return True
