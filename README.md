# gcp-pipline-twitter
GCP를 기반으로 간단한 데이터 파이프라인을 구성하는 프로젝트입니다.
![image](https://user-images.githubusercontent.com/68193636/193706881-d47c2fe6-8dd2-4718-b391-c65023a05291.png)

### Docker Image
1. twitter app을 생성하고, key를 아래의 형태로 json파일에 저장합니다. _(twitter_key.json)_  
https://developer.twitter.com/en/portal/dashboard  

```json
{
   "bearer_token":"(발급받은 키)",
   "consumer_key":"(발급받은 키)",
   "consumer_secret":"(발급받은 키)",
   "access_token":"(발급받은 키)",
   "access_token_secret":"(발급받은 키)"
}
```
2. GCP 프로젝트의 서비스 계정 키를 json파일로 만듭니다  
_(IAM 및 관리자 > 서비스 계정 > 키 만들기)_  

3. repository의 파일을 받습니다  

4. tweet_new_version.py 파일을 수정합니다 
  >* key_path를 2에서 생성한 파일명으로 변경
  >* topic_path의 'tweet-pipeline-362010'를 본인의 GCP 프로젝트 id로 변경

5. 도커 이미지를 생성합니다  

6. Google Cloud SDK를 설치하고 도커 이미지를 업로드합니다


### Pub/Sub
* topic id: tweets

### BigQuery
- 데이터셋 이름: tweet_data
- 테이블 이름: tweets
- 테이블 스키마  
![image](https://user-images.githubusercontent.com/68193636/193709226-7e09faa4-ba68-4e68-8e96-46b0390e7b6d.png)

### Cloud Functions
* 트리거: Pub/Sub
* 코드
```python
import base64
import json
from google.cloud import bigquery

def tweets_to_bq(tweet):
  client = bigquery.Client()
  dataset_ref = client.dataset('tweet_data')
  table_ref = dataset_ref.table('tweets')
  table = client.get_table(table_ref)
  tweet_dict = json.loads(tweet)
  rows_to_insert = [
  (tweet_dict['id'], tweet_dict['created_at'], tweet_dict['text'])
  ]
  error = client.insert_rows(table, rows_to_insert)
  print(error)
  
def hello_pubsub(event, context):
  """Triggered from a message on a Cloud Pub/Sub topic.
  Args:
  event (dict): Event payload.
  context (google.cloud.functions.Context): Metadata for the event.
  """
  pubsub_message = base64.b64decode(event['data']).decode('utf-8')
  print(pubsub_message)
  tweets_to_bq(pubsub_message)
```
* requirements.txt  
`google-cloud-bigquery`
