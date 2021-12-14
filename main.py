import time
import json
import requests
from datetime import timedelta

###
# user entries
target_assets = ("AXS 90", "AXS 60", "AXS 30")  # complete as multiple strings of coin and duration 
check_every = 1  # in minutes

# baseline url request
friendly_url = "https://www.binance.com/gateway-api/v1/friendly/pos/"\
               "union?pageSize=50&pageIndex=1&status=ALL"

# running full looping
while True:
    # requesting data from binance
    response = json.loads(requests.get(friendly_url).text)["data"]

    # unpacking results
    avaliables = []
    for item in response:
        for asset in item["projects"]:
            if not asset["sellOut"]:
                # asset available, adding a dictionary with asset name, duration and APY to the result list
                avaliables.append({
                    "asset": asset["asset"],
                    "duration": asset["duration"],
                    "APY": str(round(float(asset["config"]["annualInterestRate"])*100, 2))
                })

    printed = False
    for line in target_assets:
        name, period = line.split(" ")
        for item in avaliables:
            if name == item["asset"] and period == item["duration"]:
                printed = True
                print(f"************\n"\
                    f"Binance Locked Stacking\n"
                    f"{item['asset']} for {item['duration']}d / {item['APY']}% APY\n***\n**\n\n")
    
    if not printed:
        print("----")

    # time loop waiting
    time.sleep(timedelta(minutes=check_every).total_seconds())
