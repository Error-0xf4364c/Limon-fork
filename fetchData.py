import collections


async def fetchData(bot, _id):

    db = bot.mongoConnect["cupcake"]
    collection = db["economy"]


    if await collection.find_one({"_id" : _id}) == None:
        newData = {
            "_id": _id,
            "coins" :0
        }
        await collection.insert_one(newData)

    return await collection.find_one({"_id" : _id})