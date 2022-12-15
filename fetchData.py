import collections

async def economyData(bot, _id):

    db = bot.mongoConnect["cupcake"]
    collection = db["economy"]


    if await collection.find_one({"_id" : _id}) == None:
        newData = {
            "_id": _id,
            "coins" :0
        }
        await collection.insert_one(newData)

    return await collection.find_one({"_id" : _id})

async def careerData(bot, _id):

    db = bot.mongoConnect["cupcake"]
    collection = db["career"]


    if await collection.find_one({"_id" : _id}) == None:
        newData = {
            "_id": _id,
            "points": {
                "fisher_point" : 0,
                "hunter_point" : 0,
                "miner_point" : 0,
                "forester_point" : 0,
                "send_point" : 0,
                "gamble_point" : 0
            }
        }
        await collection.insert_one(newData)

    return await collection.find_one({"_id" : _id})