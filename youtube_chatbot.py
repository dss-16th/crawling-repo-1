import pymongo
import requests,json
import pprint
import itertools

client = pymongo.MongoClient("mongodb://:27017")
db = client.youtube
collection = db.data
searches  = collection.find({'artist':{'$regex':'방탄'},'date':{'$regex':'2021'}})
msg = []
for search in searches:
        msg.append(search)
        
title = [data["title"] for data in msg]
artist = [data["artist"] for data in msg]
viewCount = [data["viewCount"] for data in msg]
current_Rank = [data["current_Rank"] for data in msg]
previous_Rank = [data["previous_Rank"] for data in msg]
change = [data["change"] for data in msg]
period_on_chart = [data["period_on_chart"] for data in msg]
date = [data["date"] for data in msg]
image = [data["image"] for data in msg]
play_url = [data["play_url"] for data in msg]
attachments = []

for i in range(len(title)):
    mu = {"blocks": [
            {"type": "divider"},
            {"type": "section",
             "text": {"type": "mrkdwn",
             "text": f"*<{play_url[i]}|{title[i]}>*\ {artist[i]} \nview Count : {viewCount[i]}\ncurrent_Rank : {current_Rank[i]} \nchange : {change[i]}\nperiod_on_chart : {period_on_chart[i]}"
            },
            "accessory": {"type": "image",
                          "image_url": f"{image[i]}",
                          "alt_text": f"{artist[i]} {title[i]}"}
            },
            {"type": "context",
             "elements": [{"type": "plain_text",
                  "text": f"previous_Rank : {previous_Rank[i]}"}]
            },
            {"type": "divider"}]
            }
    attachments.append(mu)
text = f"We found *{len(data)} result* in youtube_chart, from *{min(date).split('-')[0]} to {max(date).split('-')[1]}*"

def send_msg(slack_webhook, msg, channel="your_channe_name", username="차트알림봇"):
    payload = {"channel": channel, "username": username, "text": text, "attachments":attachments}
    requests.post(slack_webhook, json.dumps(payload))
    
slack_webhook = ""
send_msg(slack_webhook, json.dumps(mu))
