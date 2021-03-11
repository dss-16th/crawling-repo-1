#  유튜브 차트(조회수 기준) 100을 챗봇을 이용하여 전송해주는 서비스



#### __CRAWLING PROJECT__
****
#### 기간 : 
#### * 인원 : 2명
##### * 정민주 :  
##### 
##### GitHub address : [https://github.com/meiren13](https://github.com/meiren13)
##### * 이주영 : 
##### 
##### GitHub address : [https://github.com/leekj3133](https://github.com/leekj3133)

****
#### reference
* C
****


## 1. Intro

#### 1-1. Intro

#### 1-2. purpose
조회수가 기준인 유튜브 차트 100을 이용하여 소비자들에게 정보제공을 하기 위해 크롤링과 메세지보내기를이용

#### 1-4. Dataset

![image](https://user-images.githubusercontent.com/75352728/110234179-60abcf00-7f6c-11eb-8141-8fa7f38aa8b1.png)
[Youtube_chart_url](https://charts.youtube.com/charts/TopSongs/kr/20210219-20210225?hl=ko)


#### 1-5. Roles
* 정민주 : 
* 이주영 : 

****

## 2. Result : 완성된 리스트

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

![image](https://user-images.githubusercontent.com/75352728/110268139-8a183980-8004-11eb-8fec-0433377471e2.png)

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
* 
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

#### 5. 

