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

import yaml
from yaml import Loader


# ALL ITEMS FILE
items_file = open("yamls/items.yml", "rb")
items = yaml.load(items_file, Loader = Loader) 


# MINING ITEMS 
pickaxes = items["pickaxe"]

print(pickaxes["stonepickaxe"])