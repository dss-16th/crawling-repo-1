#  유튜브 차트(조회순 기준) 100을 챗봇을 이용하여 전송해주는 서비스



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
조회수가 기준인 유튜브 차트 100을 이용하여 소비자들에게 정보제공을 하기 위해 크롤링과 메세지보내기를 이용한다.

#### 1-4. Dataset

![image](https://user-images.githubusercontent.com/75352728/110234179-60abcf00-7f6c-11eb-8141-8fa7f38aa8b1.png)
[Youtube_chart_url](https://charts.youtube.com/charts/TopSongs/kr/20210219-20210225?hl=ko)


#### 1-5. Roles
정민주 : 
이주영 : 

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

![image](https://user-images.githubusercontent.com/75352728/110234282-efb8e700-7f6c-11eb-98a1-9e64545ce1fa.png)

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


#### 2. 원하는 데이터 불러오기

![image](https://user-images.githubusercontent.com/75352728/110234572-8934c880-7f6e-11eb-8002-55ca9633bf63.png)

* 개발자 도구에서 본 불러온 json 에 저장된 값들
* 원하는 값을 불러오기
  *  contents > sectionListRenderer > contents > 0 > musicAnalyticsSectionRenderer > content > trackTypes > 0 > trackViews

![원하는 값 불러오기 위해 생성](https://user-images.githubusercontent.com/75352728/110234679-298aed00-7f6f-11eb-8a60-1d47fa1a5007.PNG)

* name, artist, viewCount, current_Rank, previous_Rank, change, period_on_chart, image, play_url 불러오기

##### 1. 
