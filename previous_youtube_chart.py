import numpy as np
import requests
import re
import json
import pandas as pd
import pandas as pd 
from datetime import datetime
import time

start = pd.date_range(start ='4-27-2018',  
         end ='12-27-2019', freq ='7D') 
start_date = start.strftime('%Y%m%d')
start_date= start_date.to_list() 
import datetime
end = start + datetime.timedelta(days=6)
end_date = end.strftime('%Y%m%d')
end_date= end_date.to_list() 
start_date,end_date 
for start_date,end_date in zip(start_date,end_date):
    url = "https://charts.youtube.com/charts/TopSongs/kr?hl=ko"
    response = requests.get(url)
    key = re.findall('"INNERTUBE_API_KEY":"\w+\W+\w+"', response.text)[0].split(":")[1].replace('"','')
    url = f'https://charts.youtube.com/youtubei/v1/browse?alt=json&key={key}'
    query = {"context":{"client":{"clientName":"WEB_MUSIC_ANALYTICS",
                                  "clientVersion":"0.2","hl":"ko","gl":"KR",
                                  "experimentIds":[],"experimentsToken":"",
                                  "theme":"MUSIC"},"capabilities":{},
                        "request":{"internalExperimentFlags":[]}},
             "browseId":"FEmusic_analytics_charts_home",
             "query":f"chart_params_type=WEEK&perspective=CHART&flags=viral_video_chart&\
             selected_chart=TRACKS&chart_params_id=weekly%3A{start_date}%3A{end_date}%3Akr"}
    headers = {"referer":"https://charts.youtube.com/charts/TopSongs/kr/20191108-20191114?hl=ko"}
    response = requests.post(url, json=query, headers=headers)
    datas = response.json()["contents"]["sectionListRenderer"]["contents"][0]["musicAnalyticsSectionRenderer"]["content"]["trackTypes"][0]["trackViews"]  
    print("url load")
    time.sleep(5)
    try:
        data_1 = [
        {"title": data["name"], "artist":data["artists"][0]["name"],
        "viewCount":str(round(int(data["viewCount"])/1000000,2)) + "M",
         "current_Rank":data["chartEntryMetadata"].get('currentPosition'),
        "previous_Rank":data['chartEntryMetadata'].get('previousPosition'),
         "change":data['chartEntryMetadata'].get('percentViewsChange'),
         "period_on_chart":str(data['chartEntryMetadata'].get('periodsOnChart')) + " week",
         "image":data["thumbnail"]["thumbnails"][1]["url"],
        "play_url":"https://www.youtube.com/watch?v=" + data["encryptedVideoId"],
        } 
        for data in datas
        ]
    
    except:
        print("we cant't find something")
        data_1 = [
        {"title": data["name"], "artist":data["artists"][0]["name"],
        "viewCount":str(round(int(data["viewCount"])/1000000,2)) + "M",
         "current_Rank":data["chartEntryMetadata"].get('currentPosition'),
        "previous_Rank":data['chartEntryMetadata'].get('previousPosition'),
         "change":data['chartEntryMetadata'].get('percentViewsChange'),
         "period_on_chart":str(data['chartEntryMetadata'].get('periodsOnChart')) + " week",
         #"image":data["thumbnail"]["thumbnails"][1]["url"],
        #"play_url":"https://www.youtube.com/watch?v=" + data["encryptedVideoId"],
        } 
        for data in datas
    ]
    df = pd.DataFrame(data_1)
    df = df.replace(np.nan,0)
    df['previous_Rank'] = df['previous_Rank'].astype(int)
    df['change'] = round(df['change'] * 100,1).astype(str) + "%"
    df["date"] = str(start_date)+"-"+str(end_date)
    try:
        df[["date","title","artist","viewCount","current_Rank","previous_Rank","change","period_on_chart","image","play_url"]]
    except:
        print("we can't findsomething")
        df["image"] = "-"
        df["play_url"] = "-" 
        df[["date","title","artist","viewCount","current_Rank","previous_Rank","change","period_on_chart","image","play_url"]]
    df[["date","title","artist","viewCount","current_Rank","previous_Rank","change","period_on_chart","image","play_url"]]
    data_1 = df.to_dict('records')
    import pymongo

    client = pymongo.MongoClient("mongodb://dss:dss@52.79.124.129:27017")
    collection = client.youtube.data


    collection.insert_many(data_1)