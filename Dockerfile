FROM python:3.7-slim

WORKDIR /app

ADD . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

ENV GOOGLE_APPLICATION_CREDENTIALS="/app/tweet-pipeline-362010-911f54e509cb.json"

CMD ["python", "tweet_new_version.py"]