import numpy as np
import requests
import re
import json
import pandas as pd


# 함수로 만들기
def youtube():
    
    # 1. 날짜 지정
#     from datetime import datetime
#     date = datetime.now()
#     start_date = int(date.strftime("%Y%m%d"))
#     import datetime
#     end_date = date + datetime.timedelta(days=6)
#     end_date = int(end_date.strftime("%Y%m%d"))
    start_date = 20210226
    end_date = 20210304
    start_date, end_date
    
    # 2. key값 불러오기.
    url = "https://charts.youtube.com/charts/TopSongs/kr?hl=ko"
    response = requests.get(url)
    key = re.findall('"INNERTUBE_API_KEY":"\w+\W+\w+"', response.text)[0].split(":")[1].replace('"','')
    
    # 3. url 불러오기
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
    
    # 4. 원하는 data불러오기
    try:
        data_1 = [
        {"title": data["name"], "artist":data["artists"][0]["name"],
        "viewCount":data["viewCount"] + "M",
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
        data_1 = [
        {"title": data["name"], "artist":data["artists"][0]["name"],
        "viewCount":data["viewCount"] + "M",
         "current_Rank":data["chartEntryMetadata"].get('currentPosition'),
        "previous_Rank":data['chartEntryMetadata'].get('previousPosition'),
         "change":data['chartEntryMetadata'].get('percentViewsChange'),
         "period_on_chart":str(data['chartEntryMetadata'].get('periodsOnChart')) + " week",
         #"image":data["thumbnail"]["thumbnails"][1]["url"],
        #"play_url":"https://www.youtube.com/watch?v=" + data["encryptedVideoId"],
        } 
        for data in datas
    ]
        
    # 5. 데이터프레임으로 변환
    df = pd.DataFrame(data_1)
    
    # 6. nan 값 제거
    df = df.replace(np.nan,0)
    
    # 7. 불러올 수 없는 data 채우기
    
    df['previous_Rank'] = df['previous_Rank'].astype(int)
    df['change'] = round(df['change'] * 100,1).astype(str) + "%"
    df["date"] = str(start_date)+"-"+str(end_date)
    try:
        df[["date","title","artist","viewCount","current_Rank","previous_Rank","change","period_on_chart","image","play_url"]]
    except:
        df["image"] = "-"
        df["play_url"] = "-" 
        df[["date","title","artist","viewCount","current_Rank","previous_Rank","change","period_on_chart","image","play_url"]]
    df[["date","title","artist","viewCount","current_Rank","previous_Rank","change","period_on_chart","image","play_url"]]
    
    
    # 8. 데이터 프레임 dict 타입으로 변환
    
    data_1 = df.to_dict('records')
    return data_1
    
    
    
    
    
    