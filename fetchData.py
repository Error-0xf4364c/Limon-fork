def create_wallet(bot, _id):

    db = bot.database["limon"]
    collection = db["wallet"]

    if collection.find_one({"_id" : _id}) == None:
        new_data = {
            "_id": _id,
            "cash" : 0
        }
        collection.insert_one(new_data)
        

    return collection.find_one({"_id" : _id}), collection

def create_career_data(bot, _id):

    db = bot.database["limon"]
    collection = db["career"]

    if collection.find_one({"_id" : _id}) == None:
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
        collection.insert_one(newData)

    return collection.find_one({"_id" : _id}), collection
