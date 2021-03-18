
#  유튜브 차트(조회수 기준) 100을 챗봇을 이용하여 전송해주는 서비스



#### __CRAWLING PROJECT__
****
#### 기간 : 
#### * 인원 : 2명
##### * 정민주 :  
##### 
##### GitHub address : [https://github.com/meiren13](https://github.com/meiren13)
##### * 이주영 : Crawling, DB 저장(2018-2019 year), slack bot 구현, module 생성(previous_youtube_chart.py, youtube.py, youtube_chatbot.py)
##### READ_ME
##### GitHub address : [https://github.com/leekj3133](https://github.com/leekj3133)

****
#### reference
* 
****


## 1. Intro

#### 1-1. Intro

#### 1-2. purpose
조회수가 기준인 유튜브 차트 100을 이용하여 소비자들에게 정보제공을 하기 위해 크롤링과 메세지보내기를이용

#### 1-4. Dataset

![image](https://user-images.githubusercontent.com/75352728/110234179-60abcf00-7f6c-11eb-8141-8fa7f38aa8b1.png)
* [Youtube_chart_url](https://charts.youtube.com/charts/TopSongs/kr/20210219-20210225?hl=ko)


#### 1-5. Roles
* 정민주 : 
* 이주영 : Crawling, DB 저장(2018-2019 year), slack bot 구현, module 생성(previous_youtube_chart.py, youtube.py, youtube_chatbot.py), READ_ME 작성

****

## 2. Result : 완성된 리스트

![캡처](https://user-images.githubusercontent.com/75352728/111612988-61bce600-8821-11eb-8b21-0e0bce6badc7.PNG)

****

## 3. Process

### 3-1. Variables Setting

#### 1. Variables

* 데이터 정의
  *  name : 노래 제목
  *  artist : 아티스트(가수)
  *  viewCount : 조회수
  *  current_Rank : 현재 순위
  *  previous_Rank : 이전 순위
  *  change : 현재 순위와 이전 순위 변동률
  *  period_on_chart : 차트 유지 기간
  *  image : 사진
  *  play_url : 동영상 play url

#### 3-2. Details

1. 사이트 분석
2. 원하는 데이터 불러오기
3. scrapy.py 작성
4. mongodb에 db 저장
5. crontab, server 이용하여 정해진 날에 scrapying 자동실행
6. 챗봇을 이용하여 서비스 제공

![캡처](https://user-images.githubusercontent.com/75352728/111613369-c8420400-8821-11eb-9b60-141c7bd81e97.PNG)

### 3-3. Process

#### 1. 사이트 분석

![image](https://user-images.githubusercontent.com/75352728/110234339-4aead980-7f6d-11eb-98cc-e59aa9a90cdb.png)


![image](https://user-images.githubusercontent.com/75352728/110234324-3a3a6380-7f6d-11eb-8648-b773413cf840.png)

* 날짜를 변경하면 url 변경 -> 동적 스크래핑
* post 방식
* json
* key 값 존재 -> key 값으로 인해 정보 변경 가능성 있음
--> scrapy 사용 결정

![image](https://user-images.githubusercontent.com/75352728/110234379-84bbe000-7f6d-11eb-9219-7a5a7f8710fa.png)

* url post 방식으로 불러오기 -> 403 error 발생
* referer 요구

![image](https://user-images.githubusercontent.com/75352728/110234450-dfedd280-7f6d-11eb-9a60-e5c3726f6731.png)

* Request header -> header값인 referer을 발견함.

![image](https://user-images.githubusercontent.com/75352728/110234493-188dac00-7f6e-11eb-9b88-5a2d98952775.png)

* header값 기입 -> error 발생

![image](https://user-images.githubusercontent.com/75352728/110234500-2cd1a900-7f6e-11eb-9ece-851d66ef7c54.png)

* 개발자 도구 -> request playroad를 query에 입력

![image](https://user-images.githubusercontent.com/75352728/110234547-64405580-7f6e-11eb-8201-98085b938d28.png)

* 성공적으로 json format 불러옴.


#### 2. 원하는 데이터 불러오기 & 

![image](https://user-images.githubusercontent.com/75352728/110234572-8934c880-7f6e-11eb-8002-55ca9633bf63.png)

* 개발자 도구에서 본 불러온 json 에 저장된 값들
* 원하는 값을 불러오기
  *  contents > sectionListRenderer > contents > 0 > musicAnalyticsSectionRenderer > content > trackTypes > 0 > trackViews

![원하는 값 불러오기 위해 생성](https://user-images.githubusercontent.com/75352728/110234679-298aed00-7f6f-11eb-8a60-1d47fa1a5007.PNG)

* name, artist, viewCount, current_Rank, previous_Rank, change, period_on_chart, image, play_url 불러오기

##### 1. name(노래 제목)

```
title = [{"title":data["name"]}
        for data in datas]
title
```
![title 코드](https://user-images.githubusercontent.com/75352728/110235012-1da02a80-7f71-11eb-944f-63185ab404b4.PNG)

* datas에 들어있는 data를 for문을 이용하여 하나씩 가져오기
* 노래제목은 dict 안에 key값 name에 들어있음.

![title](https://user-images.githubusercontent.com/75352728/110796389-3d11bd00-82bb-11eb-80f2-6a45852b4d0b.png)


##### 2. artist(가수)

```
artist = [{"artist":data["artists"][0]["name"]}
        for data in datas]
artist
```
![artist 코드값](https://user-images.githubusercontent.com/75352728/110235057-5b04b800-7f71-11eb-9e12-e2414963530c.PNG)

* datas에 들어있는 data를 for문을 이용하여 하나씩 가져오기
* 가수 이름은 dict 안에 key값 artists에 들어있음.
* artists 의 value는 list 안 dict 타입으로 list에 들어있는 0번째 data를 빼오기 위해 `[0]` 을 사용 
* dict 안에 name value값 빼오기

![artist](https://user-images.githubusercontent.com/75352728/110234958-a8ccf080-7f70-11eb-97f9-63ce7f07f64c.PNG)


##### 3. viewCount(조회수)

![viewcount 코드](https://user-images.githubusercontent.com/75352728/110235799-59d58a00-7f75-11eb-88b3-f3e22dd39906.PNG)

* datas에 들어있는 data를 for문을 이용하여 하나씩 가져오기
* 조회수는 dict 안에 key값 viewCount에 들어있음.
* 조회수를 백만단위(M)로 변환
* `data["viewCount"]`는 str타입으므로 float로 변환
* 소숫점 두자리까지 나타내기 위해 round() 함수 사용 
* 단위를 붙여주기 위해 int타입으로 바꾼 data를 string타입으로 변환 후 백만 단위 "M" 붙이기

```
viewCount = [{"viewCount":str(round((int(data["viewCount"])/1000000),2)) + "M"}
        for data in datas]
viewCount
```

![viewcount](https://user-images.githubusercontent.com/75352728/110235840-b638a980-7f75-11eb-88c4-a302fee45b9e.PNG)

##### 3. 현재순위, 이전순위, 순위유지기간, 순위변동률

```
chartEntryMetadata= [{"change":data["chartEntryMetadata"]}
        for data in datas]
chartEntryMetadata
```

* 딕셔너리 형태 하나에 현재순위, 이전순위, 순위유지기간, 순위변동률 4개의 data가 들어 있음.
* get()을 사용해서 각 data를 가져올 수 있음.

![image](https://user-images.githubusercontent.com/75352728/110797318-4d766780-82bc-11eb-8b07-72c202b80627.png)

##### 3-1. current_Rank(현재순위)
```
current_Rank= [{"current_Rank":data['chartEntryMetadata'].get('currentPosition')}
        for data in datas]
current_Rank
```

![image](https://user-images.githubusercontent.com/75352728/110797590-94645d00-82bc-11eb-84f1-fd92a030b63c.png)

##### 3-2. previous_Rank(이전순위)

```
previous_Rank= [{"previous_Rank":data['chartEntryMetadata'].get('previousPosition')}
        for data in datas]
previous_Rank
```
![image](https://user-images.githubusercontent.com/75352728/110797673-ac3be100-82bc-11eb-9e9c-f5ca469bb1d1.png)

##### 3-3. change(순위변동률)

```
change= [{"change":data['chartEntryMetadata'].get('percentViewsChange')}
        for data in datas]
change
```
![image](https://user-images.githubusercontent.com/75352728/110797762-ce356380-82bc-11eb-94bc-2c7e4ba2ec56.png)

##### 3-4. period_on_chart()

```
period_on_chart= [{"period_on_chart":str(data['chartEntryMetadata'].get('periodsOnChart')) + " week"}
        for data in datas]
period_on_chart
```

![image](https://user-images.githubusercontent.com/75352728/110797909-f9b84e00-82bc-11eb-826b-677049104215.png)

##### 4. 원하는 데이터 한번에 불러오기

```
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

data_1
```
![image](https://user-images.githubusercontent.com/75352728/110801048-2f126b00-82c0-11eb-8900-df01573ebde9.png)


#### 3. 데이터 프레임 변환 & 전처리

##### 3.1 데이터프레임으로 데이터 불러오기

```
import pandas as pd
```

```
df = pd.DataFrame(data_1)
df.head()
```

![image](https://user-images.githubusercontent.com/75352728/110798379-74816900-82bd-11eb-9e11-4971b8f7f006.png)

* dataframe을 보면 NaN 값이 있는 것을 알 수 있음
* 조회수 -  단위 변경이 필요
* 순위 변동률 - % 단위로 표현하고 소숫점 둘째자리까지만 표현하도록 변경 필요

##### 3.2 데이터프레임 정보

```
df.info()
```
![image](https://user-images.githubusercontent.com/75352728/110798839-e659b280-82bd-11eb-86f8-1587764d07e8.png)

* previous_Rank와 change 에 NaN 값이 있는 것을 알 수 있음

##### 3.3 NaN 값 0으로 변경

```
import numpy as np
```
```
df = df.replace(np.nan,0)
```
##### 3.4 변경 확인

```
df.info()
```
![image](https://user-images.githubusercontent.com/75352728/110799257-549e7500-82be-11eb-896c-de33e17481b6.png)

##### 3.4 previous_Rank 단위 변경

```
df['previous_Rank'].astype(int)
```

* 현재순위에 맞게 int타입으로 변환

##### 3.4 change 소수 첫째자리인 percentage로 변환

```
df['change'] = round(df['change'] * 100,1).astype(str) + "%"
df.head()
```
![image](https://user-images.githubusercontent.com/75352728/110799605-b1019480-82be-11eb-907b-cab1b1a7d40b.png)


#### 4. .py 형태로 모듈 만들기

##### 4.1 py 파일(previous_youtube: 이전 날짜 data, youtube: 현재 날짜 불러오기)
```
import numpy as np
import requests
import re
import json
import pandas as pd


# 함수로 만들기
def youtube():
    
    # 1. 날짜 지정
    from datetime import datetime
    date = datetime.now()
    start_date = int(date.strftime("%Y%m%d"))
    import datetime
    end_date = date + datetime.timedelta(days=6)
    end_date = int(end_date.strftime("%Y%m%d"))

# 이전 날짜 불러오는 코드 
# date_range함수와 빈도를 이용해 금요일만 불러옴
# date가 여러개 이기 때문에 for함수 사용

      #start = pd.date_range(start ='4-27-2018',  
       #          end ='12-27-2019', freq ='7D') 
       #start_date = start.strftime('%Y%m%d')
        #start_date= start_date.to_list() 
        #import datetime
        #end = start + datetime.timedelta(days=6)
        #end_date = end.strftime('%Y%m%d')
        #end_date= end_date.to_list() 
        #start_date,end_date 
        #for start_date,end_date in zip(start_date,end_date):
        #    url = "https://charts.youtube.com/charts/TopSongs/kr?hl=ko"

            # 2. key값 불러오기.
            response = requests.get(url)
            key = re.findall('"INNERTUBE_API_KEY":"\w+\W+\w+"', response.text)[0].split(":")[1].replace('"','')

    
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
    # 이전 날짜 data 불러오는 과정에서 url과 img data가 없는 경우가 있으므로 try, except을 이용
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

    # 9. mongodb로 db저장
   
    import pymongo

    client = pymongo.MongoClient("[mongodb주소:2017]")
    collection = client.youtube.data


    collection.insert_many(data_1)
```
* 참고 : mogodb 설치, 보안 설정 (패캠 수업)
* 처음 하는 분들을 위한 사이트 소개
[mongodb 설치, 보안 설정 참고 자료 : url ](https://chichi.space/post/%ED%95%9C%EB%B2%88%EC%97%90-%EB%81%9D%EB%82%B4%EB%8A%94-AWS-EC2%EC%97%90-MongoDB-%EC%84%A4%EC%B9%98%ED%95%98%EA%B3%A0-%EB%B3%B4%EC%95%88%EC%84%A4%EC%A0%95%ED%95%98%EA%B8%B0/) 

![캡처](https://user-images.githubusercontent.com/75352728/111609570-cbd38c00-881d-11eb-97af-2dbd02cc92c9.PNG)

* 생각보다 data가 많다.

##### 4.2 이전 날짜 크롤링(previous_youtube_chart 모듈 실행)

```
import previous_youtube_chart

previous_youtube_chart.previous_youtube_chart()
```


##### 4.3 현재 날짜 크롤링

```
import previous_youtube_chart

previous_youtube_chart.previous_youtube_chart()
```
```
crontab -e
```
![crontab -e](https://user-images.githubusercontent.com/75352728/111609236-70a19980-881d-11eb-9811-9a089938c9be.PNG)

* previous_youtube_chart.py 를 crontab 을 이용해서 매주 일요일마다 정보 불러올 예정
* 경로는 절대경로가 가장 좋음.
* 일요일 11:30 분에 할 예정
* 참고 :  [crontab 설정 : https://nahosung.tistory.com/95 ](https://nahosung.tistory.com/95)

#### 5. db에 저장한 data slack봇에 보내기

##### 5.1 모듈 불러오기

```
import pymongo
import requests,json
```
##### 5.2 db 불러오기

```
client = pymongo.MongoClient("mongodb주소://:27017")
db = client.youtube #client :  mongodb주소, youtube : database
collection = db.data #data : collection 
searches  = collection.find({'artist':{'$regex':'방탄'},'date':{'$regex':'2021'}})
# regex를 이용해서 특정 단어만 들어 있어도 불러 올수 있게 만듦
# find : 원하는 정보 모두를 불러옴.
msg = []

for search in searches:
        msg.append(search)
# 불러온 db를 이용하여 각 변수명에 저장(for 문 이용)
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
```

* [참고 : https://www.fun-coding.org/mongodb_basic5.html](https://www.fun-coding.org/mongodb_basic5.html)

##### 5.2 slack attachment를 이용해 원하는 형식으로 보내기
```
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
```

* f 형식을 이용해 원하는 값을 
*  [참고 : attachment 구조 확인: https://api.slack.com/block-kit](https://api.slack.com/block-kit)
* 위 주소에서 만들고 싶은 코드를 직접 확인 할 수 있음.
* attachments 변수를 payload에 추가할 필요가 있음.

##### 6. 챗봇 함수

```
def send_msg(slack_webhook, msg, channel="your_channe_name", username="차트알림>봇"):
    payload = {"channel": channel, "username": username, "text": text, "attachments":attachments}
    requests.post(slack_webhook, json.dumps(payload))
```
```
slack_webhook = ""
send_msg(slack_webhook, json.dumps(mu))
```

##### 7. Slack에 보내기

![캡처](https://user-images.githubusercontent.com/75352728/111613013-684b5d80-8821-11eb-8727-9574386afb87.PNG)

*****

## 4. Conclusion

- youtube chart 크롤링
- DB mongodb에 저장
- Slack에 전송
- 현재 작성자가 원하는 데이터만 슬랙에 전송 가능
- 예시) 날짜별 차트 전송(매주 전송) 

## 5. comment & limitations

- 추후 Flask, outgoing webhook(slack)을 이용하여 사용자가 원하는 정보를 선택적으로 전송 연구 필요
