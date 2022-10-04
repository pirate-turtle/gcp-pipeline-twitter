import json

import tweepy
from google.cloud import pubsub_v1
from google.oauth2 import service_account

key_path = 'tweet-pipeline-362010-911f54e509cb.json'

credentials = service_account.Credentials.from_service_account_file(
    key_path,
    scopes=['https://www.googleapis.com/auth/cloud-platform']
)

client = pubsub_v1.PublisherClient(credentials=credentials)
topic_path = client.topic_path('tweet-pipeline-362010', 'tweets')

# Twitter API Key 저장해둔 파일에서 불러오기
with open('twitter_key.json') as f:
    twitter_key = json.load(f)

bearer_token = twitter_key['bearer_token']

class IDPrinter(tweepy.StreamingClient):
    def on_tweet(self, tweet):
        print(tweet)
        tweet = json.dumps({'id': tweet.id, 'created_at': tweet.created_at, 'text': tweet.text}, default=str)
        client.publish(topic_path, data=tweet.encode('utf-8'))
    
    
    def on_error(self, status_code):
        print(status_code)
        if status_code == 420:
            return False

printer = IDPrinter(bearer_token)

# 필터 규칙은 한번 설정하면 v2 엔드포인트에 저장됨
# printer.add_rules(tweepy.StreamRule("Netflix"))
# print(printer.get_rules())

printer.filter(tweet_fields='created_at')
