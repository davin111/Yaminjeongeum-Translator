# scrape_tweets.py
# 트윗 수집하기

# Author: 변다빈
# 2017/12/18
# Course: Language and Computer

# Final term project

import tweepy, datetime

# 인증 요청하기. 트위터 앱의 consumer 정보
consumer_key = 'A8EZe4fYvOcEPqwGNZ0HANMlz'
consumer_secret = 'rFtR5ekZh2orwJMNDZfDyyScEvBtaeioTBa8jFRLywFDGIxUcl'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

# access 토큰 요청하기.
access_token = '526546698-MnydNTLZiTG9y0AU2JBKYk3YnrYZ03pJicFdeBXu'
access_token_secret = 'LkJaBlKN71SJr4dzcZZnXcy2JPaAvxlEHMLmxcJU90H4U'

auth.set_access_token(access_token, access_token_secret)

# twitter API 생성
api = tweepy.API(auth)


## 필요에 따라 수시로 변경해서 사용 ##
keyword = '댕댕이 OR 롬곡' # 검색할 내용 - 'OR' 등 search operator들은 https://developer.twitter.com/en/docs/tweets/search/guides/standard-operators 참고
N = 2000 # 중간에 오류가 발생하거나 트윗이 더 없지 않는 이상 약 N개의 트윗을 수집
file_name = 'data/yamin_tweets.txt' # 수집한 트윗을 저장할 파일
last_id = 0 # 이 트윗부터 과거의 트윗들을 검색 시작. 0이면 가장 최근 트윗부터.
start_num = 1745 # 이 문서에서 몇 번째 수집하기 시작하는 트윗인지(기존에 얼마나 많은 트윗을 이 문서에 수집했는지)
## 필요에 따라 수시로 변경해서 사용 ##


tweet_count = 0 # 이번 차수에 수집한 트윗의 개수
print("'{}'을/를 검색해 최대 약 {}개의 트윗을 내려받습니다. 시작 트윗 번호는 {}입니다.".format(keyword, N, start_num))
with open(file_name, 'a') as f: # 한 파일에 지속적으로 수집을 하기 위해서는 'a' 사용
    # 수집을 시작하면서 무엇에 대한 검색 결과인지 출력
    f.write("----------------------------------------\n\
\'" + keyword + "\'" + '을/를 찾은 검색결과 입니다.\n\n')

    t = datetime.datetime.now() # 언제 수집한 내용인지를 파악하기 위해 수집 시작 시간 저장
    while tweet_count < N: # 수집한 트윗의 개수가 목표치보다 적으면 계속 수집
        try: # 오류가 발생하지 않는 이상 진행 - 대표적인 것: "Rate limit exceeded"
            tweets = api.search(keyword, count = 15, max_id = last_id) # count로 수집할 단위 조절 가능. 15개가 기본이자 최대.
            if not tweets: # 더 이상 이 검색어로 트윗이 존재하지 않으면
                print('더 이상 트윗이 존재하지 않습니다.') # 메시지를 출력하고
                break # 중단

            for tweet in tweets: # (15개씩) 수집한 트윗들 하나씩에 대해
                f.write(str(tweet_count+start_num) + '\t' + str(tweet.created_at) + '\t' + tweet.text + '\n') # 몇 번째 수집한 트윗인지, 언제 작성된 트윗인지, 트윗의 내용을 파일에 작성
                tweet_count += 1 # 수집한 트윗의 개수 추가

            print('{}개의 트윗을 내려받았습니다.'.format(tweet_count)) # 일반적으로 count 개수만큼 수집할 때마다 알림
            last_id = tweets[-1].id #중요# 마지막 트윗의 ID를 저장해두었다가 max_id에 사용함으로써 계속해서 시간을 거슬러 올라갈 수 있음.

        except tweepy.TweepError as e: # 오류가 발생하면 - "Rate limit exceeded"
            print('오류 발생: ' + str(e)) # 그 내용을 출력하고
            break # 중단

    # 한 번 수집을 마치고 나면 기록해두기
    f.write('--------------------\n\
{}부터 {}까지는 {}년 {}월 {}일 {}시 {}분 {}초에 수집한 트윗들입니다.\n\
마지막 트윗의 ID는 {}입니다.\n\n\n'.format(start_num, tweet_count+start_num, t.year, t.month, t.day, t.hour, t.minute, t.second, last_id))
# 마지막 트윗의 ID를 기억해두면 다음에 이어서 또 그 이전의 트윗들을 수집할 수 있으므로 유용
print("{}개의 트윗을 내려받아 {}에 저장했습니다.\n\
마지막 트윗의 ID는 {}입니다. 파일에 저장된 총 트윗의 개수는 {}개입니다.".format(tweet_count, file_name, last_id, tweet_count+start_num))
