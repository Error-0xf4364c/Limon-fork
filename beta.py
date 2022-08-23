"""

userCareer = {
    "points" : {
        "forester_point": 60,
        "mining_point": 17
    }
    
}


##less = [ f"{' '.join(i.split('_')).title()} = {userCareer['points'][i]}" for i in userCareer["points"] ]

for i in userCareer:
    if i.endswith("_point"):
        x = i.split("_")
        #userPointName = x.title()
        userPoint = userCareer[i]
        yz = f"userPointName = {userPoint}"
    else:
        userPointName = "You have not career point!"

#y = "\n".join(less)

userCareer["points"]["forester_point"] += 1
print(userCareer)
"""
"""
mydict = {
    "items": {
        "rod": "altınolta",
        "axe": "taşbalta"
    }
}

del mydict["items"]["rod"]

print(mydict)


"""

"""
print(birlesik)

print("-----")
for i in birlesik:
    if i == "none":
        continue
    print(birlesik[i]["name"])

"""

import yaml
from yaml import Loader
from main import MyBot

# Fishes File
fish_file = open("yamls/fishing.yml", "rb")
fish = yaml.load(fish_file, Loader = Loader)

vlf = fish["veryLowLevelFish"]
lf = fish["lowLevelFish"]
mlf = fish["mediumLevelFish"]
hf = fish["highLevelFish"]
vhf = fish["veryHighLevelFish"]
priceByFishSize = fish["priceByFishSize"]
all_fish = vlf | lf | mlf | hf | vhf
beforFish = " ".join(all_fish.keys())
splittedFishFish = beforFish.split(" ")
print(all_fish)

VHF = fish["veryHighLevelFish"] # Very High Level Fishes
veryHighLvFish = " ".join(VHF.keys()) # Very High Level Fishes Keys
splittedFish = veryHighLvFish.split(" ") # to List Fishes keys
print("------------------------------")
print(splittedFishFish)