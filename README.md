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

## 3. Proess

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
* 
![title](https://user-images.githubusercontent.com/75352728/110234901-65728200-7f70-11eb-9c76-c66efca55353.PNG)

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
* 단위를 붙여주기 위해 float타입으로 바꾼 data를 string타입으로 변환 후 백만 단위 "M" 붙이기

```
viewCount = [{"viewCount":str(round((float(data["viewCount"])/1000000),2)) + "M"}
        for data in datas]
viewCount
```

![viewcount](https://user-images.githubusercontent.com/75352728/110235840-b638a980-7f75-11eb-88c4-a302fee45b9e.PNG)

##### 3. current_Rank(현재 순위)

![순위 불러오기 코드](https://user-images.githubusercontent.com/75352728/110236033-0401e180-7f77-11eb-8090-5ac3f25676a5.PNG)




